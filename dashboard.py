import time
from rich.live import Live
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
from rich.text import Text
from ui.layout import build_layout
from data.fake_cluster import get_cluster_state
from ui.components import build_cluster_summary
from ui.node_panel import build_node_panel, build_empty_node_panel


def update_node_grid(layout, nodes: list[dict]):
    # Take first 9 nodes for the demo page
    panels = [build_node_panel(n) for n in nodes[:9]]

    # Fill remaining slots with empty panels to keep a strict 3x3 grid
    while len(panels) < 9:
        panels.append(build_empty_node_panel())

    for idx, panel in enumerate(panels):
        layout[f"node_{idx}"].update(panel)


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

    cluster = get_cluster_state()

    layout["summary"].update(build_cluster_summary(cluster["summary"]))
    update_node_grid(layout, cluster["nodes"])


    layout["alerts"].update(
        Panel(Text("Alerts Panel", justify="center"))
    )



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

            layout["header"].update(render_header())
            layout["footer"].update(render_footer(start_time))

            cluster = get_cluster_state()

            layout["summary"].update(build_cluster_summary(cluster["summary"]))
            update_node_grid(layout, cluster["nodes"])

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
