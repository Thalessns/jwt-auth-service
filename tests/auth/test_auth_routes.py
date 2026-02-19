"""Module for testing auth routes."""

import pytest
from fastapi import status
from httpx import AsyncClient
from freezegun import freeze_time
from datetime import timedelta

from src.exceptions.access_groups import InvalidCredentialsException
from src.exceptions.auth import ExpiredTokenException, InvalidTokenException
from src.schema.auth import JwtResponse


@pytest.mark.asyncio
async def test_create_jwt(client: AsyncClient) -> None:
    """Test creating a JWT token.

    Args:
        client (AsyncClient): The async httpx Client fixture for making requests.
    """
    group_data = {
        "name": "Test Create JWT",
        "email": "create-jwt@example.com",
        "password": "securepassword123",
    }
    group_response = await client.post("/access-groups/", json=group_data)
    assert group_response.status_code == status.HTTP_201_CREATED
    group = group_response.json()

    request_data = {"email": group["email"], "password": group_data["password"]}
    response = await client.post("/auth/", json=request_data)

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data.get("access_group") == group.get("id")
    assert JwtResponse(**response_data)


@pytest.mark.asyncio
async def test_create_jwt_with_invalid_email(client: AsyncClient) -> None:
    """Test creating a JWT token with invalid email.

    Args:
        client (AsyncClient): The async httpx Client fixture for making requests.
    """
    request_data = {"email": "invalid@example.com", "password": "securepassword123"}
    response = await client.post("/auth/", json=request_data)

    assert response.status_code == InvalidCredentialsException.STATUS_CODE


@pytest.mark.asyncio
async def test_create_jwt_with_invalid_password(client: AsyncClient) -> None:
    """Test creating a JWT token with invalid password.

    Args:
        client (AsyncClient): The async httpx Client fixture for making requests.
    """
    request_data = {"email": "create-jwt@example.com", "password": "securepassword124"}
    response = await client.post("/auth/", json=request_data)

    assert response.status_code == InvalidCredentialsException.STATUS_CODE


@pytest.mark.asyncio
async def test_use_jwt(client: AsyncClient) -> None:
    """Test using a JWT token.

    Args:
        client (AsyncClient): The async httpx Client fixture for making requests.
    """
    group_data = {
        "name": "Test Use JWT",
        "email": "use-jwt@example.com",
        "password": "securepassword123",
    }
    group_response = await client.post("/access-groups/", json=group_data)
    assert group_response.status_code == status.HTTP_201_CREATED

    jwt_request = {"email": group_data["email"], "password": group_data["password"]}
    jwt_response = await client.post("/auth/", json=jwt_request)
    assert jwt_response.status_code == status.HTTP_201_CREATED
    jwt = JwtResponse(**jwt_response.json())

    verify_data = {"access_group": str(jwt.access_group), "signature": jwt.signature}
    response = await client.put("/auth/", json=verify_data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_use_jwt_with_invalid_signature(client: AsyncClient) -> None:
    """Test using a JWT token with invalid signature.

    Args:
        client (AsyncClient): The async httpx Client fixture for making requests.
    """
    jwt_request = {"email": "use-jwt@example.com", "password": "securepassword123"}
    jwt_response = await client.post("/auth/", json=jwt_request)
    assert jwt_response.status_code == status.HTTP_201_CREATED
    jwt = JwtResponse(**jwt_response.json())

    verify_data = {
        "access_group": str(jwt.access_group),
        "signature": "invalidsignature",
    }
    response = await client.put("/auth/", json=verify_data)
    assert response.status_code == InvalidTokenException.STATUS_CODE
    assert response.json()["detail"] == InvalidTokenException.DETAIL


@pytest.mark.asyncio
async def test_use_jwt_with_expired_token(client: AsyncClient) -> None:
    """Test using a JWT token that has expired.

    Args:
       client (AsyncClient): The async httpx Client fixture for making requests.
    """
    jwt_request = {"email": "use-jwt@example.com", "password": "securepassword123"}
    jwt_response = await client.post("/auth/", json=jwt_request)
    assert jwt_response.status_code == status.HTTP_201_CREATED
    jwt = JwtResponse(**jwt_response.json())

    with freeze_time() as frozen_time:
        frozen_time.move_to(jwt.valid_until + timedelta(seconds=5))

        verify_data = {
            "access_group": str(jwt.access_group),
            "signature": str(jwt.signature),
        }

        response_fail = await client.put("/auth/", json=verify_data)
        assert response_fail.status_code == ExpiredTokenException.STATUS_CODE
        assert response_fail.json()["detail"] == ExpiredTokenException.DETAIL
