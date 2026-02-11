"""Settings for the application."""

from pydantic_settings import BaseSettings


class EntryPointSettings(BaseSettings):
    """Settings for the app entrypoint."""

    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 5001
    APP_RELOAD: bool = False


class JwtSettings(BaseSettings):
    """Settings for the jwt tokens."""

    JWT_KEY: str = "foo"
    JWT_ALGORITHM: str = "HS256"
    JWT_VALID_TIME: int = 120


entry_settings = EntryPointSettings()
jwt_settings = JwtSettings()
