from pathlib import Path
import shutil
import zipfile


class ZipExtractor:
    """
    Handles extraction of Letterboxd export ZIP files.

    Data/
        extracted/
            <session_id>/
                ratings.csv
                reviews.csv
                diary.csv
                watched.csv
                watchlist.csv
                comments.csv
                profile.csv
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

    def extract(
        self,
        zip_path,
        session_id
    ):

        zip_path = Path(zip_path)

        if not zip_path.exists():
            raise FileNotFoundError(
                f"ZIP file not found:\n{zip_path}"
            )

        if zip_path.suffix.lower() != ".zip":
            raise ValueError(
                "Only ZIP files are supported."
            )

        session_folder = (
            self.extract_root /
            session_id
        )

        # Remove old session if it exists
        if session_folder.exists():
            shutil.rmtree(session_folder)

        session_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        try:

            with zipfile.ZipFile(
                zip_path,
                "r"
            ) as zip_ref:

                zip_ref.extractall(
                    session_folder
                )

        except zipfile.BadZipFile:

            shutil.rmtree(
                session_folder,
                ignore_errors=True
            )

            raise ValueError(
                "Invalid or corrupted ZIP file."
            )

        return session_folder

    # =====================================================
    # Session Folder
    # =====================================================

    def get_session_folder(
        self,
        session_id
    ):

        folder = (
            self.extract_root /
            session_id
        )

        if not folder.exists():
            raise FileNotFoundError(
                f"Session '{session_id}' not found."
            )

        return folder

    # =====================================================
    # Get File
    # =====================================================

    def get_file(
        self,
        session_id,
        filename
    ):

        file = (
            self.extract_root /
            session_id /
            filename
        )

        if not file.exists():
            return None

        return file

    # =====================================================
    # List Files
    # =====================================================

    def list_files(
        self,
        session_id
    ):

        folder = self.get_session_folder(
            session_id
        )

        return sorted(
            file.name
            for file in folder.iterdir()
            if file.is_file()
        )

    # =====================================================
    # Session Exists
    # =====================================================

    def session_exists(
        self,
        session_id
    ):

        return (
            self.extract_root /
            session_id
        ).exists()

    # =====================================================
    # Cleanup Session
    # =====================================================

    def cleanup(
        self,
        session_id
    ):

        folder = (
            self.extract_root /
            session_id
        )

        if folder.exists():
            shutil.rmtree(folder)

    # =====================================================
    # Cleanup All
    # =====================================================

    def cleanup_all(self):

        if self.extract_root.exists():

            shutil.rmtree(
                self.extract_root
            )

            self.extract_root.mkdir(
                parents=True,
                exist_ok=True
            )