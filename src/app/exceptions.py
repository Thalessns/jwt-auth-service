"""Exceptions for the app module."""
from fastapi import HTTPException, status


class CustomBaseException(HTTPException):
    """Custom exception for the app."""

    STATUS_CODE: int
    DETAIL: str

    def __init__(self, kwargs: dict[str, any]) -> None:
        """Constructor for the class."""

        super.__init__(
            status_code=self.STATUS_CODE,
            detail=self.DETAIL.format(**kwargs)
        )
