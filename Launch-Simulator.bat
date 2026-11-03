@echo off
title Omnitrix Alien Simulator // Wear OS Simulator
chcp 65001 >nul
color 0A

echo =====================================================================
echo  ALIEN WATCH // OMNITRIX SIMULATOR
echo  Inspired by Andrej Vujic's Wear OS / Android Omnitrix Simulator
echo =====================================================================
echo.

cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    echo [*] Starting Omnitrix Simulator...
    start "" ".venv\Scripts\python.exe" -m omnitrix_watch.main
    exit /b 0
)

echo [-] Virtual environment not found at .venv\Scripts\python.exe.
echo     Please run Launch-Omnitrix.bat first to set up the environment.
pause
exit /b 1
