import os
import pandas as pd

from sqlalchemy import create_engine, exc, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from dotenv import load_dotenv

from read import get_orders_directory, get_users_directory, get_csvs, merge_csvs

load_dotenv()

DATABASE_URL_TEMPLATE = "postgresql+psycopg2://{username}:{password}@{db_host}/{database_name}"

DATABASE_URL = DATABASE_URL_TEMPLATE.format(
    username=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    db_host=os.getenv("DB_HOST"),
    database_name=os.getenv("DB_NAME"),
)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Base class for models
Base = declarative_base()

# Session maker to create database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Constants for table names
USERS_TABLE = "users"
ORDERS_TABLE = "orders"


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


# Create tables in the database
def initialize_database():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine)


# Utility function for session management
def get_db_session():
    """Provide a transactional scope around a series of operations."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRUD Operations
def create_user(db_session, identifier: int, first_name: str, last_name: str):
    """Add a single user to the database."""
    try:
        db_user = User(identifier=identifier,
                       first_name=first_name, last_name=last_name)
        db_session.add(db_user)
        db_session.commit()
        db_session.refresh(db_user)
        return db_user
    except exc.SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error creating user: {e}")
        return None


def create_order(db_session, customer_id: int, product: str, quantity: int, total_price: int, order_date: str):
    """Add a single order to the database."""
    try:
        db_order = Orders(
            customer_id=customer_id,
            product=product,
            quantity=quantity,
            total_price=total_price,
            order_date=order_date
        )
        db_session.add(db_order)
        db_session.commit()
        db_session.refresh(db_order)
        return db_order
    except exc.SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error creating order: {e}")
        return None


def bulk_insert_users(db_session, users_csv: pd.DataFrame):
    """Bulk insert users from a DataFrame."""
    try:
        records = users_csv.to_dict(orient='records')
        db_session.bulk_insert_mappings(User, records)
        db_session.commit()
    except exc.SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error bulk inserting users: {e}")


def bulk_insert_orders(db_session, orders_csv: pd.DataFrame):
    """Bulk insert orders from a DataFrame."""
    try:
        records = orders_csv.to_dict(orient='records')
        db_session.bulk_insert_mappings(Orders, records)
        db_session.commit()
    except exc.SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error bulk inserting orders: {e}")


def get_all_users(db_session):
    """Retrieve all users from the database."""
    return db_session.query(User).all()


def get_all_orders(db_session):
    """Retrieve all orders from the database."""
    return db_session.query(Orders).all()


def drop_table(db_session, table):
    """Drop a specific table."""
    try:
        table.__table__.drop(db_session.bind)
    except exc.SQLAlchemyError as e:
        print(f"Error dropping table: {e}")


# Main function to run the script
def main():
    initialize_database()

    with SessionLocal() as db:
        # Load and merge user data
        users_directory = get_users_directory()
        users_csvs = get_csvs(users_directory)
        users_df = merge_csvs(users_csvs)

        # Load and merge order data
        orders_directory = get_orders_directory()
        orders_csvs = get_csvs(orders_directory)
        orders_df = merge_csvs(orders_csvs)

        # Insert data into the database
        bulk_insert_users(db, users_df)
        bulk_insert_orders(db, orders_df)


if __name__ == "__main__":
    main()
