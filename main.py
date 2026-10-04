"""Application entry point for the FastAPI project.

This module is the central wiring point for the API. It boots the FastAPI app,
creates the database tables during startup, and registers the authentication routes
from the router layer. In the broader project structure, this file sits at the top
of the stack: the router endpoints call the service layer, which then talks to the
repository layer, which performs database work through the SQLAlchemy session.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers.auth import authRouter
from app.util.init_db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run startup logic before the app begins serving requests.

    The application creates the database tables on startup so the User model is
    available before any route tries to read or write user data. This connects the
    app bootstrap to the database initialization helper in util/init_db.py.
    """
    create_tables()
    print("Created")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=authRouter, tags=["auth"], prefix="/auth")


@app.get("/health")
def health_check():
    """Simple readiness endpoint used to confirm the API is running.

    This is a lightweight operational check that does not interact with the database
    or user logic; it simply confirms the application instance is serving requests.
    """
    return {"status": "Running..."}