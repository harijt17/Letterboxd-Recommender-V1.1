$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================================"
Write-Host " Letterboxd Recommender - Release Build"
Write-Host "============================================================"
Write-Host ""

# ----------------------------------------------------------
# Clean Previous Release Build
# ----------------------------------------------------------

Write-Host "Cleaning previous build..."

Remove-Item ".\build_output" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item ".\launcher.build" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item ".\launcher.dist" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item ".\launcher.onefile-build" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Done."
Write-Host ""

# ----------------------------------------------------------
# Release Build
# ----------------------------------------------------------

Write-Host "Building release..."

python -m nuitka `
    --standalone `
    --follow-imports `
    --jobs=12 `
    --assume-yes-for-downloads `
    --include-package=nicegui `
    --include-package=scipy `
    --include-package=sklearn `
    --include-package=pandas `
    --include-package=numpy `
    --include-package=pyarrow `
    --include-package=joblib `
    --include-data-dir=desktop/assets=desktop/assets `
    --windows-console-mode=disable `
    --company-name="Hari Prasath JT" `
    --product-name="Letterboxd Recommender" `
    --product-version="2.0.0" `
    --file-version="2.0.0" `
    --file-description="Letterboxd Movie Recommendation System" `
    --copyright="© Hari Prasath JT" `
    `
    # Uncomment after adding your application icon
    # --windows-icon-from-ico=icon.ico `
    `
    --output-dir=build_output `
    --output-filename="Letterboxd Recommender.exe" `
    launcher.py

Write-Host ""
Write-Host "============================================================"
Write-Host " Release Build Complete"
Write-Host "============================================================"
Write-Host ""

Write-Host "Executable:"
Write-Host "build_output\launcher.dist\Letterboxd Recommender.exe"
Write-Host ""