"""Module for testing main routes."""

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_route(client: AsyncClient) -> None:
    """Test the root route of the application.

    Args:
        client (AsyncClient): The async httpx Client fixture for making requests.
    """
    response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert isinstance(response_data, dict)
