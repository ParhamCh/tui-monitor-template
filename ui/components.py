from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns


def _health_badge(health: str) -> Text:
    styles = {
        "HEALTHY": "bold green",
        "DEGRADED": "bold yellow",
        "CRITICAL": "bold red",
    }
    style = styles.get(health, "bold")
    t = Text(" ")
    t.append(health, style=style)
    t.append(" ")
    return t


def _format_notready(names: list[str], limit: int = 2) -> Text:
    if not names:
        return Text("NotReady: 0", style="green")

    show = names[:limit]
    extra = len(names) - len(show)
    msg = "NotReady: " + ", ".join(show) + (f" +{extra}" if extra > 0 else "")
    return Text(msg, style="bold red")


def build_cluster_summary(summary: dict) -> Panel:
    health = summary.get("health", "HEALTHY")
    total_nodes = summary["total_nodes"]
    ready_nodes = summary["ready_nodes"]

    notready_names = summary.get("notready_names", [])

    alerts_total = summary.get("alerts_total", 0)
    alerts_warn = summary.get("alerts_warn", 0)
    alerts_crit = summary.get("alerts_crit", 0)

    # line 1 (status)
    left_items = [
        _health_badge(health),
        Text(f"Ready: {ready_nodes}/{total_nodes}", style="cyan"),
        _format_notready(notready_names),
    ]
    left = Columns(left_items, expand=True)

    right = Text(
        f"Alerts: {alerts_total} (CRIT:{alerts_crit} WARN:{alerts_warn})",
        style="magenta" if alerts_total else "green",
    )

    # line 2 (resources + capacity + max)
    cpu = Text(
        f"CPU avg {summary.get('avg_cpu', 0)}% | max {summary.get('max_cpu', 0)}% ({summary.get('max_cpu_node', '-')}) | "
        f"{summary.get('used_cores', 0)}/{summary.get('total_cores', 0)} cores",
        style="yellow",
    )
    mem = Text(
        f"MEM avg {summary.get('avg_memory', 0)}% | max {summary.get('max_memory', 0)}% ({summary.get('max_memory_node', '-')}) | "
        f"{summary.get('used_mem_gb', 0)}/{summary.get('total_mem_gb', 0)} GB",
        style="yellow",
    )
    pods = Text(
        f"Pods {summary.get('total_pods', 0)}/{summary.get('pods_capacity', 0)}",
        style="cyan",
    )

    resources = Columns([cpu, mem, pods], expand=True)

    grid = Table.grid(expand=True)
    grid.add_column(ratio=1)
    grid.add_column(justify="right")
    grid.add_row(left, right)
    grid.add_row(resources, Text(""))

    return Panel(grid, title="Cluster Summary", border_style="green")