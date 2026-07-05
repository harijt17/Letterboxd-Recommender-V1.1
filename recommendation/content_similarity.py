import pandas as pd
import joblib
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.paths import PROCESSED_DATA_DIR

# ==========================================================
# Paths
# ==========================================================

TFIDF_DIR = (
    PROCESSED_DATA_DIR
    / "tfidf"
)

VECTORIZER_PATH = (
    TFIDF_DIR
    / "vectorizer.joblib"
)

MATRIX_PATH = (
    TFIDF_DIR
    / "matrix.npz"
)

class ContentSimilarity:

    def __init__(self):

        print("Loading TF-IDF model...")

        self.vectorizer = joblib.load(
            VECTORIZER_PATH
        )

        self.movie_matrix = sparse.load_npz(
            MATRIX_PATH
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