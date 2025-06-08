from pathlib import Path
from typing import Final

import pandas as pd
import numpy as np

from database.models.base import Base
from database.models.users import User
from database.models.orders import Order

DATA_PATH: Final[Path] = Path(__file__).parents[1] / 'data'


def create_tables(bind):
    """
    Create all tables defined on Base.metadata.

    Parameters
    ----------
    bind : Engine or Connection
        The database bind to use.
    """
    Base.metadata.create_all(bind)


def seed_data(session):
    """
    Seed the database with initial data.
    """
    # Example users
    users = [
        User(name="Alice", email="alice@example.com", city="Wonderland"),
        User(name="Bob", email="bob@example.com", city="Builderland"),
        User(name="Charlie", email="charlie@example.com",
             city="Chocolate Factory"),
    ]
    session.add_all(users)
    session.commit()

    # Example orders (assuming customer_id, product, quantity, total_price, order_date)
    orders = [
        Order(customer_id=users[0].id, product="Book",
              quantity=2, total_price=40.0),
        Order(customer_id=users[1].id, product="Hammer",
              quantity=1, total_price=15.5),
        Order(customer_id=users[2].id, product="Chocolate",
              quantity=5, total_price=25.0),
    ]
    session.add_all(orders)
    session.commit()


def find_csvs_in_directory(directory: Path):
    """
    Find all CSV files in the specified directory.

    Parameters
    ----------
    directory : Path
        The directory to search for CSV files.

    Returns
    -------
    list of Path
        A list of paths to CSV files found in the directory.
    """
    return list(directory.glob("*.csv"))


def seed_users_csv_data():
    users_dir = DATA_PATH / 'users'
    user_csvs = find_csvs_in_directory(users_dir)
    # load csv files
    if not user_csvs:
        raise FileNotFoundError(f"No CSV files found in {users_dir}")

    users_df = pd.concat((pd.read_csv(csv, sep=';')
                         for csv in user_csvs), ignore_index=True)

    return users_df


def seed_orders_csv_data():
    orders_dir = DATA_PATH / 'orders'
    order_csvs = find_csvs_in_directory(orders_dir)
    # load csv files
    if not order_csvs:
        raise FileNotFoundError(f"No CSV files found in {orders_dir}")

    orders_df = pd.concat((pd.read_csv(csv, sep=';')
                          for csv in order_csvs), ignore_index=True)

    # Convert DataFrame to list of Order objects
    return orders_df


def seed_data_from_csvs(session):
    """
    Seed the database with data from CSV files.
    """
    users_df = seed_users_csv_data()
    orders_df = seed_orders_csv_data()
    np.random.seed(911)

    users = [User(**row.to_dict()) for _, row in users_df.iterrows()]
    session.bulk_save_objects(users)

    customer_ids = list(users_df.index)
    orders_df['customer_id'] = np.random.choice(
        list(customer_ids), size=len(orders_df), replace=True) + 1

    # Convert DataFrame to list of Order objects
    orders = [Order(**row.to_dict()) for _, row in orders_df.iterrows()]
    session.bulk_save_objects(orders)

    session.commit()


if __name__ == "__main__":
    from database.db_init import get_engine_and_session
    from flask_app.config import get_flask_config
    config = get_flask_config()
    engine, SessionLocal = get_engine_and_session(config)
    create_tables(engine)
    session = SessionLocal()
    seed_data_from_csvs(session)
    session.close()
