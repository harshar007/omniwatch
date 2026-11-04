<#
.SYNOPSIS
    PowerShell launcher for Omnitrix Simulator.
#>

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "Omnitrix Alien Simulator // Wear OS Simulator"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $ProjectRoot

Write-Host "=====================================================================" -ForegroundColor Green
Write-Host "  ALIEN WATCH // OMNITRIX SIMULATOR" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host ""

$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (Test-Path $VenvPython) {
    Write-Host "[*] Launching via virtual environment..." -ForegroundColor Cyan
    Start-Process -FilePath $VenvPython -ArgumentList "-m", "omnitrix_watch.main"
    exit 0
}

$SystemPython = Get-Command python -ErrorAction SilentlyContinue
if ($SystemPython) {
    Write-Host "[*] Launching via system Python..." -ForegroundColor Cyan
    Start-Process -FilePath "python" -ArgumentList "-m", "omnitrix_watch.main"
    exit 0
}

Write-Host "[-] Python not found on system PATH. Please install Python 3.11+." -ForegroundColor Red
Read-Host "Press Enter to exit"
exit 1
