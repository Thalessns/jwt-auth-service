"""Module for the access groups schemas."""

from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator

from src.schema.passw import PasswordHandler


class AccessGroupRequest(BaseModel):
    """Schema to create a new access group."""

    name: str
    email: EmailStr
    password: str

    @field_validator("password", mode="before")
    def hash_password(cls, value: str) -> str:
        """Hash the password before validation.

        Args:
            value (str): The password to hash.

        Returns:
            str: The hashed password.
        """
        return PasswordHandler.hash_password(value)


class AccessGroupResponse(BaseModel):
    """Schema to return a access group."""

    name: str
    email: EmailStr
    date_created: datetime
