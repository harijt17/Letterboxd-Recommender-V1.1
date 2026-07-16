from pathlib import Path
import sys


def app_root() -> Path:
    """
    Returns the application's resource directory.

    Development:
        Project root

    PyInstaller:
        executable/_internal

    Nuitka:
        executable directory
    """

    if getattr(sys, "frozen", False):

        exe_dir = Path(sys.executable).parent

        return (
            exe_dir / "_internal"
            if (exe_dir / "_internal").exists()
            else exe_dir
        )

    return Path(__file__).resolve().parent.parent


def resource_path(*parts: str) -> Path:
    return app_root().joinpath(*parts)