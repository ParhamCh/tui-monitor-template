"""
ui/pages.py
===========
Page-level renderable builders for the dashboard content area.

This module is responsible for building full-page content renderables that
are inserted into the main ``content`` slot of the dashboard layout.

Currently supported views:
    - nodes
    - prometheus
    - cluster
    - gateway
    - app
"""

from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text

from ui.components import build_alerts_placeholder, build_cluster_summary
from ui.node_panel import build_empty_node_panel, build_node_panel


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

#: Fallback grid dimensions if layout metadata is missing.
DEFAULT_GRID_COLS: int = 3
DEFAULT_GRID_ROWS: int = 3

#: Internal page section sizes for the nodes page.
SUMMARY_HEIGHT: int = 4
ALERTS_HEIGHT: int = 6


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _build_node_grid_layout(nodes: list[dict], grid_cols: int, grid_rows: int) -> Layout:
    """Build a fixed-size node grid as a nested Rich layout.

    This approach guarantees equal-sized grid cells, unlike ``Columns``,
    which may size items based on content width.

    Args:
        nodes: List of node-state dictionaries.
        grid_cols: Number of grid columns.
        grid_rows: Number of grid rows.

    Returns:
        A Rich ``Layout`` containing the node grid.
    """
    capacity = grid_cols * grid_rows
    panels = [build_node_panel(node) for node in nodes[:capacity]]

    while len(panels) < capacity:
        panels.append(build_empty_node_panel())

    grid = Layout(name="nodes_grid")
    grid.split_column(
        *[Layout(name=f"grid_row_{row}", ratio=1) for row in range(grid_rows)]
    )

    for row in range(grid_rows):
        grid[f"grid_row_{row}"].split_row(
            *[
                Layout(name=f"grid_cell_{row * grid_cols + col}", ratio=1)
                for col in range(grid_cols)
            ]
        )

    for idx, panel in enumerate(panels):
        grid[f"grid_cell_{idx}"].update(panel)

    return grid


# ---------------------------------------------------------------------------
# Public page builders
# ---------------------------------------------------------------------------


def build_nodes_page(cluster: dict, grid_cols: int, grid_rows: int) -> Layout:
    """Build the nodes page as a nested layout.

    The nodes page keeps a stable vertical structure consisting of:
        - cluster summary
        - node grid
        - alerts panel

    Args:
        cluster: Full cluster-state dictionary.
        grid_cols: Number of node-grid columns.
        grid_rows: Number of node-grid rows.

    Returns:
        A Rich ``Layout`` representing the complete nodes page.
    """
    page = Layout(name="nodes_page")
    page.split_column(
        Layout(name="summary", size=SUMMARY_HEIGHT),
        Layout(name="nodes"),
        Layout(name="alerts", size=ALERTS_HEIGHT),
    )

    page["summary"].update(build_cluster_summary(cluster["summary"]))
    page["nodes"].update(
        _build_node_grid_layout(cluster["nodes"], grid_cols, grid_rows)
    )
    page["alerts"].update(build_alerts_placeholder())

    return page


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


def build_content_page(
    view_id: str,
    cluster: dict,
    grid_cols: int = DEFAULT_GRID_COLS,
    grid_rows: int = DEFAULT_GRID_ROWS,
):
    """Build the content renderable for the currently active view.

    Args:
        view_id: Identifier of the active content view.
        cluster: Full cluster-state dictionary.
        grid_cols: Number of node-grid columns for the nodes page.
        grid_rows: Number of node-grid rows for the nodes page.

    Returns:
        A Rich renderable representing the selected page.
    """
    if view_id == "nodes":
        return build_nodes_page(cluster, grid_cols, grid_rows)

    title, message = _PLACEHOLDER_PAGES.get(
        view_id,
        ("Unknown View", "This page is not implemented yet."),
    )
    return build_placeholder_page(title, message)