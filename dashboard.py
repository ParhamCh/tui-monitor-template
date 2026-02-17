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
        Panel("Uptime: 00:00:00", border_style="grey50")
    )

    layout["left"].update(build_panel(0))
    layout["right"].update(build_status_table(get_service_status()))


def format_uptime(start_time: float) -> str:
    """
    Return formatted uptime string (HH:MM:SS).
    """
    elapsed = int(time.time() - start_time)

    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60

    return f"{hours:02}:{minutes:02}:{seconds:02}"


def run(layout, start_time):
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

            layout["footer"].update(
                Panel(
                    f"Uptime: {format_uptime(start_time)}",
                    border_style="grey50"
                )
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

    start_time = time.time()

    try:
        run(layout, start_time)
    except KeyboardInterrupt:
        shutdown()
