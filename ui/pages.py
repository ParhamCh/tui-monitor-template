"""
ui/pages.py
===========
Page-level renderable builders for the dashboard content area.

This module builds full-page renderables that are inserted into the main
``content`` slot of the dashboard layout.

Current pages:
    - nodes page
    - generic placeholder page
"""

from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text

from ui.components import build_alerts_placeholder, build_cluster_summary
from ui.node_panel import build_empty_node_panel, build_node_panel


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

    The page keeps a stable vertical structure:

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
        Layout(name="summary", size=4),
        Layout(name="nodes"),
        Layout(name="alerts", size=6),
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