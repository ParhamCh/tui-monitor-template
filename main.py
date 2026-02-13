import time
from rich.console import Console
from rich.panel import Panel
from rich.live import Live

console = Console()

with Live(Panel("Starting...", title="Status"), refresh_per_second=2) as live:
    for i in range(10):
        time.sleep(1)
        live.update(
            Panel(f"Tick: {i}", title="Status")
        )
