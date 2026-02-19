"""Module for testing access group routes."""
import pytest
from uuid import uuid4
from fastapi import status
from httpx import AsyncClient

from src.exceptions.access_groups import (
    EmailAlreadyInUseException,
    AccessGroupNotFoundException,
    AccessGroupIdUUIDException
)
from src.schema.access_groups import AccessGroupResponse


@pytest.mark.asyncio
async def test_create_access_group(client: AsyncClient) -> None:
    """Test user creation endpoint.

    Args:
        client (AsyncClient): The async httpx Client fixture for making requests.
    """
    data = {
        "name": "Test Access Group",
        "email": "accessgroup@example.com",
        "password": "securepassword123"
    }
    response = await client.post("/access-groups/", json=data)

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data["name"] == data["name"]
    assert response_data["email"] == data["email"]
    assert AccessGroupResponse(**response_data)


@pytest.mark.asyncio
async def test_create_access_group_with_existing_email(client: AsyncClient) -> None:
    """Test creating an access group with an email that already exists.

    Args:
        client (AsyncClient): The async httpx Client fixture for making requests.
    """
    data = {
        "name": "Test Access Group",
        "email": "accessgroup@example.com",
        "password": "securepassword123"
    }
    response = await client.post("/access-groups/", json=data)

    assert response.status_code == EmailAlreadyInUseException.STATUS_CODE
    assert response.json()["detail"] == EmailAlreadyInUseException.DETAIL.format(email=data["email"])


@pytest.mark.asyncio
async def test_get_all_access_groups(client: AsyncClient) -> None:
    """Test retrieving all access groups.

    Args:
        client (AsyncClient): The async httpx Client fixture for making requests.
    """
    response = await client.get("/access-groups/")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_access_group_by_id(client: AsyncClient) -> None:
    """Test retrieving an access group by ID.

    Args:
        client (AsyncClient): The async httpx Client fixture for making requests.
    """
    data = {
        "name": "Test Get Access Group",
        "email": "accessgroupget@example.com",
        "password": "securepassword123"
    }
    response = await client.post("/access-groups/", json=data)
    assert response.status_code == status.HTTP_201_CREATED

    access_groups = response.json()
    group_id = access_groups["id"]
    
    response = await client.get(f"/access-groups/by-id?id={group_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == group_id


@pytest.mark.asyncio
async def test_get_access_group_by_id_not_found(client: AsyncClient) -> None:
    """Test retrieving an access group by ID that does not exist.

    Args:
        client (AsyncClient): The async httpx Client fixture for making requests.
    """
    id = str(uuid4())
    response = await client.get(f"/access-groups/by-id?id={id}")
    
    assert response.status_code == AccessGroupNotFoundException.STATUS_CODE
    assert response.json()["detail"] == AccessGroupNotFoundException.DETAIL.format(id=id)


@pytest.mark.asyncio
async def test_get_access_group_by_id_invalid_uuid(client: AsyncClient) -> None:
    """Test retrieving an access group by ID with an invalid UUID.

    Args:
        client (AsyncClient): The async httpx Client fixture for making requests.
    """
    invalid_id = "invalid-uuid"
    response = await client.get(f"/access-groups/by-id?id={invalid_id}")
    
    assert response.status_code == AccessGroupIdUUIDException.STATUS_CODE
    assert response.json()["detail"] == AccessGroupIdUUIDException.DETAIL
