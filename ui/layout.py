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

The content area is a single page-rendering slot. Individual page builders
are responsible for rendering their own internal layout and page structure.
"""

from rich.layout import Layout


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Static layout section sizes.
HEADER_HEIGHT: int = 3
FOOTER_HEIGHT: int = 3

#: Main horizontal split ratio between the sidebar and content areas.
SIDEBAR_RATIO: int = 1
CONTENT_RATIO: int = 6


# ---------------------------------------------------------------------------
# Layout builder
# ---------------------------------------------------------------------------


def build_layout() -> Layout:
    """Build and return the top-level dashboard shell layout.

    Returns:
        A fully constructed Rich ``Layout`` tree containing the application
        shell with header, sidebar, content area, and footer.
    """
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

    return layout