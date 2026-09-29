# CacheCleanerWIN - Design Specification

## 1. Overview
CacheCleanerWIN is a Windows terminal application designed to safely clear system and browser caches to free up disk space. It features a premium terminal UI, automatic virtual environment setup via a Windows Batch launcher, and an interactive module to find and delete large user folders with a strict 2-step confirmation process.

## 2. Architecture & Tech Stack
- **Launcher**: Windows Batch (`.bat`) script implementing safe and robust initialization (handling CRLF, `chcp 65001`, robust `if/for` structures avoiding unescaped parentheses).
- **Core Logic**: Python 3.
- **Dependencies**: 
  - `rich` (for premium terminal UI: panels, spinners, progress bars, colors).
  - `send2trash` (optional, but for this project we will do permanent deletion via `shutil` with user double-confirmation).
- **Dependency Management**: The `.bat` launcher automatically creates a hidden `.venv`, installs `rich`, and executes the Python script.

## 3. Core Features & Workflows

### 3.1 Initialization & Space Metrics
- Record the current free space on the target drive (usually `C:\`).
- Display a rich, premium splash screen.

### 3.2 Safe Cache Cleaning (Default Process)
Automatically and silently attempts to clean the following paths (ignoring files currently in use):
- **System Caches**: 
  - User Temp (`%USERPROFILE%\AppData\Local\Temp`)
  - Windows Temp (`C:\Windows\Temp`)
  - Prefetch (`C:\Windows\Prefetch`) - *requires admin privileges, skip gracefully if not available*.
- **Windows Update**:
  - SoftwareDistribution Download (`C:\Windows\SoftwareDistribution\Download`).
- **Browser Caches**:
  - Chrome: `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache`
  - Edge: `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache`
  - Firefox: `%LOCALAPPDATA%\Mozilla\Firefox\Profiles\*\cache2`

*UI*: Shows a loading spinner and updates the status for each cache being cleaned.

### 3.3 Large Folder Scanner
- **Target Directories**: `%USERPROFILE%\Downloads`, `%USERPROFILE%\Documents`, `%USERPROFILE%\Desktop`.
- **Threshold**: Folders taking > 500 MB of space.
- **Process**:
  1. Scan and calculate folder sizes (displaying a progress bar/spinner).
  2. List the large folders found using a `rich` Table.
  3. Prompt the user: "Do you want to review and delete any of these folders? (Y/N)".
  4. If Yes, iterate through the list. For each folder, prompt for deletion.
  5. **Security Gate**: If the user says Yes to delete a folder, prompt *again* with a red warning: "Are you absolutely sure you want to permanently delete [Folder Name]? This cannot be undone. (Y/N)".

### 3.4 Summary Report
At the end of the execution, calculate the final free space on the drive and display a `rich` Panel with:
- Free Space Before
- Free Space After
- Total Space Freed
- A success/goodbye message.

## 4. Error Handling & Edge Cases
- **Permissions**: System files like `Prefetch` often require Admin rights. The script will use `try/except` blocks (like `PermissionError`) to skip locked or protected files gracefully without halting the application.
- **Python not found**: The `.bat` launcher will check if `python --version` exists and show a friendly error if not installed.
- **Interrupts**: Catch `KeyboardInterrupt` (Ctrl+C) to exit cleanly without dumping stack traces.

## 5. File Structure
```text
CacheCleanerWIN/
├── iniciar.bat            # The robust launcher
├── requirements.txt       # Contains 'rich'
├── src/
│   ├── main.py            # Python entrypoint
│   ├── cleaner.py         # Logic for system/browser cache cleaning
│   ├── scanner.py         # Logic for scanning >500MB folders
│   └── ui.py              # Rich console instances and helpers
└── docs/
    └── superpowers/
        └── specs/
            └── 2026-09-29-cachecleanerwin-design.md
```
