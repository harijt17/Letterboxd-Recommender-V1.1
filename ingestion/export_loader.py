from pathlib import Path

import pandas as pd


class ExportLoader:

    def __init__(self, export_folder):

        self.export_folder = Path(export_folder)

    # =====================================================
    # Main Loader
    # =====================================================

    def load(self):

        ratings = self._load_csv("ratings.csv")
        reviews = self._load_csv("reviews.csv")
        diary = self._load_csv("diary.csv")

        # -------------------------------------------------
        # Merge Reviews
        # -------------------------------------------------

        if reviews is not None:

            ratings = ratings.merge(

                reviews[
                    [
                        "Letterboxd URI",
                        "Review"
                    ]
                ],

                on="Letterboxd URI",

                how="left"

            )

        else:

            ratings["Review"] = None

        # -------------------------------------------------
        # Merge Diary
        # -------------------------------------------------

        if diary is not None:

            ratings = ratings.merge(

                diary[
                    [
                        "Letterboxd URI",
                        "Watched Date",
                        "Rewatch",
                        "Tags"
                    ]
                ],

                on="Letterboxd URI",

                how="left"

            )

        else:

            ratings["Watched Date"] = None
            ratings["Rewatch"] = None
            ratings["Tags"] = None

        # -------------------------------------------------
        # Rename Columns
        # -------------------------------------------------

        ratings = ratings.rename(

            columns={

                "Name": "title",

                "Year": "year",

                "Rating": "rating",

                "Review": "review",

                "Watched Date": "watched_date",

                "Rewatch": "rewatch",

                "Tags": "tags",

                "Letterboxd URI": "uri"

            }

        )

        # -------------------------------------------------
        # Remove Unused Columns
        # -------------------------------------------------

        ratings = ratings.drop(

            columns=[
                "Date"
            ],

            errors="ignore"

        )

        # -------------------------------------------------
        # Convert Data Types
        # -------------------------------------------------

        ratings["rating"] = pd.to_numeric(

            ratings["rating"],

            errors="coerce"

        )

        ratings["year"] = (

            pd.to_numeric(

                ratings["year"],

                errors="coerce"

            )

            .fillna(0)

            .astype(int)

        )

        # -------------------------------------------------
        # Fill Missing Values
        # -------------------------------------------------

        ratings["review"] = ratings["review"].fillna("")

        ratings["tags"] = ratings["tags"].fillna("")

        ratings["rewatch"] = ratings["rewatch"].fillna(False)

        ratings["watched_date"] = pd.to_datetime(

            ratings["watched_date"],

            errors="coerce"

        )

        ratings["watched_date"] = ratings["watched_date"].apply(

            lambda x: x.strftime("%Y-%m-%d")

            if pd.notna(x)

            else None

        )

        # -------------------------------------------------
        # Replace Remaining NaN with None
        # -------------------------------------------------

        ratings = ratings.where(

            pd.notna(ratings),

            None

        )

        # -------------------------------------------------
        # Return Python Objects
        # -------------------------------------------------

        return ratings.to_dict("records")

    # =====================================================
    # Load CSV Helper
    # =====================================================

    def _load_csv(

        self,

        filename

    ):

        file = self.export_folder / filename

        if not file.exists():

            return None

        return pd.read_csv(

            file,

            low_memory=False

        )