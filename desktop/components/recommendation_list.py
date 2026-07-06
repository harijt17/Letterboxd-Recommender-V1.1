from nicegui import ui

from desktop.state import state
from desktop.components.movie_card import create_movie_card


def show_recommendations(df):

    state.recommendation_container.clear()

    with state.recommendation_container:

        ui.label(
            "Your Recommendations"
        ).classes(
            "text-4xl font-bold mb-8 fade-in"
        )

        with ui.row().classes(
            "justify-center items-start w-full gap-8 flex-wrap"
        ):

            for _, movie in df.iterrows():

                create_movie_card(movie)