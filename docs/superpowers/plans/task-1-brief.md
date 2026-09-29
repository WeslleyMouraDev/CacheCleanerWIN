# Task 1: Initialize Project and Launcher

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
