"""Conftest module for pytest configuration."""
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

from src.app.main import app
from src.app.settings import entry_settings

app_url = f"http://{entry_settings.APP_HOST}:{entry_settings.APP_PORT}/api"


@pytest_asyncio.fixture(scope="session")
async def client():
    """Fixture for the async HTTP client with lifespan management."""
    async with LifespanManager(app) as manager:
        async with AsyncClient(transport=ASGITransport(app=manager.app), base_url=app_url) as http_client:
            yield http_client
