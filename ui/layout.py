from rich.layout import Layout


def build_layout():
    layout = Layout(name="root")
    layout.split_column(
        Layout(name="body")
    )
    return layout
