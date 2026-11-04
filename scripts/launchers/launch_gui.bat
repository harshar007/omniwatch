@echo off
title Omnitrix Watch Companion // OS Launcher
chcp 65001 >nul
color 0A

echo =====================================================================
echo  OMNITRIX WATCH // INITIALIZING COMPANION OS
echo =====================================================================
echo.

:: Move to project root
cd /d "%~dp0..\.."

:: 1. Check if virtual environment exists
if exist ".venv\Scripts\python.exe" (
    echo [*] Found local Python virtual environment in .venv
    goto :ACTIVATE_AND_LAUNCH
)

:: 2. If no virtual environment, check for system Python
echo [!] Local .venv not found. Searching for system Python 3...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [-] ERROR: Python 3 is not found on your system PATH!
    echo     Please install Python 3.11+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo [*] Initializing virtual environment in .venv...
python -m venv .venv
if %errorlevel% neq 0 (
    echo [!] Warning: Failed to create .venv. Falling back to system python.
    python -m omnitrix_watch.main
    exit /b %errorlevel%
)

:ACTIVATE_AND_LAUNCH
echo [*] Activating environment and verifying dependencies...
call ".venv\Scripts\activate.bat"

:: Quick check if bleak is installed
python -c "import bleak" >nul 2>nul
if %errorlevel% neq 0 (
    echo [*] Installing required BLE dependencies (bleak)...
    python -m pip install -e .
)

echo [*] Launching Omnitrix Watch GUI...
start "" ".venv\Scripts\pythonw.exe" -m omnitrix_watch.main
if %errorlevel% neq 0 (
    echo [*] Running fallback launcher with console...
    python -m omnitrix_watch.main
)

echo.
echo [✓] Omnitrix Watch started successfully.
echo     You can close this window now.
timeout /t 3 >nul
