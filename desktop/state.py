from pathlib import Path


class AppState:

    def __init__(self):

        self.uploaded_zip_path: Path | None = None

        self.status_label = None

        self.progress = None

        self.recommendation_container = None

        self.stats_container = None


state = AppState()