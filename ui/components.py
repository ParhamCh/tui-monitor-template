from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def format_status(status: str) -> Text:
    """
    Return color-coded Text object based on service status.
    """

    if status == "OK":
        return Text(status, style="green")
    elif status == "WARN":
        return Text(status, style="yellow")
    elif status == "DOWN":
        return Text(status, style="bold red")
    else:
        return Text(status)


def build_panel(tick: int) -> Panel:
    return Panel(f"Tick: {tick}", title="Status")


def build_status_table(services: dict) -> Panel:
    table = Table(title="Services")

    table.add_column("Service")
    table.add_column("Status")

    for name, status in services.items():
        table.add_row(name, format_status(status))

    return Panel(table, border_style="yellow")

