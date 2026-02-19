from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.text import Text
from rich.columns import Columns
from rich.console import Group
from rich.align import Align


def format_status(status: str) -> Text:
    if status == "Ready":
        return Text(status, style="green")
    return Text(status, style="bold red")


def metric_row(label: str, value: int):
    bar = ProgressBar(total=100, completed=value)
    percent = Text(f"{value:>3}%", style="bold")

    # You can keep expand=True here because the Layout cell controls width.
    return Columns(
        [
            Text(f"{label:<4}", style="cyan"),
            bar,
            Align.right(percent),
        ],
        expand=True,
    )


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

    info_row = Columns(
        [
            Text(f"Pods: {node['pods']}", style="yellow"),
            Align.right(Text(f"Lat: {node['latency_ms']}ms", style="yellow")),
        ],
        expand=True,
    )

    content = Group(
        metric_row("CPU", node["cpu"]),
        metric_row("MEM", node["memory"]),
        metric_row("DSK", node["disk"]),
        info_row,
    )

    return Panel(
        content,
        title=title,
        border_style="blue",
        padding=(0, 1),
    )
