"""Schemas for auth."""

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator

from src.exceptions.access_groups import AccessGroupIdUUIDException


class Jwt(BaseModel):
    """Schema for the Jwt Token."""

    id: UUID
    access_group: UUID
    signature: str
    valid_until: datetime
    date_created: datetime
    last_refresh: datetime | None
    times_refreshed: int


class JwtRequest(BaseModel):
    """Schema for a new jwt request."""

    email: EmailStr
    password: str


class JwtResponse(BaseModel):
    """Schema for a created jwt."""

    id: UUID
    access_group: UUID
    signature: str
    valid_until: datetime
    date_created: datetime


class VerifyJwtRequest(BaseModel):
    """Schema for jwt verification."""

    access_group: str
    signature: str

    @field_validator("access_group")
    def validate_uuid(cls, value: str) -> UUID:
        """Validate that the access group is a valid UUID.

        Args:
            value (str): The access group id.

        Returns:
            UUID: The access group id as a UUID.

        Raises:
            AccessGroupIdUUIDException: If the access group id is not a valid UUID.
        """
        try:
            UUID(value)
        except ValueError:
            raise AccessGroupIdUUIDException()
        return UUID(value)
