"""Database initialization helper used during app startup.

This module acts as the bridge between the SQLAlchemy metadata and the database
engine. `main.py` calls `create_tables()` inside the app lifespan hook, which then
reads all registered models, including the `User` model from `db/models/user.py`,
and creates the corresponding tables in the configured database.
"""

from app.core.database import Base, engine
from app.db.models import user


def create_tables():
    """Create all SQLAlchemy tables defined in the project metadata."""
    Base.metadata.create_all(bind=engine)