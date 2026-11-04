<#
.SYNOPSIS
    Launches the Omnitrix Web Simulator Demo in default browser.
#>

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$IndexPath = Join-Path $ProjectRoot "web\index.html"

Write-Host "=====================================================================" -ForegroundColor Green
Write-Host "  OMNITRIX WATCH // LAUNCHING WEB BROWSER SIMULATOR" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host ""

Write-Host "[*] Opening $IndexPath in default browser..." -ForegroundColor Cyan
Start-Process $IndexPath
Write-Host "[✓] Web Simulator active." -ForegroundColor Green
Start-Sleep -Seconds 2
