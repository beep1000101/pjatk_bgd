from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

import pandas as pd

from read import get_orders_directory, get_users_directory, get_csvs, merge_csvs

# Replace with your actual username, password, and database name
DATABASE_URL_TEMPLATE = "postgresql+psycopg2://{username}:{password}@localhost/{database_name}"
DATABASE_URL = DATABASE_URL_TEMPLATE.format(
    username="postgres",
    password="postgrespassword",
    database_name="bgddatabase"
)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Base class for models
Base = declarative_base()

# Session maker to create database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(Base):
    """
    Represents a user in the database.

    Attributes:
        identifier (int): The unique identifier for the user. Primary key.
        first_name (str): The first name of the user. Indexed for faster queries.
        last_name (str): The last name of the user. Must be unique and indexed.
    """
    __tablename__ = 'users'

    identifier = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)

    # Relationship to the Orders table
    orders = relationship("Orders", back_populates="customer")


class Orders(Base):
    """
    Represents an order in the database.

    Attributes:
        order_id (int): The unique identifier for the order. Primary key.
        customer_id (int): The identifier of the customer who placed the order. Foreign key referencing the User table.
        product (str): The name of the product ordered. Indexed.
        quantity (int): The quantity of the product ordered. Indexed.
        total_price (int): The total price of the order. Indexed.
        order_date (str): The date the order was placed. Indexed.
    """
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('users.identifier'), index=True)
    product = Column(String, index=True)
    quantity = Column(Integer, index=True)
    total_price = Column(Integer, index=True)
    order_date = Column(String, index=True)

    # Relationship to the User table
    customer = relationship("User", back_populates="orders")


# Create tables in the database
Base.metadata.create_all(bind=engine)


# Function to interact with the database (add user)
def create_user(
        db_session,
        identifier: int,
        first_name: str,
        last_name: str,
):
    db_user = User(
        identifier=identifier,
        first_name=first_name,
        last_name=last_name)
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user


def create_order(
        db_session,
        customer_id: int,
        product: str,
        quantity: int,
        total_price: int,
        order_date: str,
):
    db_order = Orders(
        customer_id=customer_id,
        product=product,
        quantity=quantity,
        total_price=total_price,
        order_date=order_date)
    db_session.add(db_order)
    db_session.commit()
    db_session.refresh(db_order)
    return db_order


def create_users_bulk(db_session, users_csv: pd.DataFrame):
    records = users_csv.to_dict(orient='records')

    db_session.bulk_insert_mappings(User, records)
    db_session.commit()


def create_orders_bulk(db_session, orders_csv: pd.DataFrame):
    records = orders_csv.to_dict(orient='records')

    db_session.bulk_insert_mappings(Orders, records)
    db_session.commit()


def get_users(db_session):
    return db_session.query(User).all()


def get_orders(db_session):
    return db_session.query(Orders).all()


def drop_users_table(db_session):
    User.__table__.drop(db_session.bind)


def drop_orders_table(db_session):
    Orders.__table__.drop(db_session.bind)


# Main function to run code
if __name__ == "__main__":
    with SessionLocal() as db:
        users_directory = get_users_directory()
        users_csvs = get_csvs(users_directory)
        users_df = merge_csvs(users_csvs)

        # get orders data
        orders_directory = get_orders_directory()
        orders_csvs = get_csvs(orders_directory)
        orders_df = merge_csvs(orders_csvs)

        # put data into database
        create_users_bulk(db, users_df)
        create_orders_bulk(db, orders_df)
