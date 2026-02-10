"""Auth service module."""
import jwt
import pytz
from datetime import datetime

from src.app.settings import jwt_settings
from src.exceptions.auth import (
    ExpiredTokenException,
    InvalidTokenException
)
from src.schema.auth import JwtRequest, JwtResponse


class AuthService:
    """Auth service class."""

    brazil_timezone = pytz.timezone("America/Sao_Paulo")
    tokens: list[str] = []

    @classmethod
    async def create_jwt(cls, request: JwtRequest) -> JwtResponse:
        """Create a jwt token.
        
        Args:
            request (JwtRequest): The user payload.

        Returns:
            JwtResponse: The jwt token.
        """
        payload = request.model_dump()
        payload["timestamp"] = await cls.__get_timestamp() + jwt_settings.JWT_VALID_TIME
        encoded = jwt.encode(
            payload=payload,
            key=jwt_settings.JWT_KEY,
            algorithm=jwt_settings.JWT_ALGORITHM
        )
        cls.tokens.append(encoded)
        return JwtResponse(
            access_token=encoded,
            valid_until=datetime.fromtimestamp(payload["timestamp"], cls.brazil_timezone)
        )

    @classmethod
    async def decode_jwt(cls, token: str) -> dict:

        return jwt.decode(
            jwt=token,
            key=jwt_settings.JWT_KEY,
            algorithms=[jwt_settings.JWT_ALGORITHM]
        )

    @classmethod
    async def verify_token(cls, user_token: str) -> None:
        """Verify if the token is valid.
        
        Args:
            user_token (str): The user token.

        Raises:
            ExpiredTokenException: If the token expired.
            InvalidTokenException: If the token is invalid.
        """
        for token in cls.tokens:
            if user_token == token:
                stored_token = await cls.decode_jwt(token)
                timestamp = await cls.__get_timestamp() 
                if timestamp <= stored_token["timestamp"]:
                    return
                raise ExpiredTokenException()
        raise InvalidTokenException()

    @classmethod
    async def __get_timestamp(cls) -> int:
        """Get the current timestamp.
        
        Returns:
            int: The timestamp.
        """
        return int(datetime.now(cls.brazil_timezone).timestamp())
