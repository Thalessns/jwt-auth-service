"""Module for password handling utilities."""

from pwdlib import PasswordHash


class PasswordHandler:
    """Utility class for handling password hashing and verification."""

    password_hasher = PasswordHash.recommended()

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Hash a password.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """
        return cls.password_hasher.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        """Verify a password against a hashed password.

        Args:
            password (str): The password to verify.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        return cls.password_hasher.verify(password, hashed_password)
