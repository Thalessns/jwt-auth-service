"""Endpoints for authentication."""
from fastapi import APIRouter, status

from src.schema.auth import JwtRequest, JwtResponse
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
    # Validate user here TODO
    return await AuthService.create_jwt(request)


@auth_router.get("/", status_code=status.HTTP_200_OK)
async def verify_jwt(token: str):
    """Verify if is the jwt is valid."""
    return await AuthService.verify_token(token)
