from pathlib import Path
import re

import pandas as pd
from rapidfuzz import process, fuzz


DEFAULT_DATASET = (
    Path("Data")
    / "processed"
    / "movies.parquet"
)


# ==========================================================
# Helpers
# ==========================================================

def normalize_title(title: str) -> str:

    if title is None:
        return ""

    title = str(title).lower()

    title = title.replace("&", "and")
    title = title.replace("–", "-")
    title = title.replace("—", "-")

    # Remove year
    title = re.sub(r"\(\d{4}\)", "", title)

    # Remove punctuation
    title = re.sub(r"[^\w\s]", " ", title)

    # Remove extra spaces
    title = " ".join(title.split())

    return title


def to_python(value):

    if isinstance(value, list):
        return value

    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        return value.item()

    return value


# ==========================================================
# Movie Matcher
# ==========================================================

class MovieMatcher:

    def __init__(self,movies_df=None,dataset_path=None):

        if movies_df is not None:

            self.movies_df = movies_df

        else:

            if dataset_path is None:
                dataset_path = DEFAULT_DATASET

            print("Loading processed movie dataset...")

            self.movies_df = pd.read_parquet(dataset_path)

        self.movies_df["title_lower"] = (
            self.movies_df["title"]
            .apply(normalize_title)
        )
        # ======================================================
        # Build Lookup Tables
        # ======================================================

        print("Building title lookup...")

        self.title_lookup = {}

        for idx, title, year in zip(
            self.movies_df.index,
            self.movies_df["title_lower"],
            self.movies_df["year"]
        ):
            self.title_lookup[(title, year)] = idx


        print(f"Indexed {len(self.title_lookup):,} movies")

        self.movie_titles = (
            self.movies_df["title_lower"]
            .unique()
            .tolist()
        )

        print(f"Loaded {len(self.movies_df):,} movies")

        # ======================================================
        # Statistics
        # ======================================================

        self.exact_matches = 0
        self.fuzzy_matches = 0
        self.failed_matches = 0

    # ======================================================
    # Exact Match
    # ======================================================

    def exact_match(self,title,year=None):

        title = normalize_title(title)
        

        if year is None:
            return None

        idx = self.title_lookup.get((title, year))

        if idx is None:
            return None

        return self.movies_df.loc[idx]
    
    # ======================================================
    # Fuzzy Match
    # ======================================================

    def fuzzy_match(
        self,
        title,
        year=None,
        threshold=90
    ):

        title = normalize_title(title)

        result = process.extractOne(
            title,
            self.movie_titles,
            scorer=fuzz.WRatio
        )

        if result is None:
            return None

        matched_title, score, _ = result

        if score < threshold:
            return None

        matches = self.movies_df[
            self.movies_df["title_lower"] == matched_title
        ]

        if matches.empty:
            return None

        if year is not None:

            year_matches = matches[
                matches["year"] == year
            ]

            if not year_matches.empty:
                return year_matches.iloc[0]

        return matches.iloc[0]

    # ======================================================
    # Main Match
    # ======================================================

    def match_movie(self, title, year=None):

        movie = self.exact_match(
            title,
            year
        )

        if movie is not None:
            self.exact_matches += 1
            return movie

        movie = self.fuzzy_match(
            title,
            year
        )

        if movie is not None:
            self.fuzzy_matches += 1
            return movie

        self.failed_matches += 1
        return None

    # ======================================================
    # Enrich Movie
    # ======================================================
    
    def enrich_movie(self, movie_record):

        movie = self.match_movie(
            title=movie_record["title"],
            year=movie_record.get("year")
        )

        if movie is None:
            return None
        movie = movie.drop(labels=[
            "genres_list",
            "director_list",
            "cast_list",
            "writers_list",
            "keywords_list",
            "countries_list",
            "languages_list"
        ], errors="ignore")

        movie = {
            key: to_python(value)
            for key, value in movie.to_dict().items()
        }

        # Preserve Letterboxd information
        movie["rating"] = movie_record.get("rating")
        movie["review"] = movie_record.get("review")
        movie["watched_date"] = movie_record.get("watched_date")
        movie["rewatch"] = movie_record.get("rewatch")
        movie["tags"] = movie_record.get("tags")
        movie["uri"] = movie_record.get("uri")

        return movie

    # ======================================================
    # Batch Match
    # ======================================================

    def match_movies(self, movie_list):

        matched = []
        unmatched = []

        for movie in movie_list:

            result = self.enrich_movie(movie)

            if result is None:
                print(f"UNMATCHED: {movie['title']} ({movie.get('year')})")
                unmatched.append(movie)
            else:
                matched.append(result)
        print("\nMovie Matching Statistics")
        print("=" * 40)
        print(f"Exact Matches : {self.exact_matches}")
        print(f"Fuzzy Matches : {self.fuzzy_matches}")
        print(f"Failed        : {self.failed_matches}")

        return matched, unmatched