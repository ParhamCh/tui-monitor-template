import time
from rich.live import Live
from rich.panel import Panel
from ui.components import build_panel, build_status_table
from ui.layout import build_layout
from data.fake_provider import get_service_status


def initialize_layout(layout):
    """
    Fully initialize all layout sections before starting Live rendering.

    Why this is required:
    ---------------------
    Rich's Live performs an immediate render on entry.
    If any Layout section has no renderable assigned,
    Rich will display its default object representation
    (e.g. Layout(name='left')).

    To prevent flicker and ensure a clean first frame,
    every section must be populated before entering Live.
    """

    layout["header"].update(
        Panel("TUI Monitor", border_style="cyan")
    )

    layout["footer"].update(
        Panel("Press Ctrl+C to exit", border_style="grey50")
    )

    layout["left"].update(build_panel(0))
    layout["right"].update(build_status_table(get_service_status()))


def run_dashboard():

    layout = build_layout()

    # Phase 1: Initial layout population (mandatory before Live)
    initialize_layout(layout)

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
