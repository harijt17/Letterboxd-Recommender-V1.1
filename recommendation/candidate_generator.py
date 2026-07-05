import pandas as pd

class CandidateGenerator:

    def __init__(self, repository):

        self.repository = repository

    # =====================================================
    # Generate Candidates
    # =====================================================

    def generate_candidates(
        self,
        profile,
        watched_ids,
        top_k=5000
    ):


        movies = self.repository.get_candidate_movies(
            profile,
            max_genres=20,
            max_directors=50,
            max_keywords=300
        )

        candidates = movies[
            ~movies["id"].isin(watched_ids)
        ].copy()

        candidates["dataset_index"] = candidates.index

        scores = []

        genres = profile.genres
        directors = profile.directors
        cast = profile.cast
        writers = profile.writers
        keywords = profile.keywords
        countries = profile.countries
        languages = profile.languages
        decades = profile.decades
        

        for movie in candidates.itertuples(index=False):

            score = 0.0

            for value in movie.genres_list:
                score += genres.get(value, 0)

            for value in movie.director_list:
                score += directors.get(value, 0)

            for value in movie.cast_list:
                score += cast.get(value, 0)

            for value in movie.writers_list:
                score += writers.get(value, 0)

            for value in movie.keywords_list:
                score += keywords.get(value, 0)

            for value in movie.countries_list:
                score += countries.get(value, 0)

            for value in movie.languages_list:
                score += languages.get(value, 0)

            score += decades.get(movie.decade, 0)

            scores.append(score)
        

        candidates["candidate_score"] = scores

        candidates = candidates[
            candidates["candidate_score"] > 0
        ]

        candidates = candidates.sort_values(
            by="candidate_score",
            ascending=False
        )

        

        return candidates.head(top_k)