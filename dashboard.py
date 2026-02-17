import time
from rich.live import Live
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
from rich.text import Text
from ui.layout import build_layout
from ui.components import build_status_table, build_metrics_table
from data.fake_provider import get_service_status
from data.fake_metrics import get_metrics



def render_header() -> Panel:
    """
    Render header with structured two-column layout:
    - Left: static title
    - Right: dynamic current time
    """

    left = Text("TUI Monitor", style="bold cyan")

    current_time = time.strftime("%H:%M:%S")
    right = Align.right(
        Text(f"Time: {current_time}", style="cyan")
    )

    content = Columns([left, right], expand=True)

    return Panel(content, border_style="cyan")


def render_footer(start_time: float) -> Panel:
    """
    Render footer with structured two-column layout:
    - Left: static hint
    - Right: dynamic uptime
    """

    left = Text("Press Ctrl+C to exit", style="grey70")

    uptime = format_uptime(start_time)
    right = Align.right(
        Text(f"Uptime: {uptime}", style="grey70")
    )

    content = Columns([left, right], expand=True)

    return Panel(content, border_style="grey50")


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

    layout["header"].update(render_header())
    layout["footer"].update(render_footer(time.time()))

    layout["left"].update(build_metrics_table(get_metrics()))
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

            layout["left"].update(
                build_metrics_table(get_metrics())
            )
            layout["right"].update(
                build_status_table(get_service_status())
            )

            layout["header"].update(render_header())
            layout["footer"].update(render_footer(start_time))

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
