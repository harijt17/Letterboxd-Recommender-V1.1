from pathlib import Path
import pandas as pd


class ExportValidator:
    """
    Validates an extracted Letterboxd export folder.
    """

    REQUIRED_FILES = [
        "ratings.csv",
        "reviews.csv",
        "diary.csv",
        "watched.csv",
        "profile.csv"
    ]

    REQUIRED_COLUMNS = {
        "ratings.csv": [
            "Name",
            "Year",
            "Rating",
            "Letterboxd URI"
        ],

        "reviews.csv": [
            "Name",
            "Year",
            "Review",
            "Letterboxd URI"
        ],

        "diary.csv": [
            "Name",
            "Year",
            "Watched Date",
            "Letterboxd URI"
        ],

        "watched.csv": [
            "Name",
            "Year",
            "Letterboxd URI"
        ],

        "profile.csv": [
            "Given Name"
        ]
    }

    # =====================================================
    # Main Validation
    # =====================================================

    def validate(self, folder):

        folder = Path(folder)

        if not folder.exists():
            raise FileNotFoundError(
                f"Folder not found:\n{folder}"
            )

        self._check_required_files(folder)

        self._check_required_columns(folder)

        return True

    # =====================================================
    # Check Required Files
    # =====================================================

    def _check_required_files(self, folder):

        missing = []

        for filename in self.REQUIRED_FILES:

            file = folder / filename

            if not file.exists():
                missing.append(filename)

        if missing:

            raise FileNotFoundError(

                "Missing required files:\n"

                + "\n".join(missing)

            )

    # =====================================================
    # Check Required Columns
    # =====================================================

    def _check_required_columns(self, folder):

        for filename, columns in self.REQUIRED_COLUMNS.items():

            file = folder / filename

            df = pd.read_csv(
                file,
                nrows=5
            )

            missing_columns = [

                col

                for col in columns

                if col not in df.columns

            ]

            if missing_columns:

                raise ValueError(

                    f"{filename} is missing columns:\n"

                    + ", ".join(missing_columns)

                )

    # =====================================================
    # Summary
    # =====================================================

    def summary(self, folder):

        folder = Path(folder)

        print("=" * 60)
        print("LETTERBOXD EXPORT VALIDATION")
        print("=" * 60)

        for file in sorted(folder.glob("*.csv")):

            df = pd.read_csv(
                file,
                nrows=5
            )

            print(f"{file.name:<15} OK")