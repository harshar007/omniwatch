@echo off
title Omnitrix Watch - Create Desktop Shortcut
chcp 65001 >nul
cd /d "%~dp0"

echo =====================================================================
echo  CREATING OMNITRIX WATCH DESKTOP SHORTCUT
echo =====================================================================
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Create-Desktop-Shortcut.ps1"

pause
