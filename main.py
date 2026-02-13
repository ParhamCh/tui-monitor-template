import time
from rich.console import Console
from rich.panel import Panel
from rich.live import Live


console = Console()


def build_panel(tick: int) -> Panel:
    return Panel(f"Tick: {tick}", title="Status")


with Live(build_panel(0), refresh_per_second=2) as live:
    for i in range(10):
        time.sleep(1)
        live.update(build_panel(i))
