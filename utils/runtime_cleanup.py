from pathlib import Path
import shutil

from utils.paths import (
    UPLOADS_DIR,
    EXTRACTED_DIR,
)


# ==========================================================
# Temporary Runtime Directories
# ==========================================================

TEMP_DIRECTORIES = (
    UPLOADS_DIR,
    EXTRACTED_DIR,
)


# ==========================================================
# Clear Directory
# ==========================================================

def clear_directory(directory: Path) -> None:
    """
    Deletes everything inside a directory while
    preserving the directory itself.
    """

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    for item in directory.iterdir():

        try:

            if item.is_dir():
                shutil.rmtree(item)

            else:
                item.unlink()

        except Exception as e:

            print(f"Warning: Could not delete '{item}'")
            print(e)


# ==========================================================
# Runtime Cleanup
# ==========================================================

def cleanup_runtime() -> None:
    """
    Removes all temporary runtime files.
    """

    print("Cleaning runtime workspace...")

    for directory in TEMP_DIRECTORIES:
        clear_directory(directory)

    print("Runtime workspace ready.")