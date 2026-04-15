"""
ui/components.py
================
Reusable Rich renderable builders for high-level dashboard sections.

This module currently provides:
    - Cluster summary panel rendering
    - Alerts placeholder panel rendering
    - Small sparkline helper for trend visualization

These builders are intentionally presentation-focused and should not contain
data-fetching logic. All input data must be prepared upstream by the dashboard
or data-provider layers.
"""

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


# ---------------------------------------------------------------------------
# Public renderable builders
# ---------------------------------------------------------------------------


def build_cluster_summary(summary: dict) -> Panel:
    """Build the cluster summary panel.

    The summary is currently rendered as a two-column layout:

    - Left column:
        - Ready node ratio
        - Prometheus health (currently static/mock)
    - Right column:
        - CPU capacity + average usage
        - Memory capacity + average usage

    Args:
        summary: Cluster summary dictionary prepared by the data/dashboard
                 layer.

    Returns:
        A Rich ``Panel`` containing the formatted summary view.
    """
    # ---------------------------------------------------------------------
    # Left block: cluster readiness and service health
    # ---------------------------------------------------------------------
    total_nodes = summary["total_nodes"]
    ready_nodes = summary["ready_nodes"]

    left_line_1 = Text(
        f"Cluster Ready Nodes: {ready_nodes}/{total_nodes}",
        style="cyan",
    )

    # NOTE:
    # Prometheus health is currently static and purely demonstrational.
    # It is not yet sourced from a real service-state provider.
    prom_health = "Healthy"
    prom_style = "green" if prom_health == "Healthy" else "yellow"

    left_line_2 = Text("Prometheus: ", style="grey70")
    left_line_2.append(prom_health, style=prom_style)

    left_block = Group(left_line_1, left_line_2)

    # ---------------------------------------------------------------------
    # Right block: resource capacity, averages, and trends
    # ---------------------------------------------------------------------
    used_cores = summary.get("used_cores", 0)
    total_cores = summary.get("total_cores", 0)
    avg_cpu = summary.get("avg_cpu", 0)
    cpu_trend = summary.get("cpu_trend", [])

    used_mem = summary.get("used_mem_gb", 0)
    total_mem = summary.get("total_mem_gb", 0)
    avg_mem = summary.get("avg_memory", 0)
    mem_trend = summary.get("mem_trend", [])

    right_line_1 = Text(
        f"CPU: {used_cores}/{total_cores} cores | avg {avg_cpu}% ",
        style="yellow",
    )

    right_line_2 = Text(
        f"MEM: {used_mem}/{total_mem} GB | avg {avg_mem}% ",
        style="yellow",
    )

    right_block = Group(right_line_1, right_line_2)

    # ---------------------------------------------------------------------
    # Final layout: two balanced columns inside a single panel
    # ---------------------------------------------------------------------
    grid = Table.grid(expand=True)
    grid.add_column(ratio=1, justify="center")
    grid.add_column(ratio=1, justify="center")
    grid.add_row(left_block, right_block)

    return Panel(grid, title="Cluster Summary", border_style="green")


def build_alerts_placeholder() -> Panel:
    """Build a placeholder alerts panel.

    This panel explicitly communicates that alert handling has not yet been
    implemented, to avoid confusing "no alerts" with "alerts subsystem absent".

    Returns:
        A Rich ``Panel`` containing a centered placeholder message.
    """
    message = Text("Alerts panel is not implemented yet", style="yellow")
    hint = Text("Coming soon", style="grey50")

    content = Align.center(
        Text.assemble(message, "\n", hint),
        vertical="middle",
    )

    return Panel(content, title="Alerts", border_style="yellow")