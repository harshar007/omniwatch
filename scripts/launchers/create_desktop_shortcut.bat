@echo off
title Create Omnitrix Desktop Shortcut
chcp 65001 >nul
color 0A

echo [*] Generating desktop shortcut...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0create_desktop_shortcut.ps1"
if %errorlevel% equ 0 (
    echo [✓] Shortcut successfully placed on your Desktop!
) else (
    echo [-] Failed to create desktop shortcut.
)
timeout /t 3 >nul
