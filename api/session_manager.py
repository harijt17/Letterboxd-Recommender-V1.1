from pathlib import Path
import shutil
import uuid
import json
from datetime import datetime

# ==========================================================
# Session Directory
# ==========================================================

SESSION_ROOT = (
    Path("uploads")
    / "sessions"
)

SESSION_ROOT.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================================
# Session Manager
# ==========================================================

class SessionManager:

    # ------------------------------------------------------
    # Create Session
    # ------------------------------------------------------

    def create_session(self):

        session_id = str(uuid.uuid4())

        session_folder = (
            SESSION_ROOT
            / session_id
        )

        session_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        return session_id, session_folder

    # ------------------------------------------------------
    # Existing Session
    # ------------------------------------------------------

    def get_session_folder(
        self,
        session_id
    ):

        folder = (
            SESSION_ROOT
            / session_id
        )

        if not folder.exists():

            raise FileNotFoundError(
                f"Session not found: {session_id}"
            )

        return folder

    # ------------------------------------------------------
    # Save Upload
    # ------------------------------------------------------

    def save_upload(
        self,
        session_id,
        upload_file
    ):

        folder = self.get_session_folder(
            session_id
        )

        zip_path = (
            folder
            / upload_file.filename
        )

        with open(
            zip_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                upload_file.file,
                buffer
            )

        return zip_path

    # ------------------------------------------------------
    # Save Object
    # ------------------------------------------------------

    def save_object(
        self,
        session_id,
        filename,
        obj
    ):

        import pickle

        folder = self.get_session_folder(
            session_id
        )

        with open(
            folder / filename,
            "wb"
        ) as file:

            pickle.dump(
                obj,
                file
            )
    # ==========================================================
    # Save Session Metadata
    # ==========================================================

    def save_metadata(
        self,
        session_id,
        metadata
    ):

        metadata["created_at"] = datetime.utcnow().isoformat()

        path = self.get_session_folder(session_id) / "session.json"

        with open(path, "w", encoding="utf-8") as f:

            json.dump(
                metadata,
                f,
                indent=4
            )


    # ------------------------------------------------------
    # Load Object
    # ------------------------------------------------------

    def load_object(
        self,
        session_id,
        filename
    ):

        import pickle

        folder = self.get_session_folder(
            session_id
        )

        with open(
            folder / filename,
            "rb"
        ) as file:

            return pickle.load(
                file
            )
        
    # ------------------------------------------------------
    # Load Session Metadata
    # ------------------------------------------------------

    def load_metadata(
        self,
        session_id
    ):

        folder = self.get_session_folder(
            session_id
        )

        with open(
            folder / "session.json",
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )

    # ------------------------------------------------------
    # Delete Session
    # ------------------------------------------------------

    def delete_session(
        self,
        session_id
    ):

        folder = (
            SESSION_ROOT
            / session_id
        )

        if folder.exists():

            shutil.rmtree(folder)