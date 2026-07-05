from pathlib import Path
import shutil

from nicegui import ui

from core.recommendation_engine import RecommendationEngine
from download_dataset import download_dataset


# ==========================================================
# Backend Initialization
# ==========================================================

download_dataset()
engine = RecommendationEngine()

recommendation_container = None
status_label = None
progress = None

# ==========================================================
# Theme
# ==========================================================

ui.dark_mode().enable()

ui.colors(
    primary="#ef4444",
    secondary="#111827",
)


# ==========================================================
# Header
# ==========================================================

with ui.column().classes("w-full items-center"):

    ui.label("🎬 Letterboxd Recommender").classes(
        "text-5xl font-bold mt-8"
    )

    ui.label(
        "Upload your Letterboxd export ZIP and receive personalized recommendations."
    ).classes(
        "text-lg text-gray-400 mb-8"
    )

recommendation_container = ui.column().classes(
    "w-full items-center mt-8"
)

# ==========================================================
# Upload Card
# ==========================================================

uploaded_zip_path = None


async def handle_upload(e):

    global uploaded_zip_path

    upload_dir = Path("Data/uploads")
    upload_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    uploaded_zip_path = (
        upload_dir / e.file.name
    )

    await e.file.save(uploaded_zip_path)

    status_label.set_text(
        f"Selected: {e.file.name}"
    )

    ui.notify(
        "ZIP uploaded successfully!",
        color="positive"
    )

def show_movies(df):

    recommendation_container.clear()

    with recommendation_container:

        ui.label(
            "🎬 Top Recommendations"
        ).classes(
            "text-3xl font-bold mb-6"
        )

        for _, movie in df.iterrows():

            poster = (
                "https://image.tmdb.org/t/p/w342"
                + movie["poster_path"]
                if movie["poster_path"]
                else "https://placehold.co/342x513?text=No+Poster"
            )

            with ui.card().classes(
                "w-[900px] mb-6"
            ):

                with ui.row().classes("w-full"):

                    ui.image(
                        poster
                    ).classes(
                        "w-48"
                    )

                    with ui.column().classes(
                        "ml-6"
                    ):

                        ui.label(
                            f"{movie['title'].title()} ({movie['year']})"
                        ).classes(
                            "text-2xl font-bold"
                        )

                        ui.label(
                            f"🎬 Director: {movie['director']}"
                        )

                        ui.label(
                            f"🎭 Genres: {movie['genres']}"
                        )

                        ui.linear_progress(
                            value=float(
                                movie["recommendation_score"]
                            )
                        ).classes(
                            "w-96"
                        )

                        ui.label(
                            f"Score: {movie['recommendation_score']:.4f}"
                        )


def generate_recommendations():

    global uploaded_zip_path

    if uploaded_zip_path is None:

        ui.notify(
            "Please upload your Letterboxd export ZIP.",
            color="negative"
        )

        return

    progress.visible = True
    progress.value = 0.2

    status_label.set_text(
        "Analyzing profile..."
    )

    result = engine.recommend(uploaded_zip_path)

    progress.value = 1

    status_label.set_text(
        "Recommendations generated!"
    )

    print(result.keys())
    print(result["movies_loaded"])
    print(result["movies_matched"])
    print(result["movies_unmatched"])
    print(result["recommendations"][:3])

    recommendations = result["recommendations"]
    
    show_movies(recommendations)

with ui.card().classes("w-[700px] p-8"):

    ui.upload(
        on_upload=handle_upload,
        auto_upload=False,
    ).props(
        'accept=".zip"'
    )

    ui.separator()

    status_label = ui.label()

    progress = ui.linear_progress(
        value=0
    ).classes("w-full")

    progress.visible = False

    ui.button(
        "Generate Recommendations",
        on_click=generate_recommendations,
    ).classes(
        "w-full mt-4"
    )

# ==========================================================
# Run Application
# ==========================================================

ui.run(
    title="Letterboxd Recommender",
    native=False,
    reload=False,
)