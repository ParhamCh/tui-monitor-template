from rich.console import Console
from rich.panel import Panel

console = Console()

panel = Panel("TUI Monitor Started", title="Status")

console.print(panel)
