import requests
import os

# ==========================================================
# API Configuration
# ==========================================================

API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000"
)


# ==========================================================
# Upload Letterboxd Export
# ==========================================================

def upload_export(file):

    files = {
        "file": (
            file.name,
            file,
            "application/zip"
        )
    }

    response = requests.post(
        f"{API_URL}/upload",
        files=files
    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Get Recommendations
# ==========================================================

def get_recommendations(session_id):

    response = requests.get(
        f"{API_URL}/recommend/{session_id}"
    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Get Session Information
# ==========================================================

def get_session(session_id):

    response = requests.get(
        f"{API_URL}/session/{session_id}"
    )

    response.raise_for_status()

    return response.json()