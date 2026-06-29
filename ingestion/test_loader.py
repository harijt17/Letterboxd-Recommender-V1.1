from ingestion.zip_extractor import ZipExtractor
from ingestion.validators import ExportValidator
from ingestion.export_loader import ExportLoader
from pathlib import Path

exports_dir = Path("Data/exports")

zip_files = list(exports_dir.glob("*.zip"))

if not zip_files:
    raise FileNotFoundError(
        "No ZIP file found in Data/exports"
    )

ZIP_FILE = zip_files[0]
SESSION_ID = "test"

# -----------------------------------

extractor = ZipExtractor()

folder = extractor.extract(
    ZIP_FILE,
    SESSION_ID
)

# -----------------------------------

validator = ExportValidator()

validator.validate(folder)

# -----------------------------------

loader = ExportLoader(folder)

movies = loader.load()

# -----------------------------------

print("=" * 60)
print("MOVIES LOADED")
print("=" * 60)

print("Total Movies :", len(movies))

print()

print(movies[0])