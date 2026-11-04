<#
.SYNOPSIS
    PowerShell launcher for Omnitrix Watch Companion OS.
.DESCRIPTION
    Validates Python environment, virtual environment, dependencies, and launches the UI.
#>

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "Omnitrix Watch Companion // OS Launcher"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $ProjectRoot

Write-Host "=====================================================================" -ForegroundColor Green
Write-Host "  OMNITRIX WATCH // INITIALIZING COMPANION OS" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host ""

$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$VenvPythonw = Join-Path $ProjectRoot ".venv\Scripts\pythonw.exe"
$ActivateScript = Join-Path $ProjectRoot ".venv\Scripts\Activate.ps1"

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
    try {
        & python -m venv .venv
    } catch {
        Write-Host "[!] Could not create .venv. Running via system Python directly..." -ForegroundColor Yellow
        & python -m omnitrix_watch.main
        exit 0
    }
}

if (Test-Path $ActivateScript) {
    Write-Host "[*] Activating virtual environment..." -ForegroundColor Cyan
    & $ActivateScript
}

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
