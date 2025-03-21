from contextlib import contextmanager

import pandas as pd
from sqlalchemy import create_engine, exc, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from typing import Generator, Type

# Constants for table names
USERS_TABLE = "users"
ORDERS_TABLE = "orders"

# Base class for models
Base: DeclarativeMeta = declarative_base()


class User(Base):
    """Represents a user in the database."""
    __tablename__ = USERS_TABLE

    identifier = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)

    # Relationship to the Orders table
    orders = relationship("Orders", back_populates="customer")


class Orders(Base):
    """Represents an order in the database."""
    __tablename__ = ORDERS_TABLE

    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey(
        f"{USERS_TABLE}.identifier"), index=True)
    product = Column(String, index=True)
    quantity = Column(Integer, index=True)
    total_price = Column(Integer, index=True)
    order_date = Column(String, index=True)

    # Relationship to the User table
    customer = relationship("User", back_populates="orders")


def initialize_database(engine) -> None:
    """
    Initialize the database by creating all tables.

    Args:
        engine: SQLAlchemy engine instance.
    """
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db_session(session_factory: sessionmaker) -> Generator[Session, None, None]:
    """
    Provide a transactional scope around a series of operations.

    Args:
        session_factory: SQLAlchemy sessionmaker instance.

    Yields:
        Session: A database session.
    """
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


def bulk_insert_users(db_session: Session, users_csv: pd.DataFrame) -> None:
    """
    Bulk insert users from a DataFrame.

    Args:
        db_session (Session): Database session.
        users_csv (pd.DataFrame): DataFrame containing user data.
    """
    try:
        records = users_csv.to_dict(orient='records')
        db_session.bulk_insert_mappings(User, records)
        db_session.commit()
    except exc.SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error bulk inserting users: {e}")


def bulk_insert_orders(db_session: Session, orders_csv: pd.DataFrame) -> None:
    """
    Bulk insert orders from a DataFrame.

    Args:
        db_session (Session): Database session.
        orders_csv (pd.DataFrame): DataFrame containing order data.
    """
    try:
        records = orders_csv.to_dict(orient='records')
        db_session.bulk_insert_mappings(Orders, records)
        db_session.commit()
    except exc.SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error bulk inserting orders: {e}")


def drop_table(db_session: Session, table: Type[Base]) -> None:
    """
    Drop a specific table.

    Args:
        db_session (Session): Database session.
        table (Type[Base]): SQLAlchemy table class to drop.
    """
    try:
        table.__table__.drop(db_session.bind)
    except exc.SQLAlchemyError as e:
        print(f"Error dropping table: {e}")
