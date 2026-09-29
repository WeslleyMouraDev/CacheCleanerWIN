# Task 4: Folder Scanner Logic

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
