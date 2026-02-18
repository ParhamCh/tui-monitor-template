from rich.panel import Panel
from rich.table import Table
from rich.progress_bar import ProgressBar
from rich.text import Text
from rich.columns import Columns


def format_status(status: str) -> Text:
    if status == "Ready":
        return Text(status, style="green")
    return Text(status, style="bold red")


def metric_row(label: str, value: int):
    """
    Create one metric row with progress bar and percentage.
    """

    bar = ProgressBar(total=100, completed=value)

    percent = Text(f"{value}%", style="bold")

    return Columns(
        [
            Text(f"{label:<6}", style="cyan"),
            bar,
            percent,
        ],
        expand=True,
    )


def build_node_panel(node: dict) -> Panel:
    """
    Render hybrid node panel.
    """

    title = Text()
    title.append(node["name"], style="bold")
    title.append(" | ")
    title.append(node["role"], style="magenta")
    title.append(" | ")
    title.append_text(format_status(node["status"]))

    rows = [
        metric_row("CPU", node["cpu"]),
        metric_row("MEM", node["memory"]),
        metric_row("Disk", node["disk"]),
        Columns(
            [
                Text(f"Pods: {node['pods']}", style="yellow"),
                Text(f"Lat: {node['latency_ms']}ms", style="yellow"),
            ],
            expand=True,
        ),
    ]

    return Panel(
        Columns(rows, expand=True),
        title=title,
        border_style="blue",
    )
