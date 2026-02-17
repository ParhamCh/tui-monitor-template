from rich.layout import Layout


def build_layout():
    layout = Layout(name="root")

    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3),
    )

    layout["body"].split_row(
        Layout(name="left"),
        Layout(name="right"),
    )

    return layout
