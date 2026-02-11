"""Endpoints for authentication."""

from fastapi import APIRouter, status

from src.schema.auth import JwtRequest, JwtResponse, VerifyJwtRequest
from src.service.access_groups import AccessGroupsService
from src.service.auth import AuthService

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/", status_code=status.HTTP_201_CREATED, response_model=JwtResponse)
async def create_jwt(request: JwtRequest):
    """Creates a new jwt token.

    Args:
        request (JwtRequest): The user payload.

    Returns:
        JwtResponse: The jwt token.
    """
    group_id = await AccessGroupsService.authenticate_group(
        request.email, request.password
    )
    return await AuthService.create_jwt(request, group_id)


@auth_router.put("/", status_code=status.HTTP_200_OK)
async def verify_jwt(request: VerifyJwtRequest):
    """Verify if is the jwt is valid.

    Args:
        request (VerifyJwtRequest): The request data.
    """
    return await AuthService.verify_token(request)
