"""
ui/nodes_page.py
================
Nodes page builder for the dashboard content area.

This module owns the full structure of the ``nodes`` view, including:
    - cluster summary
    - node grid
    - alerts panel

It also owns the node-grid preset definition and fallback behavior.
"""

from rich.layout import Layout

from config import GRID_PRESET
from ui.components import build_alerts_placeholder, build_cluster_summary
from ui.node_panel import build_empty_node_panel, build_node_panel


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Supported node-grid presets in the format "cols x rows".
_GRID_PRESETS: dict[str, tuple[int, int]] = {
    "2x2": (2, 2),
    "3x2": (3, 2),
    "3x3": (3, 3),
}

#: Default preset dimensions used when an invalid preset is provided.
DEFAULT_GRID_COLS: int = 3
DEFAULT_GRID_ROWS: int = 3

#: Static section sizes inside the nodes page.
SUMMARY_HEIGHT: int = 4
ALERTS_HEIGHT: int = 6


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _resolve_grid_preset() -> tuple[int, int]:
    """Resolve the active node-grid preset from configuration.

    Returns:
        A tuple of ``(grid_cols, grid_rows)``.
    """
    return _GRID_PRESETS.get(
        GRID_PRESET,
        (DEFAULT_GRID_COLS, DEFAULT_GRID_ROWS),
    )


def _build_node_grid_layout(nodes: list[dict]) -> Layout:
    """Build a fixed-size node grid as a nested Rich layout.

    Args:
        nodes: List of node-state dictionaries.

    Returns:
        A Rich ``Layout`` containing the node grid.
    """
    grid_cols, grid_rows = _resolve_grid_preset()
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
# Public page builder
# ---------------------------------------------------------------------------


def build_nodes_page(cluster: dict) -> Layout:
    """Build the nodes page as a nested layout.

    The nodes page keeps a stable vertical structure consisting of:
        - cluster summary
        - node grid
        - alerts panel

    Args:
        cluster: Full cluster-state dictionary.

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
    page["nodes"].update(_build_node_grid_layout(cluster["nodes"]))
    page["alerts"].update(build_alerts_placeholder())

    return page