$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================================"
Write-Host " Letterboxd Recommender - Release Build"
Write-Host "============================================================"
Write-Host ""

Write-Host "Cleaning previous release build..."

Remove-Item ".\dist" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Done."
Write-Host ""

Write-Host "Building release..."

python -m nuitka `
    --standalone `
    --jobs=12 `
    --assume-yes-for-downloads `
    --include-package=nicegui `
    --include-package-data=nicegui `
    --include-package=scipy `
    --include-package=sklearn `
    --include-package=pandas `
    --include-package=numpy `
    --include-package=pyarrow `
    --include-package=joblib `
    --nofollow-import-to=sklearn.tests `
    --nofollow-import-to=scipy.tests `
    --nofollow-import-to=numpy.tests `
    --nofollow-import-to=pandas.tests `
    --include-data-dir=desktop/assets=desktop/assets `
    --output-dir=dist `
    --output-filename="Letterboxd Recommender.exe" `
    launcher.py

Write-Host ""
Write-Host "============================================================"
Write-Host " Release Build Complete"
Write-Host "============================================================"
Write-Host ""

Write-Host "Executable:"
Write-Host "dist\launcher.dist\Letterboxd Recommender.exe"
Write-Host ""