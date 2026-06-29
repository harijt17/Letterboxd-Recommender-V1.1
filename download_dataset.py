from pathlib import Path
import urllib.request

DATASET_URL = (
    "https://huggingface.co/datasets/harijt7/"
    "letterboxd-recommender-dataset/resolve/main/"
    "movies.parquet"
)

OUTPUT_PATH = (
    Path("Data")
    / "processed"
    / "movies.parquet"
)


def main():

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if OUTPUT_PATH.exists():

        print("Dataset already exists.")
        return

    print("Downloading processed dataset...")

    urllib.request.urlretrieve(
        DATASET_URL,
        OUTPUT_PATH
    )

    print("Download complete!")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()