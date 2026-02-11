"""Module for database operations."""

from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine

from src.database.settings import database_settings

Base = declarative_base(metadata=MetaData())


class Database:
    """The database class, used to perform operations."""

    engine = create_async_engine(database_settings.conn_url)

    @classmethod
    async def fetch_one(cls, query) -> dict | None:
        """Fetch one row from the database.

        Args:
            query (): The query to be executed.

        Returns:
            dict | None: Dict if is any row, None otherwise.
        """
        async with cls.engine.connect() as conn:
            cursor = await conn.execute(query)
            row = cursor.fetchone()
            return (row._mapping) if row else None

    @classmethod
    async def fetch_all(cls, query) -> list[dict]:
        """Fetch many rows from the database.

        Args:
            query (): The query to be executed.

        Returns:
            list[dict]: Rows fetched.
        """
        async with cls.engine.connect() as conn:
            cursor = await conn.execute(query)
            rows = cursor.fetchall()
            return [(row._mapping) for row in rows]

    @classmethod
    async def execute(cls, query) -> None:
        """Execute a query.

        Args:
            query (): The query to be executed.
        """
        async with cls.engine.begin() as conn:
            await conn.execute(query)

    @classmethod
    async def execute_many(cls, queries: list) -> None:
        """Execute many queries in one transaction.

        Args:
            queries (): The queries to be executed.
        """
        async with cls.engine.begin() as conn:
            for query in queries:
                await conn.execute(query)

    @classmethod
    async def init_models(cls) -> None:
        """Initialize the database tables."""
        async with cls.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
