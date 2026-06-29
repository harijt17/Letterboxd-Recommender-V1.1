import re
import pandas as pd


class DiversityFilter:

    def __init__(
        self,
        max_per_director=2,
        max_per_decade=5
    ):

        self.max_per_director = max_per_director
        self.max_per_decade = max_per_decade

    # =====================================================
    # Normalize Title
    # =====================================================

    def normalize_title(self, title):

        if title is None:
            return ""

        title = title.lower()

        title = re.sub(
            r"\(\d{4}\)",
            "",
            title
        )

        title = re.sub(
            r"[^a-z0-9 ]",
            " ",
            title
        )

        title = " ".join(
            title.split()
        )

        return title

    # =====================================================
    # Simple Franchise Key
    # =====================================================

    def franchise_key(self, title):

        title = self.normalize_title(title)

        words = title.split()

        if len(words) >= 2:
            return " ".join(words[:2])

        return title

    # =====================================================
    # Apply Diversity
    # =====================================================

    def apply(
        self,
        ranked_movies,
        top_k=20
    ):

        results = []

        director_count = {}
        decade_count = {}
        franchise_seen = set()

        for _, movie in ranked_movies.iterrows():

            director = movie.get(
                "director",
                ""
            )

            year = movie.get(
                "year"
            )

            title = movie.get(
                "title",
                ""
            )

            # -----------------------------
            # Director Diversity
            # -----------------------------

            if director:

                count = director_count.get(
                    director,
                    0
                )

                if count >= self.max_per_director:
                    continue

            # -----------------------------
            # Decade Diversity
            # -----------------------------

            if year:

                decade = (
                    int(year) // 10
                ) * 10

                count = decade_count.get(
                    decade,
                    0
                )

                if count >= self.max_per_decade:
                    continue

            # -----------------------------
            # Franchise Diversity
            # -----------------------------

            key = self.franchise_key(
                title
            )

            if key in franchise_seen:
                continue

            # -----------------------------
            # Accept Movie
            # -----------------------------

            results.append(movie)

            franchise_seen.add(key)

            if director:

                director_count[
                    director
                ] = director_count.get(
                    director,
                    0
                ) + 1

            if year:

                decade_count[
                    decade
                ] = decade_count.get(
                    decade,
                    0
                ) + 1

            if len(results) >= top_k:
                break

        return pd.DataFrame(results).reset_index(drop=True)