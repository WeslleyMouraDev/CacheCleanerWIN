@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul
title CacheCleanerWIN
color 0B
cls

:: 0. Verificacao de privilegios de Administrador e auto-elevacao
net session >nul 2>&1
if %errorlevel% equ 0 goto :admin_ok

echo.
echo  ======================================================================
echo   * SOLICITANDO PRIVILEGIOS DE ADMINISTRADOR *
echo  ======================================================================
echo.
echo  [!] Solicitando permissao de Administrador para limpeza completa...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process '%~f0' -Verb RunAs"
exit /b

:admin_ok
cd /d "%~dp0"

echo.
echo  ======================================================================
echo   * CACHECLEANERWIN - INICIALIZANDO *
echo  ======================================================================
echo.
echo  [1/3] Verificando ambiente virtual...

if exist ".venv\Scripts\activate.bat" goto :venv_ok

echo  [2/3] Criando ambiente virtual e instalando dependencias...
python -m venv .venv
call .venv\Scripts\activate.bat
call pip install -r requirements.txt
if %errorlevel% neq 0 goto :erro_deps
goto :run_app

:erro_deps
echo.
echo  [ERRO] Falha ao instalar dependencias com pip.
pause
exit /b %errorlevel%

:venv_ok
call .venv\Scripts\activate.bat
echo  [2/3] Ambiente virtual pronto!

:run_app
echo.
echo  [3/3] Executando aplicacao...
echo  ----------------------------------------------------------------------
echo.
python src/main.py
echo.
echo  ----------------------------------------------------------------------
echo   Pressione qualquer tecla para encerrar.
pause >nul
exit /b 0
