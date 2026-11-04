@echo off
title Omnitrix Alien Simulator // Wear OS Simulator
chcp 65001 >nul
color 0A

echo =====================================================================
echo  ALIEN WATCH // OMNITRIX SIMULATOR
echo  Inspired by Andrej Vujic's Wear OS / Android Omnitrix Simulator
echo =====================================================================
echo.

cd /d "%~dp0..\.."

if exist ".venv\Scripts\python.exe" (
    echo [*] Starting Omnitrix Simulator via virtual environment...
    start "" ".venv\Scripts\python.exe" -m omnitrix_watch.main
    exit /b 0
)

:: If .venv doesn't exist, try system python directly
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo [*] Starting Omnitrix Simulator via system Python...
    start "" python -m omnitrix_watch.main
    exit /b 0
)

echo [-] Python not found on system PATH and .venv not initialized.
echo     Please run scripts\launchers\launch_gui.bat first.
pause
exit /b 1
