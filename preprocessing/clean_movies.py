import pandas as pd
from pathlib import Path

# ==========================================================
# Paths
# ==========================================================

INPUT_FILE = "Data/raw/The Ultimate 1Million Movies Dataset (TMDB + IMDb).csv"

OUTPUT_DIR = Path("Data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CSV_OUTPUT = OUTPUT_DIR / "movies.csv"
PARQUET_OUTPUT = OUTPUT_DIR / "movies.parquet"

# ==========================================================
# Load Dataset
# ==========================================================

print("=" * 60)
print("Loading dataset...")
print("=" * 60)

df = pd.read_csv(
    INPUT_FILE,
    low_memory=False
)

print(f"Original movies : {len(df):,}")

# ==========================================================
# Keep Required Columns
# ==========================================================

columns = [
    "id",
    "title",
    "status",
    "vote_average",
    "vote_count",
    "release_date",
    "runtime",
    "original_language",
    "overview",
    "popularity",
    "genres",
    "production_companies",
    "production_countries",
    "spoken_languages",
    "cast",
    "director",
    "director_of_photography",
    "writers",
    "producers",
    "music_composer",
    "imdb_rating",
    "imdb_votes",
    "poster_path",
    "tagline",
    "keywords",
    "certification_us"
]

df = df[columns]

print(f"Columns kept : {len(columns)}")

# ==========================================================
# Keep Released Movies Only
# ==========================================================

before = len(df)

df = df[df["status"] == "Released"]

print(f"Removed unreleased movies : {before - len(df):,}")

# ==========================================================
# Remove Missing Release Dates
# ==========================================================

before = len(df)

df = df[df["release_date"].notna()]

print(f"Removed missing release dates : {before - len(df):,}")

# ==========================================================
# Remove Movies Missing Essential Information
# ==========================================================

before = len(df)

df = df.dropna(
    subset=[
        "title",
        "genres",
        "overview"
    ]
)

print(f"Removed incomplete movies : {before - len(df):,}")

# ==========================================================
# Vote Statistics (Informational Only)
# ==========================================================

print("\nVote Count Distribution")
print("-" * 60)

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
# Fill Missing Numeric Values
# ==========================================================

numeric_columns = [
    "vote_average",
    "vote_count",
    "runtime",
    "popularity",
    "imdb_rating",
    "imdb_votes"
]

for col in numeric_columns:
    df[col] = df[col].fillna(0)

# ==========================================================
# Convert Release Date
# ==========================================================

df["release_date"] = pd.to_datetime(
    df["release_date"],
    errors="coerce"
)

df = df.dropna(subset=["release_date"])

df["year"] = df["release_date"].dt.year.astype(int)

# ==========================================================
# Keep Movies Released From 1900 Onwards
# ==========================================================

before = len(df)

df = df[df["year"] >= 1900]

print(f"Removed movies before 1900 : {before - len(df):,}")

df["decade"] = (
    (df["year"] // 10) * 10
).astype(int)


# ==========================================================
# Runtime
# ==========================================================

df["runtime"] = (
    pd.to_numeric(
        df["runtime"],
        errors="coerce"
    )
    .fillna(0)
    .astype(int)
)

before = len(df)

df = df[df["runtime"] >= 15]

print(f"Removed runtime < 15 min : {before - len(df):,}")

# ==========================================================
# Vote Count
# ==========================================================

before = len(df)

df = df[
    (df["vote_count"] > 1) |
    (df["imdb_votes"] > 5)
]

print(f"Removed movies with insufficient votes : {before - len(df):,}")

# ==========================================================
# Clean Text Columns
# ==========================================================

text_columns = [
    "title",
    "overview",
    "genres",
    "keywords",
    "cast",
    "director",
    "writers",
    "director_of_photography",
    "producers",
    "music_composer",
    "production_companies",
    "production_countries",
    "spoken_languages",
    "tagline",
    "certification_us"
]

for col in text_columns:

    df[col] = (
        df[col]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.strip()
    )
# ==========================================================
# Poster Path
# ==========================================================

df["poster_path"] = (
    df["poster_path"]
    .fillna("")
    .astype(str)
    .str.strip()
)

df["combined_features"] = (
    df["genres"].fillna("") + " " +
    df["keywords"].fillna("") + " " +
    df["director"].fillna("") + " " +
    df["cast"].fillna("") + " " +
    df["writers"].fillna("") + " " +
    df["overview"].fillna("")
)

# ==========================================================
# Sort Movies
# ==========================================================

df = df.sort_values(
    by="popularity",
    ascending=False
)

# ==========================================================
# Reset Index
# ==========================================================

df = df.reset_index(drop=True)


# ==========================================================
# Remove Unused Columns
# ==========================================================

df = df.drop(
    columns=[
        "status",
        "release_date",
        "vote_count",
        "imdb_votes",
        "overview",
        "original_language",
        "production_companies",
        "director_of_photography",
        "producers",
        "music_composer",
        "tagline",
        "certification_us",
        "popularity"
    ]
)

# ==========================================================
# Save Processed Dataset
# ==========================================================

print("\nSaving processed dataset...")

df.to_csv(
    CSV_OUTPUT,
    index=False
)

try:
    df.to_parquet(
        PARQUET_OUTPUT,
        index=False
    )
    print("Parquet saved successfully.")
except ImportError:
    print("Parquet not saved.")
    print("Install pyarrow:")
    print("pip install pyarrow")

# ==========================================================
# Summary
# ==========================================================

print("\n" + "=" * 60)
print("PREPROCESSING COMPLETE")
print("=" * 60)

print(f"Final movies : {len(df):,}")
print(f"Final columns: {len(df.columns)}")

memory = df.memory_usage(deep=True).sum() / (1024 ** 2)

print(f"Memory usage : {memory:.2f} MB")

print(f"\nCSV      : {CSV_OUTPUT}")
print(f"Parquet  : {PARQUET_OUTPUT}")