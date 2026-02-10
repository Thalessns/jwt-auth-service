"""Schemas for auth."""
from datetime import datetime
from pydantic import BaseModel


class JwtRequest(BaseModel):
    """Schema for a new jwt request."""

    username: str
    password: str


class JwtResponse(BaseModel):
    """Schema for a created jwt."""

    access_token: str
    valid_until: datetime
