# Task 2: Premium UI Helpers

**Files:**
- Create: `src/ui.py`
- Create: `tests/test_ui.py`

**Interfaces:**
- Consumes: `rich` library.
- Produces: `show_header()`, `get_space_panel(before, after)`, `ask_confirmation(msg)`, `ask_danger_confirmation(msg)`.

- [ ] **Step 1: Write the failing test**

```python
import pytest
from src.ui import get_space_panel

def test_get_space_panel():
    panel = get_space_panel(1000, 1500)
    assert "Antes: 1000" in str(panel)
    assert "Liberado: 500" in str(panel)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_ui.py`
Expected: FAIL (file or function not defined)

- [ ] **Step 3: Write minimal implementation**

```python
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table

console = Console()

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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_ui.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/ui.py tests/test_ui.py
git commit -m "feat: add ui helpers"
```
