from rich.layout import Layout


def build_layout():
    layout = Layout(name="root")

    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="summary", size=5),
        Layout(name="nodes", ratio=6),
        Layout(name="alerts", ratio=2),
        Layout(name="footer", size=3),
    )

    # Create a fixed 3x3 grid inside "nodes"
    layout["nodes"].split_column(
        Layout(name="nodes_row_0", ratio=1),
        Layout(name="nodes_row_1", ratio=1),
        Layout(name="nodes_row_2", ratio=1),
    )

    for r in range(3):
        layout[f"nodes_row_{r}"].split_row(
            Layout(name=f"node_{r*3+0}", ratio=1),
            Layout(name=f"node_{r*3+1}", ratio=1),
            Layout(name=f"node_{r*3+2}", ratio=1),
        )

    return layout
