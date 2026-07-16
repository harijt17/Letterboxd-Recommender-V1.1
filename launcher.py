from nicegui import ui, native

from config.settings import WINDOW_TITLE
from desktop.runtime import initialize_runtime


@ui.page("/")
def root():

    # Runtime folders
    initialize_runtime()

    # Import after runtime initialization
    from desktop.app import build_app

    build_app()


ui.run(
    title=WINDOW_TITLE,
    reload=False,
    port=native.find_open_port(),
)