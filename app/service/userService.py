"""Business logic for user registration and authentication.

This service sits between the HTTP route layer and the repository layer. It applies
application rules such as duplicate email checks, password hashing, and JWT issue
logic. In the overall architecture, the router receives HTTP requests, validates
incoming data with Pydantic schemas, and then calls this service; the service then
delegates persistent operations to the repository and security helpers.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security.authHandler import AuthHandler
from app.core.security.hashHelper import HashHelper
from app.db.repository.userRepo import UserRepository
from app.db.schema.user import UserInCreate, UserInLogin, UserOutput, UserWithToken


class UserService:
    """Encapsulate the rules for signup and login operations."""

    def __init__(self, session: Session):
        """Create a repository tied to the caller's database session."""
        self.__userRepository = UserRepository(session=session)

    def signup(self, user_details: UserInCreate) -> UserOutput | None:
        """Register a new user after checking for duplicates and hashing the password.

        The method coordinates several lower-level pieces:
        - repository checks for an existing email
        - password is hashed using `HashHelper`
        - the sanitized user record is inserted through the repository
        - the created ORM object is returned to the caller
        """
        if self.__userRepository.user_exist_by_email(email=user_details.email):
            raise HTTPException(status_code=400, detail="Please Login")

        hashed_password = HashHelper.get_password_hash(plain_password=user_details.password)
        user_details.password = hashed_password
        return self.__userRepository.create_user(user_data=user_details)

    def login(self, login_details: UserInLogin) -> UserWithToken | None:
        """Authenticate a user and return a JWT token when credentials are valid.

        This method links the database, hashing, and token-generation layers together:
        it loads the user by email, compares the submitted password with the stored
        bcrypt hash, and if correct it calls `AuthHandler.sign_jwt()` to issue a token.
        """
        if not self.__userRepository.user_exist_by_email(email=login_details.email):
            raise HTTPException(
                status_code=400,
                detail="Please create an account",
            )

        user = self.__userRepository.get_user_by_email(email=login_details.email)

        if HashHelper.verify_password(
            plain_password=login_details.password,
            hashed_password=str(user.password),
        ):
            token = AuthHandler.sign_jwt(user_id=user.id) # type: ignore

            if token:
                return UserWithToken(token=token)

            raise HTTPException(
                status_code=500,
                detail="Unable to process request",
            )

        raise HTTPException(
            status_code=400,
            detail="Please check your credentials",
        )