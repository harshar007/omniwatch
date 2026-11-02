<#
.SYNOPSIS
    Creates a desktop shortcut for Omnitrix Watch with one click.
#>

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TargetBat = Join-Path $ScriptDir "Launch-Omnitrix.bat"

if (-not (Test-Path $TargetBat)) {
    Write-Host "[-] Error: Launch-Omnitrix.bat not found in $ScriptDir" -ForegroundColor Red
    exit 1
}

$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
$ShortcutPath = Join-Path $DesktopPath "Omnitrix Watch.lnk"

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetBat
$Shortcut.WorkingDirectory = $ScriptDir
$Shortcut.Description = "Omnitrix Watch Companion & BLE Research Platform"
$Shortcut.Save()

Write-Host "=====================================================================" -ForegroundColor Green
Write-Host "  OMNITRIX WATCH // DESKTOP SHORTCUT CREATED" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "[+] Shortcut successfully placed on your Desktop:" -ForegroundColor Green
Write-Host "    $ShortcutPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now double-click 'Omnitrix Watch' directly from your Desktop!" -ForegroundColor Green
