"""
ui/pages.py
===========
Page-level routing for the dashboard content area.

This module is responsible for selecting which page renderable should be
placed into the main ``content`` slot based on the active view identifier.
"""

from rich.align import Align
from rich.panel import Panel
from rich.text import Text

from ui.nodes_page import build_nodes_page


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Static page metadata for views that are not implemented yet.
_PLACEHOLDER_PAGES: dict[str, tuple[str, str]] = {
    "prometheus": (
        "Prometheus",
        "Prometheus page is not implemented yet.",
    ),
    "cluster": (
        "Cluster",
        "Cluster page is not implemented yet.",
    ),
    "gateway": (
        "Gateway",
        "Gateway page is not implemented yet.",
    ),
    "app": (
        "Application",
        "Application page is not implemented yet.",
    ),
}


# ---------------------------------------------------------------------------
# Public page builders
# ---------------------------------------------------------------------------


def build_placeholder_page(title: str, message: str) -> Panel:
    """Build a placeholder page for views that are not implemented yet.

    Args:
        title: Title shown on the panel.
        message: Main placeholder message shown in the content body.

    Returns:
        A Rich ``Panel`` with centered placeholder text.
    """
    content = Align.center(
        Text(message, style="yellow"),
        vertical="middle",
    )

    return Panel(
        content,
        title=title,
        border_style="yellow",
    )


def build_content_page(view_id: str, cluster: dict):
    """Build the content renderable for the currently active view.

    Args:
        view_id: Identifier of the active content view.
        cluster: Full cluster-state dictionary.

    Returns:
        A Rich renderable representing the selected page.
    """
    if view_id == "nodes":
        return build_nodes_page(cluster)

    title, message = _PLACEHOLDER_PAGES.get(
        view_id,
        ("Unknown View", "This page is not implemented yet."),
    )
    return build_placeholder_page(title, message)