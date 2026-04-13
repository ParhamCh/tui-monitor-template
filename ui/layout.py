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
    └── footer

The content area acts as a single page-rendering slot. Individual page
builders are responsible for rendering their full internal structure.

The selected grid preset is still stored as metadata on the content area so
page builders can render node pages with the correct grid dimensions.
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


# ---------------------------------------------------------------------------
# Layout builder
# ---------------------------------------------------------------------------


def build_layout(grid_preset: str = "3x3") -> Layout:
    """Build and return the dashboard layout for the selected grid preset.

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

    # Store grid dimensions as metadata for page builders that need them.
    layout["content"]._grid_cols = cols
    layout["content"]._grid_rows = rows

    return layout