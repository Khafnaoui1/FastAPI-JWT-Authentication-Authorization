"""Shared repository base used by all data-access classes.

This file defines the common dependency that every repository in the project will
receive: a SQLAlchemy `Session`. That session is created in the database layer and
then injected into repository classes such as `UserRepository`. By keeping the
session at the base class level, all repository-specific queries share the same
connection lifecycle and naming pattern.
"""

from sqlalchemy.orm import Session


class BaseRepository:
    """Provide a common database session to concrete repository classes."""

    def __init__(self, session: Session) -> None:
        """Store the active database session for use by repository methods."""
        self.session = session