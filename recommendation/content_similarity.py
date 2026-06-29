import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ContentSimilarity:

    def __init__(self, repository):

        self.repository = repository

        print("Building TF-IDF model...")

        self.movies = repository.movies
        
        self.movies["combined_features"] = (
            self.movies["combined_features"]
            .fillna("")
            .astype(str)
        )

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=50000,
            ngram_range=(1, 2),
            min_df=2
        )

        self.movie_matrix = self.vectorizer.fit_transform(
            self.movies["combined_features"]
        )

        print(
            f"TF-IDF vocabulary size : "
            f"{len(self.vectorizer.vocabulary_):,}"
        )

    # =====================================================
    # Rating Weight
    # =====================================================

    def rating_weight(self, rating):

        if rating >= 5.0:
            return 5

        if rating >= 4.5:
            return 4

        if rating >= 4.0:
            return 3

        if rating >= 3.5:
            return 2

        if rating >= 3.0:
            return 1

        return 0


    # =====================================================
    # Build User Document
    # =====================================================

    def build_user_document(
        self,
        matched_movies
    ):

        documents = []

        for movie in matched_movies:

            weight = self.rating_weight(
                movie.get("rating", 0)
            )

            if weight == 0:
                continue

            text = movie.get(
                "combined_features",
                ""
            )

            if not text:
                continue

            documents.extend(
                [text] * weight
            )

        return " ".join(documents)
        # =====================================================
    # Compute Content Similarity
    # =====================================================

    # =====================================================
    # Compute Content Similarity
    # =====================================================

    def compute_similarity(
        self,
        candidates,
        matched_movies
    ):

        # ---------------------------------------------
        # Build User Document
        # ---------------------------------------------

        user_document = self.build_user_document(
            matched_movies
        )

        user_vector = self.vectorizer.transform(
            [user_document]
        )

        # ---------------------------------------------
        # Candidate Vectors
        # ---------------------------------------------

        candidate_indices = (
            candidates["dataset_index"]
            .tolist()
        )

        candidate_matrix = self.movie_matrix[
            candidate_indices
        ]

        similarities = cosine_similarity(
            user_vector,
            candidate_matrix
        ).flatten()

        candidates = candidates.copy()

        candidates["content_similarity"] = similarities

        return candidates