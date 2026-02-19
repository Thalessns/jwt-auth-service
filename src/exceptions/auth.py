"""Exceptions for auth."""

from fastapi import status

from src.app.exceptions import CustomBaseException


class ExpiredTokenException(CustomBaseException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "The token provided is expired."


class InvalidTokenException(CustomBaseException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "The token provided is invalid."
