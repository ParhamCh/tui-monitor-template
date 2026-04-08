"""
ui/node_panel.py
================
Renderable builders for cluster node panels.

This module contains:
    - A custom expandable block bar renderable
    - Node metric row builders
    - Node information row builder
    - Full node panel and empty placeholder panel builders

These helpers are presentation-only and should not perform any data fetching.
All node data must be prepared upstream by the dashboard/data layers.
"""

from rich.align import Align
from rich.console import Console, ConsoleOptions, Group, RenderResult
from rich.measure import Measurement
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Severity threshold for warning state.
WARN_THRESHOLD: int = 60

#: Severity threshold for critical state.
CRIT_THRESHOLD: int = 85

#: Minimum internal width of the custom block bar.
BAR_MIN_WIDTH: int = 6

#: Shared spacer line inserted between metric rows.
ROW_SPACER: Text = Text("")


# ---------------------------------------------------------------------------
# Custom renderables
# ---------------------------------------------------------------------------


class BlockBar:
    """Expandable block bar renderable for percentage-based metrics.

    The bar adapts to the available width at render time and uses filled and
    empty block characters to represent utilization.
    """

    def __init__(
        self,
        value: int,
        *,
        fill: str = "█",
        empty: str = "░",
        show_brackets: bool = True,
        fill_style: str = "white",
        empty_style: str = "grey50",
        min_width: int = BAR_MIN_WIDTH,
    ) -> None:
        self.value = max(0, min(100, int(value)))
        self.fill = fill
        self.empty = empty
        self.show_brackets = show_brackets
        self.fill_style = fill_style
        self.empty_style = empty_style
        self.min_width = min_width

    def __rich_measure__(
        self,
        console: Console,
        options: ConsoleOptions,
    ) -> Measurement:
        """Return the minimum/maximum width for the renderable."""
        min_width = self.min_width + (2 if self.show_brackets else 0)
        return Measurement(min_width, options.max_width)

    def __rich_console__(
        self,
        console: Console,
        options: ConsoleOptions,
    ) -> RenderResult:
        """Render the expandable block bar based on the available width."""
        max_width = options.max_width or 0
        bracket_width = 2 if self.show_brackets else 0
        inner_width = max(1, max_width - bracket_width)

        filled = int(round(inner_width * self.value / 100))
        empty = max(0, inner_width - filled)

        bar = Text()

        if self.show_brackets:
            bar.append("[", style="grey70")

        if filled:
            bar.append(self.fill * filled, style=self.fill_style)

        if empty:
            bar.append(self.empty * empty, style=self.empty_style)

        if self.show_brackets:
            bar.append("]", style="grey70")

        yield bar


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def format_status(status: str) -> Text:
    """Return a colorized status label for a node."""
    if status == "Ready":
        return Text(status, style="green")
    return Text(status, style="bold red")


def severity_style(value: int) -> str:
    """Return the severity style for a utilization percentage."""
    value = max(0, min(100, int(value)))

    if value >= CRIT_THRESHOLD:
        return "bold red"
    if value >= WARN_THRESHOLD:
        return "yellow"
    return "green"


def metric_row(label: str, value: int) -> Table:
    """Build a single metric row containing label, bar, and percentage."""
    grid = Table.grid(expand=True, padding=(0, 1))
    grid.add_column(width=4)
    grid.add_column(ratio=1)
    grid.add_column(justify="right", width=4)

    grid.add_row(
        Text(f"{label:<3}", style="cyan"),
        BlockBar(
            value,
            show_brackets=False,
            fill_style=severity_style(value),
            empty_style="grey35",
        ),
        Text(f"{value:>3}%", style=severity_style(value)),
    )
    return grid


def info_row(pods: int, latency_ms: int) -> Table:
    """Build the bottom information row for a node panel."""
    grid = Table.grid(expand=True, padding=(0, 1))
    grid.add_column(ratio=1)
    grid.add_column(justify="right")

    grid.add_row(
        Text(f"Pods: {pods}", style="yellow"),
        Text(f"Lat: {latency_ms}ms", style="yellow"),
    )
    return grid


def build_node_title(node: dict) -> Text:
    """Build the panel title for a node."""
    title = Text()
    title.append(node["name"], style="bold")
    title.append(" | ")
    title.append(node["role"], style="magenta")
    title.append(" | ")
    title.append_text(format_status(node["status"]))
    return title


# ---------------------------------------------------------------------------
# Public renderable builders
# ---------------------------------------------------------------------------


def build_empty_node_panel(title: str = "Empty") -> Panel:
    """Build a placeholder panel for unused grid cells."""
    return Panel(
        Align.center(Text("—", style="grey50"), vertical="middle"),
        title=Text(title, style="grey50"),
        border_style="grey50",
        padding=(0, 1),
    )


def build_node_panel(node: dict) -> Panel:
    """Build a full node panel from a node-state dictionary.

    The panel contains:
        - A title with node name, role, and readiness status
        - CPU / RAM / Disk metric rows
        - One compact info row with pod count and latency
    """
    content = Group(
        ROW_SPACER,
        metric_row("CPU", node["cpu"]),
        ROW_SPACER,
        metric_row("RAM", node["memory"]),
        ROW_SPACER,
        metric_row("DSK", node["disk"]),
        ROW_SPACER,
        info_row(node["pods"], node["latency_ms"]),
    )

    return Panel(
        content,
        title=build_node_title(node),
        border_style="blue",
        padding=(0, 1),
    )