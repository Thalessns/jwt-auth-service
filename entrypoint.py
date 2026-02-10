"""Entrypoint for the service."""
import uvicorn

from src.app.settings import entry_settings


def start_app():
    """Starts the application."""

    uvicorn.run(
        app="src.app.main:app",
        host=entry_settings.APP_HOST,
        port=entry_settings.APP_PORT,
        reload=entry_settings.APP_RELOAD
    )


if __name__ == "__main__":
    start_app()
