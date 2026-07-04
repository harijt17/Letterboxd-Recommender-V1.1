from pathlib import Path

import joblib
import pandas as pd
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer

# ==========================================================
# Paths
# ==========================================================

DATASET_PATH = (
    Path("Data")
    / "processed"
    / "movies.parquet"
)

OUTPUT_DIR = (
    Path("Data")
    / "processed"
    / "tfidf"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

VECTORIZER_PATH = (
    OUTPUT_DIR
    / "vectorizer.joblib"
)

MATRIX_PATH = (
    OUTPUT_DIR
    / "matrix.npz"
)

# ==========================================================
# Load Dataset
# ==========================================================

print("=" * 60)
print("Loading processed dataset...")
print("=" * 60)

movies = pd.read_parquet(
    DATASET_PATH,
    columns=["combined_features"]
)

movies["combined_features"] = (
    movies["combined_features"]
    .fillna("")
    .astype(str)
)

print(f"Movies loaded : {len(movies):,}")

# ==========================================================
# Build TF-IDF Model
# ==========================================================

print("\nBuilding TF-IDF model...")

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=50000,
    ngram_range=(1, 2),
    min_df=2
)

movie_matrix = vectorizer.fit_transform(
    movies["combined_features"]
)

print(
    f"Vocabulary size : "
    f"{len(vectorizer.vocabulary_):,}"
)

# ==========================================================
# Save Vectorizer
# ==========================================================

print("\nSaving vectorizer...")

joblib.dump(
    vectorizer,
    VECTORIZER_PATH,
    compress=3
)

# ==========================================================
# Save Sparse Matrix
# ==========================================================

print("Saving TF-IDF matrix...")

sparse.save_npz(
    MATRIX_PATH,
    movie_matrix
)

# ==========================================================
# Summary
# ==========================================================

print("\n" + "=" * 60)
print("TF-IDF BUILD COMPLETE")
print("=" * 60)

print(f"Vectorizer : {VECTORIZER_PATH}")
print(f"Matrix     : {MATRIX_PATH}")
print(f"Movies     : {movie_matrix.shape[0]:,}")
print(f"Vocabulary : {movie_matrix.shape[1]:,}")