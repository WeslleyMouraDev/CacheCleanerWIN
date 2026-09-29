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
