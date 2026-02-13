from rich.panel import Panel


def build_panel(tick: int) -> Panel:
    return Panel(f"Tick: {tick}", title="Status")
