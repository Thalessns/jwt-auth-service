"""Settings for the database."""


class DatabaseSettings:
    """Class for the database settings."""

    conn_url: str = "sqlite+aiosqlite:///src/database/data/db.sql"


database_settings = DatabaseSettings()
