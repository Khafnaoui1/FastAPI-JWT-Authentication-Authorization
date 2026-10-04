"""Central SQLAlchemy database configuration for the project.

This file creates the database engine, configures a session factory, and defines
`Base`, which all ORM models inherit from. It is the shared foundation that ties
all higher layers together: models in the db/models package create tables based on
this `Base`, repositories use database sessions to query/write records, and routes
can receive sessions through `get_db()` when they need database access.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if SQLALCHEMY_DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL environment variable is not set")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    """Create and yield a database session for request-scoped access.

    This generator pattern is the standard FastAPI approach for dependency injection.
    Any route or service layer that needs database access can depend on `get_db()` to
    obtain a session tied to the configured engine. The session is closed after the
    request completes, which keeps database access consistent and avoids leaking
    connections.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()