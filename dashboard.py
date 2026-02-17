import time
from rich.live import Live
from rich.panel import Panel
from ui.components import build_panel, build_status_table
from ui.layout import build_layout
from data.fake_provider import get_service_status


def build():
    """
    Build base layout structure.
    """
    return build_layout()


def initialize(layout):
    """
    Fully initialize all layout sections before Live rendering.
    Prevents initial flicker caused by empty Layout sections.
    """

    layout["header"].update(
        Panel("TUI Monitor", border_style="cyan")
    )

    layout["footer"].update(
        Panel("Press Ctrl+C to exit", border_style="grey50")
    )

    layout["left"].update(build_panel(0))
    layout["right"].update(build_status_table(get_service_status()))


def run(layout):
    """
    Main live rendering loop.
    """

    i = 0

    with Live(layout, refresh_per_second=2, screen=True, transient=True):
        while True:
            time.sleep(1)

            layout["left"].update(build_panel(i))
            layout["right"].update(
                build_status_table(get_service_status())
            )

            i += 1


def shutdown():
    """
    Graceful shutdown hook.
    Reserved for future resource cleanup.
    """
    pass


def run_dashboard():
    layout = build()
    initialize(layout)

    try:
        run(layout)
    except KeyboardInterrupt:
        shutdown()
