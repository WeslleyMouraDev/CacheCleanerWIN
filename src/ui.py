from rich.console import Console
from rich.panel import Panel as _RichPanel
from rich.prompt import Confirm

console = Console()

class Panel(_RichPanel):
    def __str__(self) -> str:
        return str(self.renderable)

def show_header():
    console.print(Panel("[bold cyan]CacheCleanerWIN[/bold cyan]\nLimpeza segura de disco.", expand=False))

def get_space_panel(before_mb: float, after_mb: float):
    freed = after_mb - before_mb
    text = f"Antes: {before_mb:.2f} MB\nDepois: {after_mb:.2f} MB\n[bold green]Liberado: {freed:.2f} MB[/bold green]"
    return Panel(text, title="Resumo de Espaço", expand=False)

def ask_confirmation(msg: str) -> bool:
    return Confirm.ask(msg)

def ask_danger_confirmation(msg: str) -> bool:
    return Confirm.ask(f"[bold red]PERIGO:[/bold red] {msg}")

def print_success(msg: str):
    console.print(f"[bold green]OK[/bold green] {msg}")

def print_error(msg: str):
    console.print(f"[bold red]ERRO[/bold red] {msg}")
