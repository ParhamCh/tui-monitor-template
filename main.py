import time
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from ui.components import build_panel
from ui.layout import build_layout


console = Console()

layout = build_layout()

layout["header"].update(
    Panel("TUI Monitor", border_style="cyan")
)

layout["body"].update(build_panel(0))

layout["footer"].update(
    Panel("Press Ctrl+C to exit", border_style="grey50")
)


with Live(layout, refresh_per_second=2) as live:
    for i in range(10):
        time.sleep(1)
        layout["body"].update(build_panel(i))
