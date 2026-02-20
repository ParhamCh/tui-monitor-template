from rich.layout import Layout

_GRID_PRESETS = {
    "2x2": (2, 2),
    "3x2": (3, 2),
    "3x3": (3, 3),
}


def build_layout(grid_preset: str = "3x3") -> Layout:
    cols, rows = _GRID_PRESETS.get(grid_preset, (3, 3))

    layout = Layout(name="root")
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="summary", size=5),
        Layout(name="nodes", ratio=6),
        Layout(name="alerts", ratio=2),
        Layout(name="footer", size=3),
    )

    # build grid inside nodes
    layout["nodes"].split_column(
        *[Layout(name=f"nodes_row_{r}", ratio=1) for r in range(rows)]
    )

    for r in range(rows):
        layout[f"nodes_row_{r}"].split_row(
            *[Layout(name=f"node_{r*cols+c}", ratio=1) for c in range(cols)]
        )

    # store meta (helpful for updater)
    layout["nodes"]._grid_cols = cols  # simple internal metadata
    layout["nodes"]._grid_rows = rows

    return layout