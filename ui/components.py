from rich.panel import Panel
from rich.table import Table


def build_panel(tick: int) -> Panel:
    return Panel(f"Tick: {tick}", title="Status")


def build_status_table() -> Panel:
    table = Table(title="Services")

    table.add_column("Service")
    table.add_column("Status")

    table.add_row("API", "OK")
    table.add_row("DB", "OK")
    table.add_row("Cache", "OK")

    return Panel(table, border_style="yellow")
