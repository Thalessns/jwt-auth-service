"""Auth service module."""

import jwt
from uuid import UUID

from src.app.settings import jwt_settings
from src.database.database import Database
from src.database.tables import jwt_tokens_table
from src.exceptions.auth import ExpiredTokenException, InvalidTokenException
from src.schema.auth import Jwt, JwtRequest, JwtResponse, VerifyJwtRequest
from src.service.utils import UtilsService


class AuthService:
    """Auth service class."""

    @classmethod
    async def create_jwt(cls, request: JwtRequest, group_id: UUID) -> JwtResponse:
        """Create a jwt token.

        Args:
            request (JwtRequest): The user payload.
            group_name (UUID): The access group id.

        Returns:
            JwtResponse: The jwt token.
        """
        payload = request.model_dump()
        date_created = UtilsService.get_current_datetime()
        payload["timestamp"] = (
            UtilsService.get_int_timestamp(date_created) + jwt_settings.JWT_VALID_TIME
        )
        encoded = jwt.encode(
            payload=payload,
            key=jwt_settings.JWT_KEY,
            algorithm=jwt_settings.JWT_ALGORITHM,
        )
        token_id = UtilsService.create_uuid()
        valid_until = UtilsService.get_timestamp_from_int(payload["timestamp"])
        query = jwt_tokens_table.insert().values(
            id=token_id,
            access_group=group_id,
            signature=encoded,
            valid_until=valid_until,
            date_created=date_created,
        )
        await Database.execute(query)
        return JwtResponse(
            id=token_id,
            access_group=group_id,
            signature=encoded,
            valid_until=valid_until,
            date_created=date_created,
        )

    @classmethod
    async def decode_jwt(cls, token: str) -> dict:
        """Decode a jwt token.

        Args:
            token: The jwt token to be decoded.

        Returns:
            dict: The decoded token.
        """
        return jwt.decode(
            jwt=token, key=jwt_settings.JWT_KEY, algorithms=[jwt_settings.JWT_ALGORITHM]
        )

    @classmethod
    async def use_token(cls, request: VerifyJwtRequest) -> None:
        """Use the JWT.

        Args:
            request (VerifyJwtRequest): Request data.

        Raises:
            ExpiredTokenException: If the token expired.
            InvalidTokenException: If the token is invalid.
        """
        query_verify = (
            jwt_tokens_table.select()
            .where(jwt_tokens_table.c.signature == request.signature)
            .where(jwt_tokens_table.c.access_group == UUID(request.access_group))
        )
        row_verify = await Database.fetch_one(query_verify)

        if not row_verify:
            raise InvalidTokenException()

        token = Jwt(**row_verify)

        current_timestamp = UtilsService.get_int_timestamp()
        valid_until = UtilsService.get_int_timestamp(token.valid_until)

        if current_timestamp > valid_until:
            raise ExpiredTokenException()

        if (valid_until - current_timestamp) < 60:
            valid_until = valid_until + 60

        await cls.refresh_token(token, valid_until)

        return JwtResponse(
            id=token.id,
            access_group=token.access_group,
            signature=token.signature,
            valid_until=UtilsService.get_timestamp_from_int(valid_until),
            date_created=token.date_created,
        )

    @classmethod
    async def refresh_token(cls, token: Jwt, valid_until: int) -> None:
        """Refresh the Jwt.

        Args:
            token (Jwt): The jwt to be updated.
            valid_until (int): When the token expires.
        """
        query_update = (
            jwt_tokens_table.update()
            .where(jwt_tokens_table.c.id == token.id)
            .values(
                valid_until=UtilsService.get_timestamp_from_int(valid_until),
                last_refresh=UtilsService.get_current_datetime(),
                times_refreshed=token.times_refreshed + 1,
            )
        )
        await Database.execute(query_update)
