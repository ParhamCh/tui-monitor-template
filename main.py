import time
from rich.console import Console
from rich.live import Live
from ui.components import build_panel


console = Console()


with Live(build_panel(0), refresh_per_second=2) as live:
    for i in range(10):
        time.sleep(1)
        live.update(build_panel(i))
