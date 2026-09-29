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
    if status:
        status.start()

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
        if status:
            status.stop()

    return sorted(large_folders, key=lambda x: x[1], reverse=True)
