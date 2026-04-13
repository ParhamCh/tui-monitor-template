"""
ui/sidebar.py
=============
Renderable builder for the dashboard navigation sidebar.

This module is responsible only for presentation of navigation items.
It does not handle keyboard input, page routing, or application state
mutation. Those concerns remain in the dashboard/orchestration layer.
"""

from rich.console import Group
from rich.panel import Panel
from rich.text import Text


def _build_menu_item(shortcut: str, view_id: str, label: str, current_view: str) -> Text:
    """Build one navigation menu item.

    The active item is highlighted using a marker and a stronger style so the
    user can clearly identify the currently selected view.

    Args:
        shortcut: Numeric shortcut associated with the menu item.
        view_id: Internal identifier of the target view.
        label: Human-readable label displayed in the sidebar.
        current_view: Identifier of the currently active view.

    Returns:
        A Rich ``Text`` object representing one menu line.
    """
    is_active = view_id == current_view

    item = Text()
    item.append("> " if is_active else "  ", style="cyan" if is_active else "grey50")
    item.append(f"{shortcut}. ", style="bold" if is_active else "white")
    item.append(label, style="bold cyan" if is_active else "white")

    return item


def build_sidebar(
    menu_items: tuple[tuple[str, str, str], ...],
    current_view: str,
) -> Panel:
    """Build the navigation sidebar panel.

    Args:
        menu_items: Static menu definition where each item is a tuple of:
            ``(shortcut_key, view_id, label)``.
        current_view: Identifier of the currently active content view.

    Returns:
        A Rich ``Panel`` containing the rendered navigation menu.
    """
    items = [
        _build_menu_item(shortcut, view_id, label, current_view)
        for shortcut, view_id, label in menu_items
    ]

    content = Group(*items)

    return Panel(
        content,
        title="Navigation",
        border_style="blue",
        padding=(0, 1),
    )