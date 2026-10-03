import jwt
from decouple import config  # type: ignore[import-not-found]
import time

JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")


class authHandler(object):

    @staticmethod
    def sign_jwt(user_id: int) -> str:
        payload={
            "user_id" : user_id,
            "expires": time.time() + 900
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token

    @staticmethod
    def decode_jwt(token: str)-> dict | None:
        try:
            decoded_token = jwt.decode(token, JWT_SECRET,algorithm=JWT_ALGORITHM)
            return decoded_token if decoded_token["expires"] >= time.time() else None
        except Exception as e:
           print(f"Unable to decode the token: {e}")
           return None
   