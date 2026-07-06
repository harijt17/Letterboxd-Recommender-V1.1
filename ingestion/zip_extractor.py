from pathlib import Path
import shutil
import zipfile


class ZipExtractor:
    """
    Extracts a Letterboxd export ZIP into a temporary folder.

    Data/
        extracted/
            desktop/
                ratings.csv
                reviews.csv
                diary.csv
                ...
    """

    def __init__(self, extract_root="Data/extracted"):

        self.extract_root = Path(extract_root)

        self.extract_root.mkdir(
            parents=True,
            exist_ok=True
        )

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

        if extract_folder.exists():
            shutil.rmtree(extract_folder)

        extract_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        try:

            with zipfile.ZipFile(
                zip_path,
                "r"
            ) as zip_ref:

                zip_ref.extractall(
                    extract_folder
                )

        except zipfile.BadZipFile:

            shutil.rmtree(
                extract_folder,
                ignore_errors=True
            )

            raise ValueError(
                "Invalid or corrupted ZIP file."
            )

        return extract_folder

    # =====================================================
    # Cleanup
    # =====================================================

    def cleanup(self):

        folder = (
            self.extract_root /
            "desktop"
        )

        if folder.exists():
            shutil.rmtree(folder)