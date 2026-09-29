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
    try:
        items = os.listdir(folder_path)
    except (PermissionError, OSError):
        return
    for item in items:
        item_path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except Exception:
            pass  # Ignore files in use or permission errors

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
