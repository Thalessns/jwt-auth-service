"""Setup file for the JWT Authentication Service."""
from setuptools import setup, find_packages

setup(
    name="jwt-auth-service",
    version="0.0.1",
    description="A JWT authentication service built with FastAPI.",
    python_requires=">=3.10",
    packages=find_packages(where="src")
)
