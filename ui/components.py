from rich.panel import Panel
from rich.table import Table


def build_panel(tick: int) -> Panel:
    return Panel(f"Tick: {tick}", title="Status")


def build_status_table(services: dict) -> Panel:
    table = Table(title="Services")

    table.add_column("Service")
    table.add_column("Status")

    for name, status in services.items():
        table.add_row(name, status)

    return Panel(table, border_style="yellow")
