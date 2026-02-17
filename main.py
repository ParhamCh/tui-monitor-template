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

layout["left"].update(build_panel(0))

layout["right"].update(
    Panel("Right Panel", border_style="yellow")
)

layout["footer"].update(
    Panel("Press Ctrl+C to exit", border_style="grey50")
)


try:
    with Live(layout, refresh_per_second=2, screen=True, transient=True) as live:
        i = 0
        while True:
            time.sleep(1)
            layout["body"].update(build_panel(i))
            i += 1

except KeyboardInterrupt:
    pass
