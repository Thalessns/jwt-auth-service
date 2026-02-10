"""Main module."""
from fastapi import FastAPI, status

from src.router.auth import auth_router


app = FastAPI(
    title="JWT Auth Service",
    version="0.0.1"
    )


@app.get("/", status_code=status.HTTP_200_OK)
async def root() -> str:
    """Service root endpoint.

    Returns:
        str: Message to the user.
    """
    return "The JWT Auth Service is running!"


prefix = "/api"
app.include_router(auth_router, prefix=prefix)
