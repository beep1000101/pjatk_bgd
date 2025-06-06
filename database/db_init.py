from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def init_db(testing=False):
    """
    Initialize the database engine and session factory.

    Parameters
    ----------
    testing : bool, optional
        If True, use an in-memory SQLite database for testing. Defaults to False.

    Returns
    -------
    tuple
        A tuple containing the database engine and session factory.

    Notes
    -----
    This function sets up the database connection and session factory. It uses
    an in-memory database for testing or a file-based SQLite database for production.

    Examples
    --------
    >>> engine, SessionLocal = init_db(testing=True)
    """
    if testing:
        database_url = 'sqlite:///:memory:'
    else:
        stem = Path(__file__).parent.name
        database_url = f'sqlite:///{stem}/pokemon.db'

    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal


# Initialize the database based on the TESTING flag
engine, SessionLocal = init_db(testing=False)
