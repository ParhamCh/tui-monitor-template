"""
ui/components.py
================
Reusable Rich renderable builders for high-level dashboard sections.

This module currently provides:
    - Cluster summary panel rendering
    - Alerts panel rendering

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
# Constants
# ---------------------------------------------------------------------------

ALERT_VISIBLE_LINES: int = 4

HEALTH_STYLES: dict[str, str] = {
    "HEALTHY": "green",
    "DEGRADED": "yellow",
    "CRITICAL": "bold red",
}

ALERT_SEVERITY_STYLES: dict[str, str] = {
    "WARN": "yellow",
    "CRIT": "bold red",
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _health_style(health: str) -> str:
    """Return display style for a cluster health label."""
    return HEALTH_STYLES.get(health, "white")


def _alert_severity_style(severity: str) -> str:
    """Return display style for an alert severity label."""
    return ALERT_SEVERITY_STYLES.get(severity, "white")


def _alerts_total_style(alerts_total: int, alerts_crit: int) -> str:
    """Return display style for the summary alert count."""
    if alerts_crit:
        return "bold red"
    if alerts_total:
        return "yellow"
    return "green"


# ---------------------------------------------------------------------------
# Public renderable builders
# ---------------------------------------------------------------------------


def build_cluster_summary(summary: dict) -> Panel:
    """Build the cluster summary panel.

    The summary is currently rendered as a two-column layout:

    - Left column:
        - Ready node ratio
        - Cluster health and alert counts
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

    health = summary.get("health", "UNKNOWN")
    alerts_total = summary.get("alerts_total", 0)
    alerts_warn = summary.get("alerts_warn", 0)
    alerts_crit = summary.get("alerts_crit", 0)

    left_line_2 = Text("Health: ", style="grey70")
    left_line_2.append(health, style=_health_style(health))
    left_line_2.append(" | Alerts: ", style="grey70")
    left_line_2.append(
        str(alerts_total),
        style=_alerts_total_style(alerts_total, alerts_crit),
    )
    left_line_2.append(f" ({alerts_warn}W/{alerts_crit}C)", style="grey70")

    left_block = Group(left_line_1, left_line_2)

    # ---------------------------------------------------------------------
    # Right block: resource capacity, averages, and trends
    # ---------------------------------------------------------------------
    used_cores = summary.get("used_cores", 0)
    total_cores = summary.get("total_cores", 0)
    avg_cpu = summary.get("avg_cpu", 0)

    used_mem = summary.get("used_mem_gb", 0)
    total_mem = summary.get("total_mem_gb", 0)
    avg_mem = summary.get("avg_memory", 0)

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

    return Panel(grid, title="Cluster Summary", border_style=_health_style(health))


def build_alerts_panel(alerts: list[dict]) -> Panel:
    """Build the alerts panel from alert dictionaries.

    Args:
        alerts: Alert dictionaries prepared by the data layer.

    Returns:
        A Rich ``Panel`` containing current alerts or a clear empty state.
    """
    if not alerts:
        content = Align.center(
            Text("No active alerts", style="green"),
            vertical="middle",
        )
        return Panel(content, title="Alerts", border_style="green")

    visible_alerts = alerts[:ALERT_VISIBLE_LINES]
    hidden_count = len(alerts) - len(visible_alerts)
    lines: list[Text] = []

    for alert in visible_alerts:
        severity = alert["severity"]
        line = Text()
        line.append(f"{severity:<4}", style=_alert_severity_style(severity))
        line.append("  ")
        line.append(alert["node"], style="cyan")
        line.append("  ")
        line.append(alert["message"], style="white")
        lines.append(line)

    if hidden_count > 0:
        lines[-1] = Text(f"+{hidden_count} more alerts", style="grey70")

    return Panel(
        Group(*lines),
        title="Alerts",
        border_style="bold red" if any(alert["severity"] == "CRIT" for alert in alerts) else "yellow",
    )
