$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================================"
Write-Host " Cleaning Build Artifacts"
Write-Host "============================================================"
Write-Host ""

Write-Host "Removing build artifacts..."

Remove-Item ".\dist" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item ".\build_output" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Done."
Write-Host ""