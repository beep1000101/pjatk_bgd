from pathlib import Path
from typing import Final

import pandas as pd
import numpy as np

from database.models.base import Base

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
    ...


# Example usage (not for import!):
# from database.db_init import get_engine_and_session
# engine, SessionLocal = get_engine_and_session(database_uri)
# create_tables(engine)
# session = SessionLocal()
# seed_data(session)
