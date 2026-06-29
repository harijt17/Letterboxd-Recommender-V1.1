from pathlib import Path

from ingestion.zip_extractor import ZipExtractor
from ingestion.validators import ExportValidator
from ingestion.export_loader import ExportLoader

from matching.movie_matcher import MovieMatcher

from profiling.profile_builder import ProfileBuilder

# ==========================================================
# Configuration
# ==========================================================

SESSION_ID = "test"

exports_dir = Path("Data/exports")

zip_files = list(exports_dir.glob("*.zip"))

if not zip_files:

    raise FileNotFoundError(
        "No ZIP file found in Data/exports"
    )

ZIP_FILE = zip_files[0]

# ==========================================================
# Extract ZIP
# ==========================================================

extractor = ZipExtractor()

folder = extractor.extract(
    ZIP_FILE,
    SESSION_ID
)

# ==========================================================
# Validate Export
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

matched_movies, unmatched = matcher.match_movies(
    movies
)

# ==========================================================
# Build Profile
# ==========================================================

builder = ProfileBuilder()

profile = builder.build_profile(
    matched_movies
)

profile = builder.to_dict(
    profile
)

# ==========================================================
# Print Summary
# ==========================================================

print("\n" + "=" * 60)
print("PROFILE SUMMARY")
print("=" * 60)

print(f"Movies Processed : {profile['movie_count']}")
print(f"Average Rating   : {profile['average_rating']}")

print("\nTop Genres")
print("-" * 60)

for genre, score in sorted(
    profile["genres"].items(),
    key=lambda x: x[1],
    reverse=True
)[:10]:

    print(
        f"{genre:<25} {score:.2f}"
    )

print("\nTop Directors")
print("-" * 60)

for director, score in sorted(
    profile["directors"].items(),
    key=lambda x: x[1],
    reverse=True
)[:10]:

    print(
        f"{director:<25} {score:.2f}"
    )

print("\nTop Cast")
print("-" * 60)

for actor, score in sorted(
    profile["cast"].items(),
    key=lambda x: x[1],
    reverse=True
)[:10]:

    print(
        f"{actor:<25} {score:.2f}"
    )

print("\nTop Keywords")
print("-" * 60)

for keyword, score in sorted(
    profile["keywords"].items(),
    key=lambda x: x[1],
    reverse=True
)[:10]:

    print(
        f"{keyword:<25} {score:.2f}"
    )

print("\nRuntime Preference")
print("-" * 60)

print(profile["runtime"])