from utils.paths import (
    UPLOADS_DIR,
    EXTRACTED_DIR,
)

from utils.runtime_cleanup import cleanup_runtime


# ==========================================================
# Runtime Initialization
# ==========================================================

def initialize_runtime():
    """
    Initializes the runtime environment.

    - Creates required runtime folders.
    - Cleans temporary runtime data.
    """

    for directory in (
        UPLOADS_DIR,
        EXTRACTED_DIR,
    ):
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    cleanup_runtime()