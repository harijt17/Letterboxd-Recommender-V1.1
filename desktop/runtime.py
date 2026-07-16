from utils.paths import (
    UPLOADS_DIR,
    EXTRACTED_DIR,
)


# ==========================================================
# Runtime Initialization
# ==========================================================

def initialize_runtime():
    """
    Creates all runtime folders required by the application.
    """

    for directory in (
        UPLOADS_DIR,
        EXTRACTED_DIR,
    ):
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )