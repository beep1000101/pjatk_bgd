import pytest

from database.db_init import get_engine_and_session
from database.models.base import Base

from flask_app.config import TestingConfig


@pytest.fixture(scope="module")
def engine_and_session():
    # Use in-memory SQLite for testing
    engine, SessionLocal = get_engine_and_session(TestingConfig)
    # Create all tables before tests
    Base.metadata.create_all(engine)
    return engine, SessionLocal


@pytest.fixture(scope="module")
def session(engine_and_session):
    _, SessionLocal = engine_and_session
    session = SessionLocal()
    yield session
    session.close()


def test_database_connection(engine_and_session):
    engine, _ = engine_and_session
    assert engine is not None


def test_session_creation(session):
    assert session is not None
