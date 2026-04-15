"""
dashboard.py
============
Entry point for the TUI cluster-monitoring dashboard.

This module is responsible for the full lifecycle of the dashboard:
    - Building the layout structure
    - Initializing all UI sections before rendering begins
    - Running the main live-update loop
    - Graceful shutdown

Typical usage::

    from dashboard import run_dashboard
    run_dashboard()
"""

import time

from rich.align import Align
from rich.columns import Columns
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from data.fake_cluster import get_cluster_state
from terminal_input import TerminalKeyReader
from ui.pages import build_content_page
from ui.sidebar import build_sidebar
from ui.layout import build_layout


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: How often (in seconds) the dashboard state is refreshed.
UPDATE_INTERVAL: float = 1.0

#: Rich ``Live`` refresh rate derived from UPDATE_INTERVAL so the two stay
#: in sync and never diverge silently.
REFRESH_PER_SECOND: float = 1.0 / UPDATE_INTERVAL

#: Default initial view shown in the main content area.
DEFAULT_VIEW: str = "nodes"

#: Static sidebar menu definition.
#: Each item is defined as: (shortcut_key, view_id, label)
MENU_ITEMS: tuple[tuple[str, str, str], ...] = (
    ("1", "prometheus", "Prometheus"),
    ("2", "nodes", "Nodes"),
    ("3", "cluster", "Cluster"),
    ("4", "gateway", "Gateway"),
    ("5", "app", "App"),
)


# ---------------------------------------------------------------------------
# Context helpers
# ---------------------------------------------------------------------------


def create_context() -> dict:
    """Create and return the initial runtime context for the dashboard.

    The context dictionary is a lightweight container for mutable state that
    must survive across frames but does not belong to any single component.

    Returns:
        A dictionary with the following keys:

        - ``start_time`` (*float*): ``time.time()`` at dashboard launch, used to compute uptime.
        - ``current_view`` (*str*): Identifier of the currently active content page.
    """
    return {
        "start_time": time.time(),
        "current_view": DEFAULT_VIEW,
    }


# ---------------------------------------------------------------------------
# Layout update helpers
# ---------------------------------------------------------------------------


def update_sidebar(layout, ctx: dict) -> None:
    """Render the navigation sidebar for the currently active view.

    Args:
        layout: The active Rich ``Layout`` tree.
        ctx: Runtime context dictionary containing navigation state.
    """
    layout["sidebar"].update(
        build_sidebar(MENU_ITEMS, ctx["current_view"])
    )


def resolve_view_from_key(key: str) -> str | None:
    """Resolve a target view identifier from a pressed shortcut key.

    Args:
        key: Single-character keyboard input.

    Returns:
        The matching view identifier if the key exists in ``MENU_ITEMS``,
        otherwise ``None``.
    """
    for shortcut, view_id, _label in MENU_ITEMS:
        if shortcut == key:
            return view_id
    return None


def apply_navigation_input(ctx: dict, key: str) -> bool:
    """Apply one navigation key to the runtime context.

    This function is intentionally limited to state mutation only. It does not
    perform any rendering by itself.

    Args:
        ctx: Runtime context dictionary.
        key: Single-character keyboard input.

    Returns:
        ``True`` if the active view changed, otherwise ``False``.
    """
    target_view = resolve_view_from_key(key)
    if target_view is None:
        return False

    if target_view == ctx["current_view"]:
        return False

    ctx["current_view"] = target_view
    return True


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------


def format_uptime(start_time: float) -> str:
    """Convert an epoch *start_time* to a human-readable uptime string.

    Args:
        start_time: The ``time.time()`` value recorded when the dashboard
                    was launched.

    Returns:
        A zero-padded ``"HH:MM:SS"`` string representing elapsed wall time.

    Example::

        >>> format_uptime(time.time() - 3725)
        '01:02:05'
    """
    elapsed: int = int(time.time() - start_time)
    hours, remainder = divmod(elapsed, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


# ---------------------------------------------------------------------------
# Renderable builders
# ---------------------------------------------------------------------------


def render_header() -> Panel:
    """Build and return the top header panel for the current tick.

    The header shows the application title on the left and the current
    wall-clock time on the right.

    Returns:
        A :class:`rich.panel.Panel` ready to be passed to ``Layout.update()``.
    """
    left = Text("TUI Monitor", style="bold cyan")
    right = Align.right(Text(f"Time: {time.strftime('%H:%M:%S')}", style="cyan"))
    content = Columns([left, right], expand=True)
    return Panel(content, border_style="cyan")


def render_footer(start_time: float) -> Panel:
    """Build and return the bottom footer panel showing uptime and exit hint.

    Args:
        start_time: Dashboard launch epoch used to compute the uptime string.

    Returns:
        A :class:`rich.panel.Panel` ready to be passed to ``Layout.update()``.
    """
    left = Text("Press Ctrl+C to exit", style="grey70")
    right = Align.right(Text(f"Uptime: {format_uptime(start_time)}", style="grey70"))
    content = Columns([left, right], expand=True)
    return Panel(content, border_style="grey50")


# ---------------------------------------------------------------------------
# Dashboard lifecycle
# ---------------------------------------------------------------------------


def build():
    """Build and return the base layout structure.

    This is deliberately separated from :func:`initialize` so that the layout
    tree can be constructed without triggering any I/O or data fetches.

    Returns:
        A Rich ``Layout`` instance representing the top-level dashboard shell.
    """
    return build_layout()


def initialize(layout) -> dict:
    """Fully populate every layout section before the Live renderer starts.

    Pre-rendering all sections prevents the initial frame from showing blank
    or partially-drawn panels (visual flicker).

    Args:
        layout: The Rich ``Layout`` returned by :func:`build`.

    Returns:
        The runtime context dictionary created by :func:`create_context`.
    """
    ctx = create_context()

    layout["header"].update(render_header())
    layout["footer"].update(render_footer(ctx["start_time"]))
    update_sidebar(layout, ctx)

    cluster = get_cluster_state()

    layout["content"].update(
        build_content_page(
            ctx["current_view"],
            cluster,
        )
    )

    return ctx


def update_frame(layout, ctx: dict) -> None:
    """Fetch fresh data and redraw all dynamic layout sections.

    Called once per :data:`UPDATE_INTERVAL` inside the main render loop.

    Args:
        layout: The active Rich ``Layout`` being rendered by ``Live``.
        ctx: The runtime context dictionary produced by :func:`create_context`.
    """
    layout["header"].update(render_header())
    layout["footer"].update(render_footer(ctx["start_time"]))
    update_sidebar(layout, ctx)

    cluster = get_cluster_state()

    layout["content"].update(
        build_content_page(
            ctx["current_view"],
            cluster,
        )
    )


def run(layout, ctx: dict) -> None:
    """Start the blocking Live render loop.

    The loop reacts to two kinds of events:
        - periodic refresh deadlines
        - numeric navigation key presses

    At this stage, only simple menu switching is supported. Valid shortcut
    keys are defined centrally in ``MENU_ITEMS``.

    Args:
        layout: The fully-initialized Rich ``Layout``.
        ctx: The runtime context dictionary.

    Raises:
        KeyboardInterrupt: Propagated to the caller (:func:`run_dashboard`)
            so shutdown logic can be executed there.
    """
    next_update_at = time.monotonic() + UPDATE_INTERVAL

    with TerminalKeyReader() as key_reader, Live(
        layout,
        refresh_per_second=REFRESH_PER_SECOND,
        screen=True,
        transient=True,
    ):
        while True:
            timeout = max(0.0, next_update_at - time.monotonic())
            key = key_reader.read_key(timeout=timeout)

            if key is not None and apply_navigation_input(ctx, key):
                update_frame(layout, ctx)
                next_update_at = time.monotonic() + UPDATE_INTERVAL
                continue

            now = time.monotonic()
            if now >= next_update_at:
                update_frame(layout, ctx)
                next_update_at = now + UPDATE_INTERVAL


def shutdown() -> None:
    """Execute graceful shutdown tasks before the process exits.

    Currently limited to flushing log handlers.  Add resource-cleanup logic
    (e.g. closing network connections, persisting state) here as the
    application grows.
    """
    return


def run_dashboard() -> None:
    """Build, initialise, and run the TUI dashboard until interrupted.

    This is the single public entry-point for the module.  It wires together
    the full lifecycle::

        build() → initialize() → run() → shutdown()

    A :exc:`KeyboardInterrupt` (Ctrl-C) triggers a clean exit via
    :func:`shutdown` without printing a traceback.
    """
    layout = build()
    ctx = initialize(layout)

    try:
        run(layout, ctx)
    except KeyboardInterrupt:
        shutdown()
