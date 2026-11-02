<#
.SYNOPSIS
    One-click PowerShell launcher for Omnitrix Watch Companion OS.
.DESCRIPTION
    Automatically ensures virtual environment, dependencies, and launches the Tkinter UI.
#>

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "Omnitrix Watch Companion // OS v0.1.0"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "=====================================================================" -ForegroundColor Green
Write-Host "  OMNITRIX WATCH // INITIALIZING COMPANION OS" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host ""

$VenvPython = Join-Path $ScriptDir ".venv\Scripts\python.exe"
$VenvPythonw = Join-Path $ScriptDir ".venv\Scripts\pythonw.exe"
$ActivateScript = Join-Path $ScriptDir ".venv\Scripts\Activate.ps1"

if (-not (Test-Path $VenvPython)) {
    Write-Host "[!] Local .venv environment not found. Searching for system Python..." -ForegroundColor Yellow
    $SystemPython = Get-Command python -ErrorAction SilentlyContinue
    if (-not $SystemPython) {
        Write-Host "[-] ERROR: Python is not installed on your system." -ForegroundColor Red
        Write-Host "    Download Python 3.11+ at https://www.python.org/" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "[*] Creating virtual environment (.venv)..." -ForegroundColor Cyan
    & python -m venv .venv
}

Write-Host "[*] Activating virtual environment..." -ForegroundColor Cyan
& $ActivateScript

# Verify dependencies
$BleakCheck = & $VenvPython -c "import bleak; print('ok')" 2>$null
if ($BleakCheck -ne "ok") {
    Write-Host "[*] Installing required packages..." -ForegroundColor Cyan
    & $VenvPython -m pip install -e .
}

Write-Host "[*] Launching Omnitrix GUI..." -ForegroundColor Green
if (Test-Path $VenvPythonw) {
    Start-Process -FilePath $VenvPythonw -ArgumentList "-m", "omnitrix_watch.main"
} else {
    Start-Process -FilePath $VenvPython -ArgumentList "-m", "omnitrix_watch.main"
}

Write-Host "[✓] Omnitrix Watch is active." -ForegroundColor Green
Start-Sleep -Seconds 2
