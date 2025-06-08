from sqlalchemy import Column, Integer, String

from database.models.base import Base


class User(Base):
    """
    Represents a user in the database.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    city = Column(String)
