"""
Base class for all SQLAlchemy models.

This class serves as the foundation for all database models in the application.
It is used to define the schema and relationships for the database tables.
"""
from typing import Type

from sqlalchemy.orm import declarative_base, DeclarativeMeta

Base = declarative_base()
