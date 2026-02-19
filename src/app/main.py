"""Main module."""

from fastapi import FastAPI, status
from contextlib import asynccontextmanager

from src.database.database import Database
from src.router.access_groups import access_groups_router
from src.router.auth import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context for the application."""
    await Database.init_models()
    yield


app = FastAPI(title="JWT Auth Service", version="0.0.1", lifespan=lifespan)
prefix = "/api"

@app.get(prefix+"/", status_code=status.HTTP_200_OK)
async def root() -> dict[str, str]:
    """Service root endpoint.

    Returns:
        dict[str, str]: Message to the user.
    """
    return {"message": "The JWT Auth Service is running!"}


app.include_router(access_groups_router, prefix=prefix)
app.include_router(auth_router, prefix=prefix)
