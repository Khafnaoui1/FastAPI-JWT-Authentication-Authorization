"""ORM model for the application user table.

This is the SQLAlchemy entity that maps to the `Users` table in the database. The
model is defined with the shared `Base` from the core database configuration, so it
becomes part of the metadata that `create_tables()` creates on startup. The
repository layer performs CRUD operations against this model, while the schema layer
defines the input/output data shapes that the API routes accept and return.
"""

from sqlalchemy import Column, Integer, String

from app.core.database import Base


class User(Base):
    """Represents an application user record stored in the database."""

    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(100))
    email = Column(String(70), unique=True)
    password = Column(String(250))