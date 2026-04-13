"""
ui/layout.py
============
Layout factory for the TUI cluster-monitoring dashboard.

This module builds the full Rich layout tree used by the dashboard UI.

High-level structure::

    root
    ├── header
    ├── main
    │   ├── sidebar
    │   └── content
    │       ├── summary
    │       ├── nodes
    │       └── alerts
    └── footer

The nodes section supports a limited set of predefined grid presets:
    - 2x2
    - 3x2
    - 3x3

The selected preset determines how many node cells are created and how
``dashboard.py`` later populates them with node panels or empty placeholders.
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
FOOTER_HEIGHT: int = 3

#: Main horizontal split ratio between the sidebar and content areas.
SIDEBAR_RATIO: int = 1
CONTENT_RATIO: int = 4

#: Content vertical section sizes.
SUMMARY_HEIGHT: int = 4
ALERTS_HEIGHT: int = 6


# ---------------------------------------------------------------------------
# Layout builder
# ---------------------------------------------------------------------------


def build_layout(grid_preset: str = "3x3") -> Layout:
    """Build and return the dashboard layout for the selected grid preset.

    The resulting layout contains a sidebar/content split inside the main
    section, while the node area inside content is further subdivided into
    a fixed grid determined by the selected preset.

    Grid metadata is attached to ``layout["nodes"]`` so downstream update
    helpers can calculate the available node-cell capacity.

    Args:
        grid_preset: Grid preset identifier such as ``"2x2"``, ``"3x2"``,
            or ``"3x3"``.

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
        Layout(name="main"),
        Layout(name="footer", size=FOOTER_HEIGHT),
    )

    layout["main"].split_row(
        Layout(name="sidebar", ratio=SIDEBAR_RATIO),
        Layout(name="content", ratio=CONTENT_RATIO),
    )

    layout["content"].split_column(
        Layout(name="summary", size=SUMMARY_HEIGHT),
        Layout(name="nodes"),
        Layout(name="alerts", size=ALERTS_HEIGHT),
    )

    # Build the fixed node grid inside the content area.
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

    # Store grid dimensions as metadata for downstream update helpers.
    layout["nodes"]._grid_cols = cols
    layout["nodes"]._grid_rows = rows

    return layout