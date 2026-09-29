# CacheCleanerWIN Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a Windows terminal application to safely clear system and browser caches, and find/delete large user folders (>500MB) with a premium UI.

**Architecture:** Python core wrapped by a Windows Batch launcher that handles virtual environment creation and dependency management automatically.

**Tech Stack:** Python 3, Windows Batch (.bat), `rich`, `pytest`

## Global Constraints

- Launcher must handle Windows CRLF `\r\n` strictly.
- Launcher must avoid unescaped parentheses in `if/for` blocks.
- Launcher must use `chcp 65001`.
- Safe cache cleaning: Ignore in-use files, catch `PermissionError`.
- Large folders scanner threshold: 500 MB.
- 2-step confirmation for deleting large folders.
- Show Free Space Before, Free Space After, Total Space Freed.

---

### Task 1: Initialize Project and Launcher

**Files:**
- Create: `iniciar.bat`
- Create: `requirements.txt`
- Create: `src/__init__.py`

**Interfaces:**
- Consumes: N/A
- Produces: Environment ready to execute `src/main.py` with `rich` installed.

- [ ] **Step 1: Write `requirements.txt`**

```text
rich>=13.0.0
pytest>=7.0.0
```

- [ ] **Step 2: Write `iniciar.bat`**

```cmd
@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul
title CacheCleanerWIN
color 0B
cls

echo.
echo  ======================================================================
echo   * CACHECLEANERWIN - INICIALIZANDO *
echo  ======================================================================
echo.
echo  [1/3] Verificando ambiente virtual...
cd /d "%~dp0"

if exist ".venv\Scripts\activate.bat" goto :venv_ok

echo  [2/3] Criando ambiente virtual e instalando dependencias...
python -m venv .venv
call .venv\Scripts\activate.bat
call pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo  [ERRO] Falha ao instalar dependencias.
    pause
    exit /b %errorlevel%
)
goto :run_app

:venv_ok
call .venv\Scripts\activate.bat
echo  [2/3] Ambiente virtual ativado com sucesso!

:run_app
echo.
echo  [3/3] Executando aplicacao...
echo  ----------------------------------------------------------------------
echo.
python src/main.py
pause
```

- [ ] **Step 3: Create src module and commit**

```bash
mkdir src
echo. > src\__init__.py
git add iniciar.bat requirements.txt src\__init__.py
git commit -m "feat: add launcher and requirements"
```

---

### Task 2: Premium UI Helpers

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

---

### Task 3: Cache Cleaner Logic

**Files:**
- Create: `src/cleaner.py`
- Create: `tests/test_cleaner.py`

**Interfaces:**
- Consumes: Python `os`, `shutil`
- Produces: `clean_system_caches(console)`, `get_free_space_mb(drive)`

- [ ] **Step 1: Write the failing test**

```python
import os
from src.cleaner import get_free_space_mb

def test_get_free_space_mb():
    space = get_free_space_mb("C:\\")
    assert space > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_cleaner.py`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**

```python
import os
import shutil
import ctypes

def get_free_space_mb(drive: str) -> float:
    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(drive), None, None, ctypes.pointer(free_bytes))
    return free_bytes.value / (1024 * 1024)

def safe_delete_folder_contents(folder_path: str):
    if not os.path.exists(folder_path):
        return
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except Exception:
            pass # Ignore files in use or permission errors

def clean_system_caches(console):
    paths_to_clean = [
        os.path.expandvars(r"%USERPROFILE%\AppData\Local\Temp"),
        r"C:\Windows\Temp",
        r"C:\Windows\Prefetch",
        r"C:\Windows\SoftwareDistribution\Download",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache\Cache_Data"),
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache\Cache_Data"),
        os.path.expandvars(r"%LOCALAPPDATA%\Mozilla\Firefox\Profiles")
    ]
    
    with console.status("[bold cyan]Limpando caches do sistema e navegadores...") as status:
        for p in paths_to_clean:
            if os.path.exists(p):
                safe_delete_folder_contents(p)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_cleaner.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/cleaner.py tests/test_cleaner.py
git commit -m "feat: add cache cleaner logic"
```

---

### Task 4: Folder Scanner Logic

**Files:**
- Create: `src/scanner.py`
- Create: `tests/test_scanner.py`

**Interfaces:**
- Consumes: Python `os`
- Produces: `find_large_folders(directories, min_mb)`, `get_folder_size_mb(path)`

- [ ] **Step 1: Write the failing test**

```python
import os
from src.scanner import get_folder_size_mb

def test_get_folder_size_mb(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_bytes(b"0" * 1024 * 1024) # 1MB
    size = get_folder_size_mb(str(tmp_path))
    assert 0.9 < size < 1.1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_scanner.py`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**

```python
import os

def get_folder_size_mb(folder_path: str) -> float:
    total_size = 0
    for dirpath, _, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                try:
                    total_size += os.path.getsize(fp)
                except Exception:
                    pass
    return total_size / (1024 * 1024)

def find_large_folders(base_dirs: list[str], min_mb: float = 500.0, console=None) -> list[tuple[str, float]]:
    large_folders = []
    
    status = console.status("[bold yellow]Procurando pastas grandes (>500MB)...") if console else None
    if status: status.start()
    
    try:
        for base_dir in base_dirs:
            if not os.path.exists(base_dir):
                continue
            for item in os.listdir(base_dir):
                item_path = os.path.join(base_dir, item)
                if os.path.isdir(item_path):
                    size = get_folder_size_mb(item_path)
                    if size >= min_mb:
                        large_folders.append((item_path, size))
    finally:
        if status: status.stop()
        
    return sorted(large_folders, key=lambda x: x[1], reverse=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_scanner.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/scanner.py tests/test_scanner.py
git commit -m "feat: add large folder scanner logic"
```

---

### Task 5: Main Orchestration

**Files:**
- Create: `src/main.py`

**Interfaces:**
- Consumes: `src.ui`, `src.cleaner`, `src.scanner`
- Produces: The main executable flow.

- [ ] **Step 1: Write `src/main.py`**

```python
import os
import shutil
from rich.table import Table
from ui import console, show_header, get_space_panel, ask_confirmation, ask_danger_confirmation, print_success, print_error
from cleaner import get_free_space_mb, clean_system_caches
from scanner import find_large_folders

def main():
    show_header()
    drive = os.environ.get("SystemDrive", "C:") + "\\"
    
    space_before = get_free_space_mb(drive)
    
    console.print("\n[bold]Iniciando limpeza de caches segura...[/bold]")
    clean_system_caches(console)
    print_success("Limpeza de caches finalizada!")
    
    base_dirs = [
        os.path.expandvars(r"%USERPROFILE%\Downloads"),
        os.path.expandvars(r"%USERPROFILE%\Documents"),
        os.path.expandvars(r"%USERPROFILE%\Desktop")
    ]
    
    console.print("\n[bold]Verificando pastas grandes de usuário...[/bold]")
    large_folders = find_large_folders(base_dirs, 500.0, console)
    
    if large_folders:
        table = Table(title="Pastas Grandes Encontradas (>500MB)")
        table.add_column("Caminho", style="cyan")
        table.add_column("Tamanho (MB)", justify="right", style="magenta")
        for path, size in large_folders:
            table.add_row(path, f"{size:.2f}")
        console.print(table)
        
        if ask_confirmation("\nDeseja analisar e apagar alguma destas pastas?"):
            for path, size in large_folders:
                if ask_confirmation(f"Deseja apagar '{path}' ({size:.2f} MB)?"):
                    if ask_danger_confirmation(f"Tem certeza ABSOLUTA que deseja EXCLUIR PERMANENTEMENTE '{path}'?"):
                        try:
                            shutil.rmtree(path)
                            print_success(f"Excluído: {path}")
                        except Exception as e:
                            print_error(f"Não foi possível excluir {path}: {e}")
                    else:
                        console.print("[yellow]Exclusão cancelada pelo usuário.[/yellow]")
    else:
        console.print("[green]Nenhuma pasta maior que 500MB encontrada.[/green]")
        
    space_after = get_free_space_mb(drive)
    console.print("\n")
    console.print(get_space_panel(space_before, space_after))
    console.print("[bold green]Processo finalizado![/bold green]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Execução cancelada pelo usuário.[/bold red]")
```

- [ ] **Step 2: Commit**

```bash
git add src/main.py
git commit -m "feat: orchestrate main flow"
```
