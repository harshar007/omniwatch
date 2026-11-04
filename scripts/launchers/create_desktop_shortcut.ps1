<#
.SYNOPSIS
    Generates a Windows desktop shortcut for Omnitrix Watch Companion.
#>

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutFile = Join-Path $DesktopPath "Omnitrix Watch Companion.lnk"

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutFile)

$TargetScript = Join-Path $ProjectRoot "Launch-Omnitrix.bat"
$Shortcut.TargetPath = $TargetScript
$Shortcut.WorkingDirectory = $ProjectRoot
$Shortcut.Description = "Omnitrix Watch Research Companion for Redmi Watch Move 2"

$IconFile = Join-Path $ProjectRoot "assets\omnitrix.ico"
if (-not (Test-Path $IconFile)) {
    $IconFile = Join-Path $ProjectRoot "assets\icons\omnitrix.ico"
}
if (Test-Path $IconFile) {
    $Shortcut.IconLocation = "$IconFile,0"
}

$Shortcut.Save()
Write-Host "[✓] Desktop shortcut created at: $ShortcutFile" -ForegroundColor Green
