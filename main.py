import time
from rich.console import Console
from rich.live import Live
from ui.components import build_panel
from ui.layout import build_layout


console = Console()

layout = build_layout()
layout["body"].update(build_panel(0))


with Live(layout, refresh_per_second=2) as live:
    for i in range(10):
        time.sleep(1)
        layout["body"].update(build_panel(i))
