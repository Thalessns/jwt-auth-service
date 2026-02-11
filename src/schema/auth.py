"""Schemas for auth."""

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr


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
