from rich.layout import Layout


def build_layout():
    layout = Layout(name="root")

    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="summary", size=3),
        Layout(name="nodes", ratio=4),
        Layout(name="alerts", ratio=1),
        Layout(name="footer", size=3),
    )

    return layout
