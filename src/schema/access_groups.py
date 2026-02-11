"""Module for the access groups schemas."""

from datetime import datetime
from pydantic import BaseModel, EmailStr


class AccessGroupRequest(BaseModel):
    """Schema to create a new access group."""

    name: str
    email: EmailStr
    password: str


class AccessGroupResponse(BaseModel):
    """Schema to return a access group."""

    name: str
    email: EmailStr
    date_created: datetime
