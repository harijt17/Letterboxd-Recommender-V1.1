import pandas as pd

# ---------------------------------------
# Load processed dataset
# ---------------------------------------

df = pd.read_csv(
    "Data/raw/The Ultimate 1Million Movies Dataset (TMDB + IMDb).csv",
    low_memory=False
)

print("=" * 60)
print("Dataset Loaded")
print("=" * 60)
print(f"Total Movies : {len(df):,}")

print()

# ---------------------------------------
# Search for Ponniyin Selvan
# ---------------------------------------

movie = df[
    df["title"].str.contains(
        "ponniyin",
        case=False,
        na=False
    )
]

print("=" * 60)
print("Search Results")
print("=" * 60)

movie = df[
    df["title"].str.contains(
        "ponniyin",
        case=False,
        na=False
    )
]

print(movie.to_string())