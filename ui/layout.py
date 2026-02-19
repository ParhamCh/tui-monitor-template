from rich.layout import Layout


def build_layout():
    layout = Layout(name="root")

    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="summary", size=5),
        Layout(name="nodes"),
        Layout(name="alerts", size=5),
        Layout(name="footer", size=3),
    )

    return layout
