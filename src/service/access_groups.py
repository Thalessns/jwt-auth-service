"""Module for the access groups services."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from uuid import UUID

from src.database.database import Database
from src.database.tables import access_groups_table
from src.exceptions.access_groups import (
    AccessGroupNotFoundException,
    EmailAlreadyInUseException,
    InvalidCredentialsException,
)
from src.schema.access_groups import AccessGroupRequest, AccessGroupResponse
from src.service.utils import UtilsService


class AccessGroupsService:
    """Service class for access groups."""

    @classmethod
    async def create_access_group(
        cls, request: AccessGroupRequest
    ) -> AccessGroupResponse:
        """Create a new access group.

        Args:
            request (AccessGroupRequest): The new access group data.

        Returns:
            AccessGroupRequest: The created access group.

        Raises:
            EmailAlreadyInUseException: Raised when an email is already in use.
        """
        group_id = UtilsService.create_uuid()
        date_created = UtilsService.get_current_datetime()
        query = access_groups_table.insert().values(
            id=group_id,
            name=request.name,
            email=request.email,
            password=request.password,
            date_created=date_created,
        )
        try:
            await Database.execute(query)
        except IntegrityError:
            raise EmailAlreadyInUseException(email=request.email)
        return AccessGroupResponse(
            name=request.name, email=request.email, date_created=date_created
        )

    @classmethod
    async def get_all(cls) -> list[AccessGroupResponse]:
        """Get all access groups.

        Returns:
            list[AccessGroupResponse]: All the access groups.
        """
        query = select(
            access_groups_table.c.name,
            access_groups_table.c.email,
            access_groups_table.c.date_created,
        )
        rows = await Database.fetch_all(query)
        return [AccessGroupResponse(**row) for row in rows]

    @classmethod
    async def get_by_id(cls, id: str) -> AccessGroupResponse:
        """Get an access group by id.

        Args:
            id (str): The access group id.

        Returns:
            AccessGroupResponse: The group access.

        Raises:
            AccessGroupNotFoundException: Raised when the access group is not found.
        """
        query = select(
            access_groups_table.c.name,
            access_groups_table.c.email,
            access_groups_table.c.date_created,
        ).where(access_groups_table.c.id == id)
        row = await Database.fetch_one(query)
        if not row:
            raise AccessGroupNotFoundException(id=id)
        return AccessGroupResponse(**row)

    @classmethod
    async def authenticate_group(cls, email: str, password: str) -> UUID:
        """Authenticate access group.

        Args:
            email (str): The group email.
            password (str): The group password.

        Returns:
            UUID: The access group id.
        """
        query = (
            access_groups_table.select()
            .where(access_groups_table.c.email == email)
            .where(access_groups_table.c.password == password)
        )
        row = await Database.fetch_one(query)
        if not row:
            InvalidCredentialsException
        return row.get("id")
