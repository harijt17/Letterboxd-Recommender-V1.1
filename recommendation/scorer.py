import pandas as pd


# ==========================================================
# Recommendation Feature Weights
# ==========================================================

GENRE_WEIGHT = 0.30
KEYWORD_WEIGHT = 0.20
DIRECTOR_WEIGHT = 0.15
CAST_WEIGHT = 0.10
WRITER_WEIGHT = 0.05
COUNTRY_WEIGHT = 0.05
LANGUAGE_WEIGHT = 0.05
DECADE_WEIGHT = 0.05
RUNTIME_WEIGHT = 0.025
QUALITY_WEIGHT = 0.025

# ==========================================================
# Feature Score Caps
# ==========================================================

MAX_GENRE_MATCH = 3
MAX_KEYWORD_MATCH = 5
MAX_DIRECTOR_MATCH = 2
MAX_CAST_MATCH = 3
MAX_WRITER_MATCH = 2
MAX_COUNTRY_MATCH = 2
MAX_LANGUAGE_MATCH = 2
MAX_DECADE_MATCH = 1

# ==========================================================
# Recommendation Component Weights
# ==========================================================

METADATA_WEIGHT = 0.70
CONTENT_WEIGHT = 0.30

class RecommendationScorer:

    def __init__(self):
        pass

    # =====================================================
    # Split Helper
    # =====================================================

    def split_values(self, value):

        if pd.isna(value):
            return []

        values = []

        for separator in [",", "-", "|"]:

            if separator in str(value):

                values = [
                    item.strip().lower()
                    for item in str(value).split(separator)
                    if item.strip()
                ]

                return values

        return [str(value).strip().lower()]

    # =====================================================
    # Feature Score
    # =====================================================

    def feature_score(
        self,
        movie_values,
        profile_scores
    ):

        if len(profile_scores) == 0:
            return 0

        score = 0

        for value in movie_values:

            score += profile_scores.get(
                value,
                0
            )

        return score
        # =====================================================
    # Normalize Feature Score
    # =====================================================

    def normalize_feature_score(self,score,maximum):

        if maximum <= 0:
            return 0.0

        return min(score, maximum) / maximum

    # =====================================================
    # Runtime Score
    # =====================================================

    def runtime_score(
        self,
        runtime,
        runtime_profile
    ):

        if runtime is None:
            return 0

        average = runtime_profile["average"]

        difference = abs(
            runtime - average
        )

        if difference <= 15:
            return 1

        if difference <= 30:
            return 0.75

        if difference <= 45:
            return 0.50

        if difference <= 60:
            return 0.25

        return 0

    # =====================================================
    # Quality Score
    # =====================================================

    def quality_score(
        self,
        movie
    ):

        imdb = movie.get(
            "imdb_rating",
            0
        )

        tmdb = movie.get(
            "vote_average",
            0
        )

        quality = (
            imdb +
            tmdb
        ) / 20

        return quality

    # =====================================================
    # Score Candidates
    # =====================================================

    def score(
        self,
        candidates,
        profile
    ):

        scored_movies = candidates.copy()

        recommendation_scores = []

        genre_scores = []
        keyword_scores = []
        director_scores = []
        cast_scores = []
        writer_scores = []
        country_scores = []
        language_scores = []
        decade_scores = []
        runtime_scores = []
        quality_scores = []

        for _, movie in scored_movies.iterrows():

            genre_score = self.feature_score(
                self.split_values(movie["genres"]),
                profile.genres
            )

            keyword_score = self.feature_score(
                self.split_values(movie["keywords"]),
                profile.keywords
            )

            director_score = self.feature_score(
                self.split_values(movie["director"]),
                profile.directors
            )

            cast_score = self.feature_score(
                self.split_values(movie["cast"]),
                profile.cast
            )

            writer_score = self.feature_score(
                self.split_values(movie["writers"]),
                profile.writers
            )

            country_score = self.feature_score(
                self.split_values(
                    movie["production_countries"]
                ),
                profile.countries
            )

            language_score = self.feature_score(
                self.split_values(
                    movie["spoken_languages"]
                ),
                profile.languages
            )

            decade_score = 0

            year = movie.get("year")

            if pd.notna(year):

                decade = f"{int(year // 10) * 10}s"

                decade_score = profile.decades.get(
                    decade,
                    0
                )

            runtime = self.runtime_score(
                movie.get("runtime"),
                profile.runtime
            )

            quality = self.quality_score(
                movie
            )

            # ------------------------------------------
            # Normalize Feature Scores
            # ------------------------------------------

            genre_score = self.normalize_feature_score(
                genre_score,
                MAX_GENRE_MATCH
            )

            keyword_score = self.normalize_feature_score(
                keyword_score,
                MAX_KEYWORD_MATCH
            )

            director_score = self.normalize_feature_score(
                director_score,
                MAX_DIRECTOR_MATCH
            )

            cast_score = self.normalize_feature_score(
                cast_score,
                MAX_CAST_MATCH
            )

            writer_score = self.normalize_feature_score(
                writer_score,
                MAX_WRITER_MATCH
            )

            country_score = self.normalize_feature_score(
                country_score,
                MAX_COUNTRY_MATCH
            )

            language_score = self.normalize_feature_score(
                language_score,
                MAX_LANGUAGE_MATCH
            )

            decade_score = self.normalize_feature_score(
                decade_score,
                MAX_DECADE_MATCH
            )
            metadata_score = (

                genre_score * GENRE_WEIGHT +

                keyword_score * KEYWORD_WEIGHT +

                director_score * DIRECTOR_WEIGHT +

                cast_score * CAST_WEIGHT +

                writer_score * WRITER_WEIGHT +

                country_score * COUNTRY_WEIGHT +

                language_score * LANGUAGE_WEIGHT +

                decade_score * DECADE_WEIGHT +

                runtime * RUNTIME_WEIGHT +

                quality * QUALITY_WEIGHT

            )
            recommendation_scores.append(
                round(metadata_score, 4)
            )

            genre_scores.append(
                genre_score
            )

            keyword_scores.append(
                keyword_score
            )

            director_scores.append(
                director_score
            )

            cast_scores.append(
                cast_score
            )

            writer_scores.append(
                writer_score
            )

            country_scores.append(
                country_score
            )

            language_scores.append(
                language_score
            )

            decade_scores.append(
                decade_score
            )

            runtime_scores.append(
                runtime
            )

            quality_scores.append(
                quality
            )

        scored_movies["genre_score"] = genre_scores
        scored_movies["keyword_score"] = keyword_scores
        scored_movies["director_score"] = director_scores
        scored_movies["cast_score"] = cast_scores
        scored_movies["writer_score"] = writer_scores
        scored_movies["country_score"] = country_scores
        scored_movies["language_score"] = language_scores
        scored_movies["decade_score"] = decade_scores
        scored_movies["runtime_score"] = runtime_scores
        scored_movies["quality_score"] = quality_scores

        scored_movies["metadata_score"] = (
            recommendation_scores
        )

        return scored_movies