from pathlib import Path
import requests

from utils.paths import PROCESSED_DATA_DIR, TFIDF_DIR

# ==========================================================
# Runtime Assets
# ==========================================================

FILES = {
    "movies.parquet": {
        "url": "https://huggingface.co/datasets/harijt7/letterboxd-recommender-dataset/resolve/main/movies.parquet",
        "path": PROCESSED_DATA_DIR / "movies.parquet",
    },
    "vectorizer.joblib": {
        "url": "https://huggingface.co/datasets/harijt7/letterboxd-recommender-dataset/resolve/main/vectorizer.joblib",
        "path": TFIDF_DIR / "vectorizer.joblib",
    },
    "matrix.npz": {
        "url": "https://huggingface.co/datasets/harijt7/letterboxd-recommender-dataset/resolve/main/matrix.npz",
        "path": TFIDF_DIR / "matrix.npz",
    },
}

# ==========================================================
# Download Helper
# ==========================================================

def download_file(name: str, url: str, output: Path):

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if output.exists():
        print(f"✓ {name} already exists.")
        return

    print(f"Downloading {name}...")

    temp_file = output.with_suffix(output.suffix + ".tmp")

    try:
        with requests.get(
            url,
            stream=True,
            timeout=60,
        ) as response:

            response.raise_for_status()

            with open(temp_file, "wb") as file:

                for chunk in response.iter_content(
                    chunk_size=1024 * 1024
                ):
                    if chunk:
                        file.write(chunk)

        temp_file.replace(output)

        print(f"✓ Downloaded {name}")

    except Exception as e:

        if temp_file.exists():
            try:
                temp_file.unlink()
            except Exception:
                pass

        raise RuntimeError(
            f"Failed to download '{name}'.\n\n{e}"
        )

# ==========================================================
# Download Runtime Assets
# ==========================================================

def download_dataset():

    print("=" * 60)
    print("Checking runtime assets...")
    print("=" * 60)

    for name, info in FILES.items():

        download_file(
            name=name,
            url=info["url"],
            output=info["path"],
        )

    print("=" * 60)
    print("All runtime assets are ready.")
    print("=" * 60)

# ==========================================================
# Main
# ==========================================================

def main():
    download_dataset()


if __name__ == "__main__":
    main()