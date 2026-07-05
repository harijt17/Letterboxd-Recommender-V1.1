from pathlib import Path
import sys


def get_base_path() -> Path:
    """
    Returns the application's base directory.

    Source:
        Project Root

    PyInstaller:
        Folder containing the executable
    """

    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent

    return Path(__file__).resolve().parent.parent


BASE_DIR = get_base_path()

DATA_DIR = BASE_DIR / "Data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"
TFIDF_DIR = PROCESSED_DATA_DIR / "tfidf"
UPLOADS_DIR = BASE_DIR / "uploads"