from pathlib import Path
import asyncio

from nicegui import ui

from core.recommendation_engine import RecommendationEngine
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

download_dataset()

engine = RecommendationEngine()


# ==========================================================
# Theme
# ==========================================================

setup_theme()


# ==========================================================
# Header
# ==========================================================

create_header()


# ==========================================================
# Upload Handler
# ==========================================================

async def handle_upload(e):

    upload_dir = Path("Data/uploads")

    upload_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # ------------------------------------------------------
    # Save destination
    # ------------------------------------------------------

    state.uploaded_zip_path = (
        upload_dir / e.file.name
    )

    # ------------------------------------------------------
    # Save uploaded file
    # ------------------------------------------------------

    await e.file.save(
        state.uploaded_zip_path
    )

    # ------------------------------------------------------
    # Update UI
    # ------------------------------------------------------

    state.status_label.set_text(
        "✓ Letterboxd Export Ready"
    )

    state.status_label.classes(
        remove="hidden",
        add="upload-status pop success-flash"
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
        "Analyzing profile..."
    )

    result = await asyncio.to_thread(
        engine.recommend,
        state.uploaded_zip_path,
    )

    state.progress.value = 1

    state.status_label.set_text(
        "Recommendations generated!"
    )

    show_stats(result)

    show_recommendations(
        result["recommendations"]
    )


# ==========================================================
# Upload Panel
# ==========================================================

create_upload_panel(
    handle_upload,
    generate_recommendations,
)


# ==========================================================
# Stats Area
# ==========================================================

state.stats_container = ui.column().classes(
    "w-full items-center mt-10"
)


# ==========================================================
# Recommendation Area
# ==========================================================

state.recommendation_container = ui.column().classes(
    "w-full items-center mt-10"
)


# ==========================================================
# Run Application
# ==========================================================

ui.run(
    title="Letterboxd Recommender",
    native=False,
    reload=False,
)