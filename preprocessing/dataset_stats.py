from pathlib import Path

import pandas as pd

# ==========================================================
# Dataset Path
# ==========================================================

DATASET = (
    Path("Data")
    / "processed"
    / "movies.parquet"
)

# ==========================================================
# Load Dataset
# ==========================================================

print("=" * 70)
print("LOADING DATASET")
print("=" * 70)

df = pd.read_parquet(DATASET)

# ==========================================================
# Basic Information
# ==========================================================

print("\nDATASET SHAPE")
print("-" * 70)

print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")

print("\nCOLUMN NAMES")
print("-" * 70)

for column in df.columns:
    print(column)

# ==========================================================
# Missing Values
# ==========================================================

print("\nMISSING VALUES")
print("-" * 70)

missing = (
    df.isna()
    .sum()
    .sort_values(ascending=False)
)

missing = missing[missing > 0]

if missing.empty:
    print("No missing values.")
else:
    print(missing)

# ==========================================================
# Memory Usage
# ==========================================================

print("\nMEMORY USAGE")
print("-" * 70)

memory = df.memory_usage(deep=True).sum() / 1024**2

print(f"{memory:.2f} MB")

# ==========================================================
# Numeric Statistics
# ==========================================================

print("\nNUMERIC SUMMARY")
print("-" * 70)

numeric = [
    "vote_average",
    "vote_count",
    "runtime",
    "popularity",
    "imdb_rating",
    "imdb_votes",
    "quality_score"
]

numeric = [c for c in numeric if c in df.columns]

print(df[numeric].describe().round(2))

# ==========================================================
# Languages
# ==========================================================

print("\nTOP LANGUAGES")
print("-" * 70)

print(
    df["original_language"]
    .value_counts()
    .head(20)
)

# ==========================================================
# Release Years
# ==========================================================

print("\nYEAR RANGE")
print("-" * 70)

print(
    f"Earliest : {int(df['year'].min())}"
)

print(
    f"Latest   : {int(df['year'].max())}"
)

# ==========================================================
# Top Genres
# ==========================================================

print("\nTOP GENRES")
print("-" * 70)

genres = (
    df["genres"]
    .fillna("")
    .str.split(",")
    .explode()
    .str.strip()
)

genres = genres[genres != ""]

print(
    genres.value_counts().head(20)
)

# ==========================================================
# Top Directors
# ==========================================================

print("\nTOP DIRECTORS")
print("-" * 70)

directors = (
    df["director"]
    .fillna("")
    .str.split(",")
    .explode()
    .str.strip()
)

directors = directors[directors != ""]

print(
    directors.value_counts().head(20)
)

# ==========================================================
# Runtime Distribution
# ==========================================================

print("\nRUNTIME")
print("-" * 70)

print(
    df["runtime"]
    .describe()
    .round(2)
)

# ==========================================================
# Vote Distribution
# ==========================================================

print("\nVOTE COUNT QUANTILES")
print("-" * 70)

print(
    df["vote_count"].quantile([
        0.25,
        0.50,
        0.75,
        0.90,
        0.95,
        0.99
    ])
)

# ==========================================================
# Sample Movies
# ==========================================================

print("\nSAMPLE MOVIES")
print("-" * 70)

print(

    df[
        [
            "title",
            "year",
            "genres",
            "director",
            "vote_average",
            "imdb_rating"
        ]

    ].sample(10, random_state=42)

)

print("\n" + "=" * 70)
print("DATASET INSPECTION COMPLETE")
print("=" * 70)

