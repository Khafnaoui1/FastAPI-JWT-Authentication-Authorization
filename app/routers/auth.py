"""Authentication routes exposed by the FastAPI application.

This file defines the public HTTP endpoints for account access. It sits at the
entry point of the request flow: clients call `/auth/login` or `/auth/signup`, the
request body is validated using the Pydantic schemas in `db/schema/user.py`, and the
business logic should eventually be delegated to the service layer. In this project,
`main.py` includes this router under the `/auth` prefix, which is how these endpoints
become part of the overall API.
"""

from fastapi import APIRouter

from app.db.schema.user import UserInCreate, UserInLogin

authRouter = APIRouter()


@authRouter.post("/login")
def login(loginDetails: UserInLogin):
    """Handle a user login request.

    This endpoint is the route boundary for authentication. A request body is
    validated by `UserInLogin`, and the next step in a complete implementation is to
    forward the payload into `UserService.login()` for credential verification and JWT
    creation.
    """
    return {"data": loginDetails}


@authRouter.post("/signup")
def signUp(signUpDetails: UserInCreate):
    """Handle a user registration request.

    The request body is validated as a `UserInCreate` object before entering the
    endpoint. In a fully connected implementation, this route would call
    `UserService.signup()` to validate uniqueness, hash the password, and persist the
    user through the repository layer.
    """
    return {"data": signUpDetails}