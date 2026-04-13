"""
terminal_input.py
=================
Low-level terminal key reader for non-blocking dashboard input.

This module provides a small context-managed helper for reading single-key
input from a terminal without blocking the dashboard render loop.

Design goals:
    - non-blocking key reads
    - safe terminal-mode restoration on exit
    - no coupling to dashboard state or page routing

Notes:
    - This implementation is intended for POSIX-style terminals.
    - If stdin is not a TTY, key reading is automatically disabled.
"""

import select
import sys
import termios
import tty
from typing import TextIO


class TerminalKeyReader:
    """Context-managed non-blocking single-key terminal reader.

    The reader temporarily switches the terminal into cbreak mode so key
    presses can be observed without requiring Enter.

    If the provided stream is not a TTY, the reader disables itself and
    ``read_key()`` always returns ``None``.
    """

    def __init__(self, stream: TextIO | None = None) -> None:
        """Initialize the key reader.

        Args:
            stream: Input stream to read from. Defaults to ``sys.stdin``.
        """
        self._stream: TextIO = stream or sys.stdin
        self._fd: int | None = None
        self._old_attrs: list | None = None
        self._enabled: bool = False

    def __enter__(self) -> "TerminalKeyReader":
        """Enter the terminal reader context and enable cbreak mode if possible.

        Returns:
            The active ``TerminalKeyReader`` instance.
        """
        if self._stream.isatty():
            self._fd = self._stream.fileno()
            self._old_attrs = termios.tcgetattr(self._fd)
            tty.setcbreak(self._fd)
            self._enabled = True

        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        """Restore the original terminal settings on context exit."""
        if self._enabled and self._fd is not None and self._old_attrs is not None:
            termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old_attrs)

    def read_key(self, timeout: float = 0.0) -> str | None:
        """Read one key from the terminal if available.

        The method waits up to ``timeout`` seconds for input. If no key is
        available within the timeout window, ``None`` is returned.

        Args:
            timeout: Maximum time to wait for a key press, in seconds.

        Returns:
            A single-character string if input is available, otherwise ``None``.
        """
        if not self._enabled:
            return None

        ready, _, _ = select.select([self._stream], [], [], timeout)
        if not ready:
            return None

        key = self._stream.read(1)
        return key or None