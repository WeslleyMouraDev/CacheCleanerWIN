# Task 5: Main Orchestration

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
