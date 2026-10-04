"""JWT utilities for authentication.

This module handles token creation and validation for authenticated users. It is a
security helper used by the user service after successful login. When a user signs
in with correct credentials, `UserService.login()` calls `sign_jwt()`, producing a
token that can be returned to the client. That token can then be validated later by
protected routes or by any future authorization logic using `decode_jwt()`.
"""

import time

import jwt
from decouple import config  # type: ignore[import-not-found]

JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")


class AuthHandler(object):
    """Create and decode signed JWTs used for user authentication."""

    @staticmethod
    def sign_jwt(user_id: int) -> str:
        """Generate a JWT for a user ID with a 15-minute expiration window.

        The service layer calls this after checking the user's password; the resulting
        token is returned to the client as proof of authentication. The payload links
        the token to the user's database identity via `user_id` and includes an expiry
        timestamp to enforce short-lived sessions.
        """
        payload = {
            "user_id": user_id,
            "expires": time.time() + 900,
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token

    @staticmethod
    def decode_jwt(token: str) -> dict | None:
        """Validate a JWT and ensure it has not expired.

        This helper is the security boundary for protected endpoints: it verifies the
        token signature and checks whether the expiry timestamp is still valid. If the
        token is missing, malformed, or expired, it returns `None`, which downstream
        code can interpret as an unauthenticated or invalid request.
        """
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
            return decoded_token if decoded_token["expires"] >= time.time() else None
        except Exception as e:
            print(f"Unable to decode the token: {e}")
            return None