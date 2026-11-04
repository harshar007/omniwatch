@echo off
title Omnitrix Web Simulator Launcher
chcp 65001 >nul
color 0A

echo =====================================================================
echo  OMNITRIX WATCH // LAUNCHING WEB BROWSER SIMULATOR
echo =====================================================================
echo.

cd /d "%~dp0..\.."

echo [*] Opening web/index.html in default web browser...
start "" "web\index.html"

echo [✓] Web simulator launched!
timeout /t 2 >nul
