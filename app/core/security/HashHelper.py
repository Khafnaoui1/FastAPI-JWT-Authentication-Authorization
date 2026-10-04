"""Password hashing and verification helpers.

This module acts as the security layer for user credentials. It is used by the
service layer during sign-up and login flows: when a new account is created, the
plain-text password is hashed before saving to the database; when a user logs in,
the submitted password is compared against the stored hash. This keeps raw password
values out of the database while still allowing safe verification.
"""

from bcrypt import checkpw, gensalt, hashpw


class HashHelper(object):
    """Provide bcrypt-based password hashing support for the authentication flow."""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        """Check whether the submitted password matches the stored hash.

        This is called by the `UserService.login()` flow after loading the user from the
        database. If the result is true, the service can issue a JWT token for the user.
        """
        if checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8")):
            return True
        return False

    @staticmethod
    def get_password_hash(plain_password: str):
        """Hash a plain-text password before it is persisted to the database."""
        return hashpw(
            plain_password.encode("utf-8"),
            gensalt(),
        ).decode("utf-8")
    