"""Settings for the database."""

from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Class for the database settings."""

    CONN_URL: str = "sqlite+aiosqlite:///src/database/data/db.sql"


database_settings = DatabaseSettings()
