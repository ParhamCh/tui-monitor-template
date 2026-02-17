import time
from rich.live import Live
from rich.panel import Panel
from ui.components import build_panel, build_status_table
from ui.layout import build_layout
from data.fake_provider import get_service_status


def run_dashboard():
    layout = build_layout()

    layout["header"].update(
        Panel("TUI Monitor", border_style="cyan")
    )

    layout["footer"].update(
        Panel("Press Ctrl+C to exit", border_style="grey50")
    )

    i = 0

    try:
        with Live(layout, refresh_per_second=2, screen=True, transient=True):
            while True:
                time.sleep(1)

                layout["left"].update(build_panel(i))
                layout["right"].update(
                    build_status_table(get_service_status())
                )

                i += 1

    except KeyboardInterrupt:
        pass
