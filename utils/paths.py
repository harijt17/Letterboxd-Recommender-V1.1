from pathlib import Path
import os
import sys


# ==========================================================
# Base Paths
# ==========================================================

def get_base_path() -> Path:
    """
    Returns the application's base directory.

    Development:
        Project Root

    Packaged:
        Folder containing the executable
    """

    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent

    return Path(__file__).resolve().parent.parent


BASE_DIR = get_base_path()


# ==========================================================
# Data Directory
# ==========================================================

def get_data_directory() -> Path:

    data_dir = (
        Path(os.environ["LOCALAPPDATA"])
        / "Letterboxd Recommender"
    )

    data_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    return data_dir


DATA_DIR = get_data_directory()

# ==========================================================
# Runtime Directories
# ==========================================================

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

TFIDF_DIR = PROCESSED_DATA_DIR / "tfidf"

UPLOADS_DIR = DATA_DIR / "uploads"

EXTRACTED_DIR = DATA_DIR / "extracted"

# ==========================================================
# Create Directories
# ==========================================================

for folder in (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    TFIDF_DIR,
    UPLOADS_DIR,
    EXTRACTED_DIR,
):
    folder.mkdir(
        parents=True,
        exist_ok=True,
    )