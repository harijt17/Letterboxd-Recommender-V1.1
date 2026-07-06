from nicegui import ui


# ==========================================================
# Movie Card
# ==========================================================

def create_movie_card(movie):

    # ------------------------------------------------------
    # Poster
    # ------------------------------------------------------

    poster_path = movie.get("poster_path")

    if (
        poster_path is not None
        and str(poster_path) != "nan"
        and str(poster_path).strip() != ""
    ):

        poster = (
            "https://image.tmdb.org/t/p/w500"
            + str(poster_path)
        )

    else:

        poster = (
            "https://placehold.co/500x750?text=No+Poster"
        )

    # ------------------------------------------------------
    # Overview
    # ------------------------------------------------------

    overview = str(
        movie.get(
            "overview",
            ""
        )
    )

    if overview == "nan":
        overview = ""

    if len(overview) > 220:
        overview = overview[:220] + "..."

    # ------------------------------------------------------
    # Card
    # ------------------------------------------------------

    with ui.card().classes(
        "movie-card-horizontal fade-in hover-lift"
    ):

        with ui.row().classes(
            "w-full no-wrap"
        ):

            # ==============================================
            # Poster
            # ==============================================

            ui.image(
                poster
            ).classes(
                "movie-poster-horizontal hover-scale"
            )

            # ==============================================
            # Right Side
            # ==============================================

            with ui.column().classes(
                "movie-content"
            ):

                # ------------------------------------------
                # Title
                # ------------------------------------------

                ui.label(
                    f"{movie['title'].title()} ({movie['year']})"
                ).classes(
                    "movie-title-horizontal"
                )

                # ------------------------------------------
                # Chips
                # ------------------------------------------

                with ui.row().classes(
                    "items-center gap-2 mt-3"
                ):

                    if movie.get("imdb_rating"):

                        ui.label(
                            f"⭐ {movie['imdb_rating']}"
                        ).classes(
                            "imdb-chip pop"
                        )

                    ui.label(
                        f"👍 {movie['display_score']}% Match"
                    ).classes(
                        "match-chip pop"
                    )

                ui.separator().classes(
                    "my-3 opacity-20"
                )

                # ------------------------------------------
                # Metadata
                # ------------------------------------------

                ui.label(
                    f"🎭  {movie['genres']}"
                ).classes(
                    "movie-genre-horizontal"
                )

                ui.label(
                    f"🎬  {movie['director']}"
                ).classes(
                    "movie-director-horizontal"
                )

                runtime = movie.get("runtime")

                if runtime:

                    ui.label(
                        f"⏱️  {runtime} min"
                    ).classes(
                        "movie-runtime"
                    )

                language = movie.get(
                    "original_language"
                )

                if language:

                    ui.label(
                        f"🌍  {str(language).upper()}"
                    ).classes(
                        "movie-language"
                    )

                ui.separator().classes(
                    "my-3 opacity-20"
                )

                # ------------------------------------------
                # Overview
                # ------------------------------------------

                if overview:

                    ui.label(
                        overview
                    ).classes(
                        "movie-overview"
                    )