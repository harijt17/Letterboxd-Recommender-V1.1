import pandas as pd
import time

class CandidateGenerator:

    def __init__(self, repository):

        self.repository = repository

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

        score = 0.0

        for value in movie_values:

            score += profile_scores.get(
                value,
                0
            )

        return score

    # =====================================================
    # Generate Candidates
    # =====================================================

    def generate_candidates(
        self,
        profile,
        watched_ids,
        top_k=5000
    ):
        start_time = time.time()

        movies = self.repository.get_candidate_movies(
            profile,
            max_genres=20,
            max_directors=50,
            max_keywords=300
        )

        print(f"Repository lookup time: {time.time() - start_time:.2f} s")
        start_time = time.time()

        candidates = movies[
            ~movies["id"].isin(watched_ids)
        ].copy()

        print(f"Filter watched: {time.time() - start_time:.2f} s")
        start_time = time.time()

        candidates["dataset_index"] = candidates.index

        print(f"Candidate pool: {len(candidates):,}")

        scores = []

        for movie in candidates.itertuples(index=True):

            score = 0.0

            score += self.feature_score(
                movie.genres_list,
                profile.genres
            )

            score += self.feature_score(
                movie.director_list,
                profile.directors
            )

            score += self.feature_score(
                movie.cast_list,
                profile.cast
            )

            score += self.feature_score(
                movie.writers_list,
                profile.writers
            )

            score += self.feature_score(
                movie.keywords_list,
                profile.keywords
            )

            score += self.feature_score(
                movie.countries_list,
                profile.countries
            )

            score += self.feature_score(
                movie.languages_list,
                profile.languages
            )

            year = movie.year

            if pd.notna(year):

                decade = f"{int(year // 10) * 10}s"

                score += profile.decades.get(
                    decade,
                    0
                )

            scores.append(score)
        print(f"scored loop: {time.time() - start_time:.2f} s")
        start_time = time.time()

        candidates["candidate_score"] = scores

        candidates = candidates[
            candidates["candidate_score"] > 0
        ]

        candidates = candidates.sort_values(
            by="candidate_score",
            ascending=False
        )
        print(f"sorting: {time.time() - start_time:.2f} s")
        

        return candidates.head(top_k)