import time
from collections import deque

from rich.align import Align
from rich.columns import Columns
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from config import GRID_PRESET
from data.fake_cluster import get_cluster_state
from ui.components import build_alerts_placeholder, build_cluster_summary
from ui.layout import build_layout
from ui.node_panel import build_empty_node_panel, build_node_panel


def update_node_grid(layout, nodes: list[dict]) -> None:
    cols = getattr(layout["nodes"], "_grid_cols", 3)
    rows = getattr(layout["nodes"], "_grid_rows", 3)
    capacity = cols * rows

    panels = [build_node_panel(n) for n in nodes[:capacity]]
    while len(panels) < capacity:
        panels.append(build_empty_node_panel())

    for idx, panel in enumerate(panels):
        layout[f"node_{idx}"].update(panel)


def attach_trends_to_summary(cluster: dict, cpu_hist: deque, mem_hist: deque) -> None:
    """
    Update CPU/MEM history buffers and attach trend arrays to cluster summary.
    This keeps the main loop clean and centralizes trend behavior.
    """
    summary = cluster["summary"]

    cpu_hist.append(summary["avg_cpu"])
    mem_hist.append(summary["avg_memory"])

    summary["cpu_trend"] = list(cpu_hist)
    summary["mem_trend"] = list(mem_hist)


def format_uptime(start_time: float) -> str:
    """Return formatted uptime string (HH:MM:SS)."""
    elapsed = int(time.time() - start_time)

    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60

    return f"{hours:02}:{minutes:02}:{seconds:02}"


def render_header() -> Panel:
    left = Text("TUI Monitor", style="bold cyan")

    current_time = time.strftime("%H:%M:%S")
    right = Align.right(Text(f"Time: {current_time}", style="cyan"))

    content = Columns([left, right], expand=True)
    return Panel(content, border_style="cyan")


def render_footer(start_time: float) -> Panel:
    left = Text("Press Ctrl+C to exit", style="grey70")

    uptime = format_uptime(start_time)
    right = Align.right(Text(f"Uptime: {uptime}", style="grey70"))

    content = Columns([left, right], expand=True)
    return Panel(content, border_style="grey50")


def build():
    """Build base layout structure."""
    return build_layout(GRID_PRESET)


def initialize(layout, start_time: float, cpu_hist: deque, mem_hist: deque) -> None:
    """
    Fully initialize all layout sections before Live rendering.
    Prevents initial flicker caused by empty Layout sections.
    """
    layout["header"].update(render_header())
    layout["footer"].update(render_footer(start_time))

    cluster = get_cluster_state()
    attach_trends_to_summary(cluster, cpu_hist, mem_hist)

    layout["summary"].update(build_cluster_summary(cluster["summary"]))
    update_node_grid(layout, cluster["nodes"])

    # Alerts intentionally not implemented yet (placeholder is explicit).
    layout["alerts"].update(build_alerts_placeholder())


def update_frame(layout, start_time: float, cpu_hist: deque, mem_hist: deque) -> None:
    """Update one UI frame."""
    layout["header"].update(render_header())
    layout["footer"].update(render_footer(start_time))

    cluster = get_cluster_state()
    attach_trends_to_summary(cluster, cpu_hist, mem_hist)

    layout["summary"].update(build_cluster_summary(cluster["summary"]))
    update_node_grid(layout, cluster["nodes"])


def run(layout, start_time: float, cpu_hist: deque, mem_hist: deque) -> None:
    """Main live rendering loop."""
    with Live(layout, refresh_per_second=2, screen=True, transient=True):
        while True:
            time.sleep(1)
            update_frame(layout, start_time, cpu_hist, mem_hist)


def shutdown() -> None:
    """Graceful shutdown hook. Reserved for future resource cleanup."""
    return


def run_dashboard() -> None:
    layout = build()

    start_time = time.time()
    cpu_hist = deque(maxlen=10)
    mem_hist = deque(maxlen=10)

    initialize(layout, start_time, cpu_hist, mem_hist)

    try:
        run(layout, start_time, cpu_hist, mem_hist)
    except KeyboardInterrupt:
        shutdown()