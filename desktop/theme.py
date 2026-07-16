from desktop.resources import resource_path
from nicegui import ui


# ==========================================================
# Theme
# ==========================================================

def setup_theme():

    # ------------------------------------------------------
    # Dark Mode
    # ------------------------------------------------------

    ui.dark_mode().enable()

    # ------------------------------------------------------
    # Color Palette
    # ------------------------------------------------------

    ui.colors(

        primary="#2B7FFF",

        secondary="#0F172A",

        accent="#1F6FE5",

        positive="#22C55E",

        negative="#EF4444",

        warning="#F59E0B",

        info="#38BDF8",

        dark="#020617",

    )

    # ------------------------------------------------------
    # Global CSS
    # ------------------------------------------------------

    ui.add_css(
        resource_path(
            "desktop",
            "assets",
            "styles.css",
        ).read_text(
            encoding="utf-8"
        )
    )

    ui.add_css(
        resource_path(
            "desktop",
            "assets",
            "components.css",
        ).read_text(
            encoding="utf-8"
        )
    )

    ui.add_css(
        resource_path(
            "desktop",
            "assets",
            "animations.css",
        ).read_text(
            encoding="utf-8"
        )
    )