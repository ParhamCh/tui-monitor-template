"""
dashboard.py
============
Entry point for the TUI cluster-monitoring dashboard.

This module is responsible for the full lifecycle of the dashboard:
    - Building the layout structure
    - Initializing all UI sections before rendering begins
    - Running the main live-update loop
    - Graceful shutdown

Typical usage::

    from dashboard import run_dashboard
    run_dashboard()
"""

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


# ---------------------------------------------------------------------------
# Context helpers
# ---------------------------------------------------------------------------


def create_context() -> dict:
    """Create and return the initial runtime context for the dashboard.

    The context dictionary is a lightweight container for mutable state that
    must survive across frames but does not belong to any single component.

    Returns:
        A dictionary with the following keys:

        - ``start_time`` (*float*): ``time.time()`` at dashboard launch,
          used to compute uptime.
        - ``cpu_hist`` (*deque[float]*): Rolling window of average-CPU
          samples, capped at :data:`TREND_HISTORY_SIZE` entries.
        - ``mem_hist`` (*deque[float]*): Rolling window of average-memory
          samples, capped at :data:`TREND_HISTORY_SIZE` entries.
    """
    return {
        "start_time": time.time(),
        "cpu_hist": deque(maxlen=10),
        "mem_hist": deque(maxlen=10),
    }


# ---------------------------------------------------------------------------
# Layout update helpers
# ---------------------------------------------------------------------------


def update_node_grid(layout, nodes: list[dict]) -> None:
    """Populate the node grid section of the layout with live node data.

    The grid dimensions are read from metadata attributes set by
    :func:`ui.layout.build_layout`.  If those attributes are absent the
    module-level defaults :data:`DEFAULT_GRID_COLS` / :data:`DEFAULT_GRID_ROWS`
    are used as a fallback.

    Nodes that exceed the grid capacity are silently dropped; a warning is
    logged so operators can detect mismatches between cluster size and
    configured grid preset.

    Args:
        layout: The Rich ``Layout`` object that owns all named sections.
        nodes:  List of node-state dictionaries returned by
                :func:`data.fake_cluster.get_cluster_state`.
    """
    cols = getattr(layout["nodes"], "_grid_cols", 3)
    rows = getattr(layout["nodes"], "_grid_rows", 3)
    capacity = cols * rows

    panels = [build_node_panel(n) for n in nodes[:capacity]]
    while len(panels) < capacity:
        panels.append(build_empty_node_panel())

    for idx, panel in enumerate(panels):
        layout[f"node_{idx}"].update(panel)


def attach_trends_to_summary(
    cluster: dict,
    cpu_hist: deque,
    mem_hist: deque
) -> None:
    """Append the latest CPU/memory samples and attach trend lists to *cluster*.

    Mutates ``cluster["summary"]`` in-place by adding two keys:
    ``cpu_trend`` and ``mem_trend``, each a plain :class:`list` snapshot of
    the corresponding rolling-window deque.

    Keeping this logic here (rather than inline in the update loop) means the
    main loop stays thin and the trend behaviour is easy to unit-test in
    isolation.

    Args:
        cluster:  Cluster-state dictionary as returned by
                  :func:`data.fake_cluster.get_cluster_state`.
        cpu_hist: Mutable deque used as a rolling CPU sample buffer.
        mem_hist: Mutable deque used as a rolling memory sample buffer.
    """
    summary = cluster["summary"]

    cpu_hist.append(summary["avg_cpu"])
    mem_hist.append(summary["avg_memory"])

    # Expose immutable snapshots so downstream code cannot accidentally
    # mutate the live buffers.
    summary["cpu_trend"] = list(cpu_hist)
    summary["mem_trend"] = list(mem_hist)


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------


def format_uptime(start_time: float) -> str:
    """Convert an epoch *start_time* to a human-readable uptime string.

    Args:
        start_time: The ``time.time()`` value recorded when the dashboard
                    was launched.

    Returns:
        A zero-padded ``"HH:MM:SS"`` string representing elapsed wall time.

    Example::

        >>> format_uptime(time.time() - 3725)
        '01:02:05'
    """
    elapsed: int = int(time.time() - start_time)
    hours, remainder = divmod(elapsed, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


# ---------------------------------------------------------------------------
# Renderable builders
# ---------------------------------------------------------------------------


def render_header() -> Panel:
    """Build and return the top header panel for the current tick.

    The header shows the application title on the left and the current
    wall-clock time on the right.

    Returns:
        A :class:`rich.panel.Panel` ready to be passed to ``Layout.update()``.
    """
    left = Text("TUI Monitor", style="bold cyan")
    right = Align.right(Text(f"Time: {time.strftime('%H:%M:%S')}", style="cyan"))
    content = Columns([left, right], expand=True)
    return Panel(content, border_style="cyan")


def render_footer(start_time: float) -> Panel:
    """Build and return the bottom footer panel showing uptime and exit hint.

    Args:
        start_time: Dashboard launch epoch used to compute the uptime string.

    Returns:
        A :class:`rich.panel.Panel` ready to be passed to ``Layout.update()``.
    """
    left = Text("Press Ctrl+C to exit", style="grey70")
    right = Align.right(Text(f"Uptime: {format_uptime(start_time)}", style="grey70"))
    content = Columns([left, right], expand=True)
    return Panel(content, border_style="grey50")


# ---------------------------------------------------------------------------
# Dashboard lifecycle
# ---------------------------------------------------------------------------


def build():
    """Build and return the base layout structure.

    This is deliberately separated from :func:`initialize` so that the layout
    tree can be constructed without triggering any I/O or data fetches.

    Returns:
        A Rich ``Layout`` instance pre-configured with the preset defined in
        :data:`config.GRID_PRESET`.
    """
    return build_layout(GRID_PRESET)


def initialize(layout) -> dict:
    """Fully populate every layout section before the Live renderer starts.

    Pre-rendering all sections prevents the initial frame from showing blank
    or partially-drawn panels (visual flicker).

    Args:
        layout: The Rich ``Layout`` returned by :func:`build`.

    Returns:
        The runtime context dictionary created by :func:`create_context`.
    """
    ctx = create_context()

    layout["header"].update(render_header())
    layout["footer"].update(render_footer(ctx["start_time"]))

    cluster = get_cluster_state()
    attach_trends_to_summary(cluster, ctx["cpu_hist"], ctx["mem_hist"])

    layout["summary"].update(build_cluster_summary(cluster["summary"]))
    update_node_grid(layout, cluster["nodes"])

    # Alerts intentionally not implemented yet (placeholder is explicit).
    layout["alerts"].update(build_alerts_placeholder())

    return ctx


def update_frame(layout, ctx: dict) -> None:
    """Fetch fresh data and redraw all dynamic layout sections.

    Called once per :data:`UPDATE_INTERVAL` inside the main render loop.
    Static sections (e.g. alerts placeholder) are intentionally excluded to
    avoid unnecessary redraws.

    Args:
        layout: The active Rich ``Layout`` being rendered by ``Live``.
        ctx:    The runtime context dictionary produced by :func:`create_context`.
    """
    layout["header"].update(render_header())
    layout["footer"].update(render_footer(ctx["start_time"]))

    cluster = get_cluster_state()
    attach_trends_to_summary(cluster, ctx["cpu_hist"], ctx["mem_hist"])

    layout["summary"].update(build_cluster_summary(cluster["summary"]))
    update_node_grid(layout, cluster["nodes"])


def run(layout, ctx: dict) -> None:
    """Start the blocking Live render loop.

    Renders *layout* at :data:`REFRESH_PER_SECOND` and calls
    :func:`update_frame` every :data:`UPDATE_INTERVAL` seconds.
    Both constants are derived from a single value to guarantee they stay
    in sync.

    Args:
        layout: The fully-initialised Rich ``Layout``.
        ctx:    The runtime context dictionary.

    Raises:
        KeyboardInterrupt: Propagated to the caller (:func:`run_dashboard`)
                           so shutdown logic can be executed there.
    """
    with Live(layout, refresh_per_second=1, screen=True, transient=True):
        while True:
            time.sleep(1)
            update_frame(layout, ctx)


def shutdown() -> None:
    """Execute graceful shutdown tasks before the process exits.

    Currently limited to flushing log handlers.  Add resource-cleanup logic
    (e.g. closing network connections, persisting state) here as the
    application grows.
    """
    return


def run_dashboard() -> None:
    """Build, initialise, and run the TUI dashboard until interrupted.

    This is the single public entry-point for the module.  It wires together
    the full lifecycle::

        build() → initialize() → run() → shutdown()

    A :exc:`KeyboardInterrupt` (Ctrl-C) triggers a clean exit via
    :func:`shutdown` without printing a traceback.
    """
    layout = build()
    ctx = initialize(layout)

    try:
        run(layout, ctx)
    except KeyboardInterrupt:
        shutdown()
