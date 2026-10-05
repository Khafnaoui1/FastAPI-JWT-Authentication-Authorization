from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security.authHandler import AuthHandler
from app.core.security.hashHelper import HashHelper
from app.db.repository.userRepo import UserRepository
from app.db.schema.user import UserInCreate, UserInLogin, UserOutput, UserWithToken


class UserService:
    def __init__(self, session: Session):
        self.__userRepository = UserRepository(session=session)

    def signup(self, user_details: UserInCreate) -> UserOutput | None:
        if self.__userRepository.user_exist_by_email(email=user_details.email):
            raise HTTPException(status_code=400, detail="Please Login")

        hashed_password = HashHelper.get_password_hash(plain_password=user_details.password)
        user_details.password = hashed_password
        return self.__userRepository.create_user(user_data=user_details)

    def login(self, login_details: UserInLogin) -> UserWithToken | None:
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
            token = AuthHandler.sign_jwt(user_id=user.id)  # type: ignore

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

    def get_user_by_id(self, user_id: int):
        user = self.__userRepository.get_user_by_id(user_id=user_id)
        if user:
            return user
        raise HTTPException(status_code=400, detail="user is not available")