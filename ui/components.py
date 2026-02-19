from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text


def build_cluster_summary(summary: dict) -> Panel:
    """
    Render cluster summary panel.
    """

    items = [
        Text(f"Nodes: {summary['total_nodes']}", style="cyan"),
        Text(f"Ready: {summary['ready_nodes']}", style="green"),
        Text(f"CPU Avg: {summary['avg_cpu']}%", style="yellow"),
        Text(f"Mem Avg: {summary['avg_memory']}%", style="yellow"),
        Text(f"Pods: {summary['total_pods']}", style="magenta"),
    ]

    return Panel(
        Columns(items, expand=True),
        title="Cluster Summary",
        border_style="green",
    )

