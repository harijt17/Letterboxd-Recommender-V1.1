from nicegui import ui


# ==========================================================
# Hero Header
# ==========================================================

def create_header():

    with ui.column().classes(
        "hero-section items-center w-full fade-in"
    ):

        # =====================================================
        # Title
        # =====================================================

        ui.label(
            "🎬 Letterboxd Recommender"
        ).classes(
            "hero-title"
        )

        # =====================================================
        # Subtitle
        # =====================================================

        ui.label(
            "Upload your Letterboxd export and discover movies you'll actually enjoy."
        ).classes(
            "hero-subtitle delay-1"
        )