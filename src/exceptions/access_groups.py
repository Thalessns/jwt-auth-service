"""Exceptions for access groups."""

from fastapi import status

from src.app.exceptions import CustomBaseException


class AccessGroupNotFoundException(CustomBaseException):
    """Exception raised when an access group is not found."""

    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Access group with the id '{id}' was not found."


class EmailAlreadyInUseException(CustomBaseException):
    """Exception raised when an email is already in use."""

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "The email '{email}' is already in use, try another one."


class InvalidCredentialsException(CustomBaseException):
    """Exception raised when the group credentials are invalid."""

    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "The group credentials are invalid, check it and try again."


class AccessGroupIdUUIDException(CustomBaseException):
    """Exception raised when the access group id is invalid."""

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "The access group id must be a valid UUID, check it and try again."
