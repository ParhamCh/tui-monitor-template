from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich.measure import Measurement
from rich.console import Group, Console, ConsoleOptions, RenderResult

class BlockBar:
    """Expandable ████░░░░ bar that adapts to available width."""

    def __init__(
        self,
        value: int,
        *,
        fill: str = "█",
        empty: str = "░",
        show_brackets: bool = True,
        fill_style: str = "white",
        empty_style: str = "grey50",
        min_width: int = 6,
    ):
        self.value = max(0, min(100, int(value)))
        self.fill = fill
        self.empty = empty
        self.show_brackets = show_brackets
        self.fill_style = fill_style
        self.empty_style = empty_style
        self.min_width = min_width

    def __rich_measure__(self, console: Console, options: ConsoleOptions) -> Measurement:
        # Minimum width that still looks like a bar
        min_w = self.min_width + (2 if self.show_brackets else 0)
        return Measurement(min_w, options.max_width)

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        max_w = options.max_width or 0
        bracket_w = 2 if self.show_brackets else 0
        inner_w = max(1, max_w - bracket_w)

        filled = int(round(inner_w * self.value / 100))
        empty = max(0, inner_w - filled)

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


def format_status(status: str) -> Text:
    if status == "Ready":
        return Text(status, style="green")
    return Text(status, style="bold red")


def severity_style(value: int) -> str:
    value = max(0, min(100, int(value)))
    if value >= 85:
        return "bold red"
    if value >= 60:
        return "yellow"
    return "green"


def metric_row(label: str, value: int):
    grid = Table.grid(expand=True, padding=(0, 1))
    grid.add_column(width=4)               # Label
    grid.add_column(ratio=1)               # Bar (takes the rest)
    grid.add_column(justify="right", width=4)  # Percent

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


def info_row(pods: int, latency_ms: int):
    grid = Table.grid(expand=True, padding=(0, 1))
    grid.add_column(ratio=1)
    grid.add_column(justify="right")

    grid.add_row(
        Text(f"Pods: {pods}", style="yellow"),
        Text(f"Lat: {latency_ms}ms", style="yellow"),
    )
    return grid


def build_empty_node_panel(title: str = "Empty") -> Panel:
    return Panel(
        Align.center(Text("—", style="grey50"), vertical="middle"),
        title=Text(title, style="grey50"),
        border_style="grey50",
        padding=(0, 1),
    )


def build_node_panel(node: dict) -> Panel:
    title = Text()
    title.append(node["name"], style="bold")
    title.append(" | ")
    title.append(node["role"], style="magenta")
    title.append(" | ")
    title.append_text(format_status(node["status"]))

    content = Group(
        metric_row("CPU", node["cpu"]),
        Text(""),
        metric_row("RAM", node["memory"]),
        Text(""),
        metric_row("DSK", node["disk"]),
        Text(""),
        info_row(node["pods"], node["latency_ms"]),
    )

    return Panel(
        content,
        title=title,
        border_style="blue",
        padding=(0, 1),
    )
