"""Database access layer for user-related persistence logic.

This repository sits directly above the ORM model and below the service layer. The
service class calls repository methods to check whether a user exists, create a new
user, and load user records by email or ID. This keeps database queries out of the
route and service code while still allowing clean business-logic operations.
"""

from app.db.models.user import User
from app.db.schema.user import UserInCreate

from .base import BaseRepository


class UserRepository(BaseRepository):
    """Handle persistence for user records using the shared SQLAlchemy session."""

    def create_user(self, user_data: UserInCreate):
        """Insert a validated user payload into the database.

        `UserService.signup()` builds a `UserInCreate` object, hashes the password,
and then passes it here. The repository converts the schema to a `User` ORM model,
        saves it, commits, and refreshes it so the newly created database row is ready
        for use by the calling service.
        """
        newUser = User(user_data.model_dump(exclude_none=True))

        self.session.add(instance=newUser)
        self.session.commit()
        self.session.refresh(instance=newUser)

        return newUser

    def user_exist_by_email(self, email: str) -> bool:
        """Return whether a user with the supplied email already exists."""
        user = self.session.query(User).filter_by(email=email).first()
        return bool(user)

    def get_user_by_email(self, email: str) -> User:
        """Fetch a user record by email for authentication and lookup use cases."""
        user = self.session.query(User).filter_by(email=email).first()
        return user

    def get_user_by_id(self, user_id: int) -> User | None:
        """Fetch a user by primary key; useful for ID-based retrieval operations."""
        user = self.session.query(User).filter_by(id=user_id).first()
        return user