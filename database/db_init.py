from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask_app.config import get_flask_config


def get_engine_and_session(config=None):
    """
    Create SQLAlchemy engine and sessionmaker from a database URI.
    """
    if config is None:
        config = get_flask_config()
    database_uri = config.SQLALCHEMY_DATABASE_URI
    engine = create_engine(database_uri)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal


# Usage:
# In your Flask app, after app.config is loaded, do:
# from database.db_init import get_engine_and_session
# engine, SessionLocal = get_engine_and_session(app.config["SQLALCHEMY_DATABASE_URI"])
