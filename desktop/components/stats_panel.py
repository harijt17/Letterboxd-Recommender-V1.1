from nicegui import ui

from desktop.state import state


# ==========================================================
# Stats Panel
# ==========================================================

def show_stats(result):

    if state.stats_container is None:
        return

    state.stats_container.clear()

    with state.stats_container:

        ui.label(
            "Profile Summary"
        ).classes(
            "text-3xl font-bold mb-8 fade-in"
        )

        with ui.row().classes(
            "justify-center gap-8 w-full mb-10 flex-wrap"
        ):

            create_stat_card(
                "Movies Loaded",
                result["movies_loaded"],
                "🎬",
                "delay-1",
            )

            create_stat_card(
                "Movies Matched",
                result["movies_matched"],
                "✅",
                "delay-2",
            )

            create_stat_card(
                "Recommendations",
                len(result["recommendations"]),
                "⭐",
                "delay-3",
            )


# ==========================================================
# Individual Stat Card
# ==========================================================

def create_stat_card(
    title,
    value,
    icon,
    delay,
):

    with ui.card().classes(
        f"stats-card slide-up {delay}"
    ):

        ui.label(
            icon
        ).classes(
            "text-4xl mb-2"
        )

        ui.label(
            str(value)
        ).classes(
            "text-4xl font-bold"
        )

        ui.label(
            title
        ).classes(
            "text-muted text-lg mt-2"
        )