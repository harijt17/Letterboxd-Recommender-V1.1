$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================================"
Write-Host " Letterboxd Recommender - Development Build"
Write-Host "============================================================"
Write-Host ""

Write-Host "Starting incremental build..."
Write-Host ""

python -m nuitka `
    --standalone `
    --jobs=12 `
    --assume-yes-for-downloads `
    --remove-output `
    --include-package=nicegui `
    --include-package-data=nicegui `
    --include-package=scipy `
    --include-package=pandas `
    --include-package=numpy `
    --include-package=pyarrow `
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
Write-Host " Development Build Complete"
Write-Host "============================================================"
Write-Host ""

Write-Host "Executable:"
Write-Host "dist\launcher.dist\Letterboxd Recommender.exe"
Write-Host ""