from pathlib import Path
from typing import Final

import pandas as pd
import numpy as np

from database.db_init import engine, SessionLocal
from flask.models.base import Base

DATA_PATH: Final[Path] = Path(__file__).parent / 'data'


def create_tables(bind=None):
    """
    Create all tables defined on Base.metadata.

    Parameters
    ----------
    bind : Engine or Connection, optional
        The database bind to use. Defaults to the top‐level engine.
    """
    bind = bind or engine
    Base.metadata.create_all(bind)


def seed_data(session=None):
    ...


if __name__ == "__main__":
    create_tables()
    seed_data()
