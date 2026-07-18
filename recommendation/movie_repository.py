from collections import defaultdict

import pandas as pd

GENRE_WEIGHT = 1
DIRECTOR_WEIGHT = 2
KEYWORD_WEIGHT = 1

MAX_CANDIDATES = 30000

from utils.paths import PROCESSED_DATA_DIR

DEFAULT_DATASET = (
    PROCESSED_DATA_DIR
    / "movies.parquet"
)

def split_values(value):
    if pd.isna(value):
        return []

    text = str(value).lower()

    for separator in [",", "-", "|"]:

        if separator in text:
            return [
                item.strip()
                for item in text.split(separator)
                if item.strip()
            ]

    return [text.strip()]


class MovieRepository:

    def __init__(self, dataset_path=None):

        if dataset_path is None:
            dataset_path = DEFAULT_DATASET

        self.movies = pd.read_parquet(
            dataset_path
        )

        self.movies["genres_list"] = self.movies["genres"].apply(split_values)
        self.movies["director_list"] = self.movies["director"].apply(split_values)
        self.movies["cast_list"] = self.movies["cast"].apply(split_values)
        self.movies["writers_list"] = self.movies["writers"].apply(split_values)
        self.movies["keywords_list"] = self.movies["keywords"].apply(split_values)
        self.movies["countries_list"] = self.movies["production_countries"].apply(split_values)
        self.movies["languages_list"] = self.movies["spoken_languages"].apply(split_values)


        self.genre_index = defaultdict(set)
        self.director_index = defaultdict(set)
        self.keyword_index = defaultdict(set)

        for movie in self.movies.itertuples(index=True):

            for genre in str(movie.genres).lower().split(","):

                genre = genre.strip()

                if genre:
                    self.genre_index[genre].add(movie.Index)

            for director in str(movie.director).lower().split(","):

                director = director.strip()

                if director:
                    self.director_index[director].add(movie.Index)

            for keyword in str(movie.keywords).lower().replace("|", ",").split(","):

                keyword = keyword.strip()

                if keyword:
                    self.keyword_index[keyword].add(movie.Index)


    # =====================================================
    # Get Entire Dataset
    # =====================================================

    def get_all_movies(self):

        return self.movies

    # =====================================================
    # Get Movie by ID
    # =====================================================

    def get_movie_by_id(
        self,
        movie_id
    ):

        movie = self.movies[
            self.movies["id"] == movie_id
        ]

        if movie.empty:
            return None

        return movie.iloc[0]

    # =====================================================
    # Get Movies by IDs
    # =====================================================

    def get_movies_by_ids(
        self,
        movie_ids
    ):

        return self.movies[
            self.movies["id"].isin(movie_ids)
        ]

    # =====================================================
    # Get Movies by Genre
    # =====================================================

    def get_movies_by_genre(
        self,
        genre
    ):

        return self.movies[
            self.movies["genres"]
            .fillna("")
            .str.contains(
                genre,
                case=False,
                regex=False
            )
        ]

    # =====================================================
    # Get Movies by Director
    # =====================================================

    def get_movies_by_director(
        self,
        director
    ):

        return self.movies[
            self.movies["director"]
            .fillna("")
            .str.contains(
                director,
                case=False,
                regex=False
            )
        ]

    # =====================================================
    # Get Movies by Cast
    # =====================================================

    def get_movies_by_cast(
        self,
        actor
    ):

        return self.movies[
            self.movies["cast"]
            .fillna("")
            .str.contains(
                actor,
                case=False,
                regex=False
            )
        ]

    # =====================================================
    # Get Movies by Keyword
    # =====================================================

    def get_movies_by_keyword(
        self,
        keyword
    ):

        return self.movies[
            self.movies["keywords"]
            .fillna("")
            .str.contains(
                keyword,
                case=False,
                regex=False
            )
        ]

    # =====================================================
    # Exclude Already Watched Movies
    # =====================================================

    def exclude_movies(
        self,
        movies,
        watched_ids
    ):

        return movies[
            ~movies["id"].isin(
                watched_ids
            )
        ]
    

    def get_candidate_movies(
    self,
    profile,
    max_genres=20,
    max_directors=50,
    max_keywords=300,
    min_score=3
):

        movie_scores = defaultdict(int)

        top_genres = sorted(
            profile.genres.items(),
            key=lambda x: x[1],
            reverse=True
        )[:max_genres]

        top_directors = sorted(
            profile.directors.items(),
            key=lambda x: x[1],
            reverse=True
        )[:max_directors]

        top_keywords = sorted(
            profile.keywords.items(),
            key=lambda x: x[1],
            reverse=True
        )[:max_keywords]

        # Genres (strong signal)
        for genre, weight in top_genres:
            for idx in self.genre_index.get(genre,()):
                movie_scores[idx] += weight * GENRE_WEIGHT

        # Directors (very strong signal)
        for director, weight in top_directors:
            for idx in self.director_index.get(director, ()):
                movie_scores[idx] += weight * DIRECTOR_WEIGHT

        # Keywords (weak signal)
        for keyword, weight in top_keywords:
            for idx in self.keyword_index.get(keyword, ()):
                movie_scores[idx] += weight * KEYWORD_WEIGHT

        candidate_indices = [
            idx
            for idx, score in sorted(
                movie_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:MAX_CANDIDATES]
        ]

        if not candidate_indices:
            return self.movies.iloc[[]].copy()

        return self.movies.loc[candidate_indices].copy()