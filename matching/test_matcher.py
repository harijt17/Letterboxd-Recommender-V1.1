from ingestion.zip_extractor import ZipExtractor
from ingestion.validators import ExportValidator
from ingestion.export_loader import ExportLoader
from matching.movie_matcher import MovieMatcher

# ==========================================================
# Configuration
# ==========================================================

SESSION_ID = "test"

from pathlib import Path

exports_dir = Path("Data/exports")

zip_files = list(exports_dir.glob("*.zip"))

if not zip_files:
    raise FileNotFoundError(
        "No ZIP file found in Data/exports"
    )

ZIP_FILE = zip_files[0]

# ==========================================================
# Extract
# ==========================================================

extractor = ZipExtractor()

folder = extractor.extract(
    ZIP_FILE,
    SESSION_ID
)

# ==========================================================
# Validate
# ==========================================================

validator = ExportValidator()

validator.validate(folder)

# ==========================================================
# Load Export
# ==========================================================

loader = ExportLoader(folder)

movies = loader.load()

# ==========================================================
# Match Movies
# ==========================================================

matcher = MovieMatcher()

matched, unmatched = matcher.match_movies(
    movies
)

# ==========================================================
# Results
# ==========================================================

print("\n" + "=" * 60)
print("MOVIE MATCHING SUMMARY")
print("=" * 60)

print(f"Movies Loaded : {len(movies)}")
print(f"Matched       : {len(matched)}")
print(f"Unmatched     : {len(unmatched)}")

match_rate = (
    len(matched) /
    len(movies)
) * 100

print(f"Match Rate    : {match_rate:.2f}%")

# ==========================================================
# Show Unmatched Movies
# ==========================================================

if unmatched:

    print("\nUnmatched Movies")
    print("-" * 60)

    for movie in unmatched[:20]:

        print(
            f"{movie['title']} ({movie['year']})"
        )

else:

    print("\nAll movies matched successfully!")