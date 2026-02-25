from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.console import Group
from rich.align import Align


def _spark(values: list[int]) -> Text:
    blocks = "▁▂▃▄▅▆▇█"
    if not values:
        return Text("")

    out = Text()
    for v in values[-10:]:
        v = max(0, min(100, int(v)))
        idx = int(round((len(blocks) - 1) * v / 100))
        out.append(blocks[idx], style="cyan")
    return out


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
    # --- left (2 lines) ---
    total_nodes = summary["total_nodes"]
    ready_nodes = summary["ready_nodes"]

    left_line1 = Text(f"Cluster Ready Nodes: {ready_nodes}/{total_nodes}", style="cyan")

    # Example service health (you can wire real ones later)
    # If you already have alerts or health, you can base this on them.
    prom_health = "Healthy"
    prom_style = "green" if prom_health == "Healthy" else "yellow"
    left_line2 = Text("Prometheus: ", style="grey70")
    left_line2.append(prom_health, style=prom_style)

    left_block = Group(left_line1, left_line2)

    # --- right (2 lines) ---
    # capacities
    used_cores = summary.get("used_cores", 0)
    total_cores = summary.get("total_cores", 0)
    avg_cpu = summary.get("avg_cpu", 0)
    cpu_trend = summary.get("cpu_trend", [])

    used_mem = summary.get("used_mem_gb", 0)
    total_mem = summary.get("total_mem_gb", 0)
    avg_mem = summary.get("avg_memory", 0)
    mem_trend = summary.get("mem_trend", [])

    # line 1: CPU
    right_line1 = Text(f"CPU: {used_cores}/{total_cores} cores | avg {avg_cpu}% ", style="yellow")
    right_line1.append_text(_spark(cpu_trend))

    # line 2: MEM
    right_line2 = Text(f"MEM: {used_mem}/{total_mem} GB   | avg {avg_mem}% ", style="yellow")
    right_line2.append_text(_spark(mem_trend))

    right_block = Group(right_line1, right_line2)

    # --- two-column layout (fixed and clean) ---
    grid = Table.grid(expand=True)
    grid.add_column(ratio=1, justify="center")
    grid.add_column(ratio=1, justify="center")
    grid.add_row(left_block, right_block)

    return Panel(grid, title="Cluster Summary", border_style="green")


def build_alerts_placeholder() -> Panel:
    message = Text("Alerts panel is not implemented yet", style="yellow")
    hint = Text("Coming soon", style="grey50")
    content = Align.center(Text.assemble(message, "\n", hint), vertical="middle")
    return Panel(content, title="Alerts", border_style="yellow")
