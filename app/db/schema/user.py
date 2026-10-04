"""Pydantic schemas used to validate request and response payloads.

These models define the contract between the API layer and the rest of the
application. The router accepts `UserInCreate` and `UserInLogin` request bodies,
`UserService` consumes them to enforce business rules, and the repository works
with the ORM model instead of raw dictionary data. This separation makes the API
layer independent from the database model while keeping validation centralized.
"""

from typing import Union

from pydantic import BaseModel, EmailStr


class UserInCreate(BaseModel):
    """Payload for creating a new user account."""

    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserOutput(BaseModel):
    """Response schema returned after user creation or lookup."""

    id: int
    first_name: str
    last_name: str
    email: EmailStr


class UserInUpdate(BaseModel):
    """Optional fields for updating an existing user record."""

    id: int
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email: Union[EmailStr, None] = None
    password: Union[str, None] = None


class UserInLogin(BaseModel):
    """Login payload containing the email and password for authentication."""

    email: EmailStr
    password: str


class UserWithToken(BaseModel):
    """Response payload returned to a client after successful login."""

    token: str