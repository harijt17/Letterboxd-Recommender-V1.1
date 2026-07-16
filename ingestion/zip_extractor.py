from pathlib import Path
import shutil
import zipfile

from desktop.runtime import EXTRACTED_DIR

class ZipExtractor:
    """
    Extracts a Letterboxd export ZIP.

    Runtime Structure:

    Data/
        extracted/
            desktop/
                ratings.csv
                reviews.csv
                diary.csv
                ...
    """

    def __init__(self):

        self.extract_root = EXTRACTED_DIR

        
    # =====================================================
    # Extract ZIP
    # =====================================================

    def extract(self, zip_path):

        zip_path = Path(zip_path)

        if not zip_path.exists():

            raise FileNotFoundError(
                f"ZIP file not found:\n{zip_path}"
            )

        if zip_path.suffix.lower() != ".zip":

            raise ValueError(
                "Only ZIP files are supported."
            )

        extract_folder = (
            self.extract_root /
            "desktop"
        )

        # -------------------------------------------------
        # Clean previous extraction
        # -------------------------------------------------

        if extract_folder.exists():

            shutil.rmtree(
                extract_folder
            )

        extract_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        # -------------------------------------------------
        # Extract ZIP
        # -------------------------------------------------

        try:

            with zipfile.ZipFile(
                zip_path,
                "r",
            ) as zip_ref:

                zip_ref.extractall(
                    extract_folder
                )

        except zipfile.BadZipFile:

            shutil.rmtree(
                extract_folder,
                ignore_errors=True,
            )

            raise ValueError(
                "Invalid or corrupted ZIP file."
            )

        return extract_folder

    # =====================================================
    # Cleanup
    # =====================================================

    def cleanup(self):

        extract_folder = (
            self.extract_root /
            "desktop"
        )

        if extract_folder.exists():

            shutil.rmtree(
                extract_folder,
                ignore_errors=True,
            )