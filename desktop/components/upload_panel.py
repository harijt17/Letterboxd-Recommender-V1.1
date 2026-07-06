from nicegui import ui

from desktop.state import state


# ==========================================================
# Upload Panel
# ==========================================================

def create_upload_panel(
    handle_upload,
    generate_recommendations,
):

    with ui.column().classes(
        "items-center w-full mt-4 mb-10 fade-in"
    ):

        # =====================================================
        # Upload Card
        # =====================================================

        with ui.card().classes(
            "upload-box glow scale-in"
        ):

            with ui.column().classes(
                "items-center w-full"
            ):

                # ---------------------------------------------
                # Upload Icon
                # ---------------------------------------------

                ui.icon(
                    "cloud_upload"
                ).classes(
                    "upload-icon float"
                )

                # ---------------------------------------------
                # Title
                # ---------------------------------------------

                ui.label(
                    "Drop your Letterboxd Export"
                ).classes(
                    "upload-title"
                )

                # ---------------------------------------------
                # Subtitle
                # ---------------------------------------------

                ui.label(
                    "Drag & drop your exported ZIP here\nor click below to browse."
                ).classes(
                    "upload-subtitle"
                )

                # ---------------------------------------------
                # Upload Control
                # ---------------------------------------------

                ui.upload(
                    on_upload=handle_upload,
                    auto_upload=False,
                ).props(
                    'accept=".zip"'
                ).classes(
                    "custom-upload"
                )

        # =====================================================
        # Upload Status
        # =====================================================

        state.status_label = ui.label().classes(
            "upload-status pop"
        )

        # =====================================================
        # Progress
        # =====================================================

        state.progress = ui.linear_progress(
            value=0
        ).classes(
            "progress-bar"
        )

        state.progress.visible = False

        # =====================================================
        # Generate Button
        # =====================================================

        ui.button(
            "✨ Generate Recommendations",
            on_click=generate_recommendations,
        ).classes(
            "gradient-button button-press mt-5"
        )