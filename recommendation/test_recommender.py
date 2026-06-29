from pathlib import Path

from ingestion.zip_extractor import ZipExtractor
from ingestion.validators import ExportValidator
from ingestion.export_loader import ExportLoader

from matching.movie_matcher import MovieMatcher

from profiling.profile_builder import ProfileBuilder

from recommendation.movie_repository import MovieRepository
from recommendation.recommender import Recommender


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
# Extract Export
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


# ==========================================================
# Watched Movie IDs
# ==========================================================

watched_ids = {

    movie["id"]

    for movie in matched_movies
}


# ==========================================================
# Recommendation Engine
# ==========================================================

repository = MovieRepository()

recommender = Recommender(
    repository
)

recommendations = recommender.recommend(
    profile=profile,
    matched_movies=matched_movies,
    watched_ids=watched_ids,
    top_k=20
)


# ==========================================================
# Display
# ==========================================================

print("\n" + "=" * 70)
print("TOP 20 RECOMMENDATIONS")
print("=" * 70)

for index, movie in enumerate(
    recommendations,
    start=1
):

    print(
        f"{index:02d}. "
        f"{movie['title']} "
        f"({int(movie['year'])})"
    )

    print(
        f"    Score : "
        f"{movie['recommendation_score']:.4f}"
    )

    print(
        f"    Genres : "
        f"{movie['genres']}"
    )

    print(
        f"    Director : "
        f"{movie['director']}"
    )

    print()