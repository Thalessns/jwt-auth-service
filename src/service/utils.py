"""Util module for services."""

import pytz
from uuid import UUID, uuid4
from datetime import datetime


class UtilsService:
    """Utils class for the other services."""

    __brazil_timezone = pytz.timezone("America/Sao_Paulo")

    @classmethod
    def create_uuid(cls) -> UUID:
        """Create an UUID.

        Returns:
            UUID: The created UUID.
        """
        return uuid4()

    @classmethod
    def get_current_datetime(cls) -> datetime:
        """Get the current datetime from Brazil - São Paulo

        Returns:
            datetime: The current datetime.
        """
        return datetime.now(cls.__brazil_timezone).replace(tzinfo=None)

    @classmethod
    def get_int_timestamp(cls, current: datetime = None) -> int:
        """Get the current timestamp.

        Args:
            current (datetime): The current datetime, default is None.

        Returns:
            int: The timestamp.
        """
        if current:
            return int(current.timestamp())
        return int(cls.get_current_datetime().timestamp())

    @classmethod
    def get_timestamp_from_int(cls, timestamp: int) -> datetime:
        """Get a timestamp from int.

        Args:
            timestamp (int): The timestamp.

        Returns:
            datetime: The converted datetime.
        """
        return datetime.fromtimestamp(timestamp, cls.__brazil_timezone).replace(
            tzinfo=None
        )
