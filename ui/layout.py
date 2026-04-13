"""
ui/layout.py
============
Layout factory for the TUI cluster-monitoring dashboard.

This module builds the full Rich layout tree, including:
    - header
    - summary
    - nodes grid
    - alerts
    - footer

The nodes section supports a limited set of predefined grid presets:
    - 2x2
    - 3x2
    - 3x3

The selected preset determines how many node cells are created and how
dashboard.py later populates them with node panels or empty placeholders.
"""

from rich.layout import Layout


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

#: Static layout section sizes.
HEADER_HEIGHT: int = 3
SUMMARY_HEIGHT: int = 4
ALERTS_HEIGHT: int = 6
FOOTER_HEIGHT: int = 3


# ---------------------------------------------------------------------------
# Layout builder
# ---------------------------------------------------------------------------


def build_layout(grid_preset: str = "3x3") -> Layout:
    """Build and return the dashboard layout for the selected grid preset.

    The resulting layout has the following high-level structure::

        root
        ├── header
        ├── summary
        ├── nodes
        │   ├── nodes_row_0
        │   │   ├── node_0
        │   │   ├── node_1
        │   │   └── ...
        │   └── ...
        ├── alerts
        └── footer

    Notes:
        - The ``nodes`` area is subdivided according to the selected preset.
        - Grid dimensions are stored as metadata on ``layout["nodes"]`` so
          downstream update helpers can compute capacity and fill empty cells.

    Args:
        grid_preset: Grid preset identifier (e.g. ``"2x2"``, ``"3x2"``,
            ``"3x3"``).

    Returns:
        A fully constructed Rich ``Layout`` tree.
    """
    cols, rows = _GRID_PRESETS.get(
        grid_preset,
        (DEFAULT_GRID_COLS, DEFAULT_GRID_ROWS),
    )

    layout = Layout(name="root")
    layout.split_column(
        Layout(name="header", size=HEADER_HEIGHT),
        Layout(name="summary", size=SUMMARY_HEIGHT),
        Layout(name="nodes"),
        Layout(name="alerts", size=ALERTS_HEIGHT),
        Layout(name="footer", size=FOOTER_HEIGHT),
    )

    # Build the grid inside the nodes section.
    layout["nodes"].split_column(
        *[Layout(name=f"nodes_row_{row}", ratio=1) for row in range(rows)]
    )

    for row in range(rows):
        layout[f"nodes_row_{row}"].split_row(
            *[
                Layout(name=f"node_{row * cols + col}", ratio=1)
                for col in range(cols)
            ]
        )

    # Store grid dimensions as metadata for downstream grid update helpers.
    layout["nodes"]._grid_cols = cols
    layout["nodes"]._grid_rows = rows

    return layout