Write-Host "Cleaning build artifacts..."

Remove-Item ".\dist" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item ".\build_output" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item ".\launcher.build" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item ".\launcher.dist" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item ".\launcher.onefile-build" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Done."