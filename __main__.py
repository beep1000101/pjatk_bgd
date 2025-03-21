import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from python.postgres import (
    initialize_database,
    get_db_session,
    bulk_insert_users,
    bulk_insert_orders,
)
from python.read import get_orders_directory, get_users_directory, get_csvs, merge_csvs


def main():
    """
    Main function to initialize the database and insert data.
    """
    # Load environment variables
    load_dotenv()

    # Construct the database URL
    DATABASE_URL_TEMPLATE = "postgresql+psycopg2://{username}:{password}@{db_host}/{database_name}"
    DATABASE_URL = DATABASE_URL_TEMPLATE.format(
        username=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        db_host=os.getenv("DB_HOST"),
        database_name=os.getenv("DB_NAME"),
    )

    # Create the SQLAlchemy engine and session factory
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Initialize the database
    initialize_database(engine)

    # Use a database session to insert data
    with get_db_session(SessionLocal) as db:
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
