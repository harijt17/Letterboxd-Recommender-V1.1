import asyncio

from nicegui import ui

from core.recommendation_engine import RecommendationEngine
from desktop.runtime import UPLOADS_DIR
from download_dataset import download_dataset

from desktop.state import state
from desktop.theme import setup_theme

from desktop.components.header import create_header
from desktop.components.upload_panel import create_upload_panel
from desktop.components.stats_panel import show_stats
from desktop.components.recommendation_list import show_recommendations


# ==========================================================
# Backend Initialization
# ==========================================================
engine = None


# ==========================================================
# Upload Handler
# ==========================================================

async def handle_upload(e):

    from desktop.runtime import UPLOADS_DIR

    state.uploaded_zip_path = (
        UPLOADS_DIR / e.file.name
    )

    await e.file.save(
        state.uploaded_zip_path
    )

    state.status_label.set_text(
        "✓ Letterboxd Export Ready"
    )

    state.status_label.classes(
        remove="hidden",
        add="upload-status pop success-flash",
    )


# ==========================================================
# Recommendation Pipeline
# ==========================================================

async def generate_recommendations():

    if state.uploaded_zip_path is None:

        ui.notify(
            "Please upload your Letterboxd export ZIP.",
            color="negative",
        )

        return

    state.progress.visible = True
    state.progress.value = 0.20

    state.status_label.set_text(
        "Analyzing your profile..."
    )

    # ------------------------------------------------------
    # Generate Recommendations
    # ------------------------------------------------------

    result = await asyncio.to_thread(
        engine.recommend,
        state.uploaded_zip_path,
    )

    # ------------------------------------------------------
    # Update Progress
    # ------------------------------------------------------

    state.progress.value = 1.0

    state.status_label.set_text(
        "Recommendations generated!"
    )

    # ------------------------------------------------------
    # Display Results
    # ------------------------------------------------------

    show_stats(result)

    show_recommendations(
        result["recommendations"]
    )

    # ------------------------------------------------------
    # Hide Progress Bar
    # ------------------------------------------------------

    await asyncio.sleep(0.3)

    state.progress.visible = False


# ==========================================================
# Build Application
# ==========================================================

def build_app():

    global engine

    # ------------------------------------------------------
    # Backend Initialization (Only Once)
    # ------------------------------------------------------

    if engine is None:

        download_dataset()

        engine = RecommendationEngine()

    # ------------------------------------------------------
    # Theme
    # ------------------------------------------------------

    setup_theme()

    # ------------------------------------------------------
    # Header
    # ------------------------------------------------------

    create_header()

    # ------------------------------------------------------
    # Upload Panel
    # ------------------------------------------------------

    create_upload_panel(
        handle_upload,
        generate_recommendations,
    )

    # ------------------------------------------------------
    # Statistics Section
    # ------------------------------------------------------

    state.stats_container = ui.column().classes(
        "w-full items-center mt-10"
    )

    # ------------------------------------------------------
    # Recommendation Section
    # ------------------------------------------------------

    state.recommendation_container = ui.column().classes(
        "w-full items-center mt-10"
    )