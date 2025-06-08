from pathlib import Path
from typing import Final

import pandas as pd
import numpy as np

from database.models.base import Base
from database.models.users import User
from database.models.orders import Order

DATA_PATH: Final[Path] = Path(__file__).parent / 'data'


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


# Example usage (not for import!):
# from database.db_init import get_engine_and_session
# engine, SessionLocal = get_engine_and_session(database_uri)
# create_tables(engine)
# session = SessionLocal()
# seed_data(session)

if __name__ == "__main__":
    from database.db_init import get_engine_and_session
    from flask_app.config import get_flask_config
    config = get_flask_config()
    engine, SessionLocal = get_engine_and_session(config)
    create_tables(engine)
    session = SessionLocal()
    seed_data(session)
    session.close()
