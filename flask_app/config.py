import os
from pathlib import Path
from enum import StrEnum

from dotenv import load_dotenv

load_dotenv()
basedir = Path(__file__).resolve().parent


class BaseConfig:
    """
    Shared settings for all configurations.

    Attributes
    ----------
    SECRET_KEY : str
        The secret key for the application.
    SQLALCHEMY_TRACK_MODIFICATIONS : bool
        Whether to track modifications of objects in SQLAlchemy.
    JSON_SORT_KEYS : bool
        Whether to sort keys in JSON responses.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))


class DevelopmentConfig(BaseConfig):
    """
    Configuration for local development.

    Attributes
    ----------
    DEBUG : bool
        Enables debug mode.
    db_name : str
        The name of the SQLite database file.
    SQLALCHEMY_DATABASE_URI : str
        The URI for the SQLite database.
    """
    debug = True
    DB_NAME = os.getenv('DB_NAME', 'mydb')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(BaseConfig):
    """
    Configuration for testing.

    Attributes
    ----------
    TESTING : bool
        Enables testing mode.
    SQLALCHEMY_DATABASE_URI : str
        The URI for the in-memory SQLite database.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(BaseConfig):
    """
    Configuration for production using a POSTGRES database.
    """
    debug = False
    user = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASSWORD', 'postgres')
    DB_HOST = os.getenv('DB_HOST', 'postgres')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'mydb')
    if not all([user, password, DB_HOST, DB_PORT, DB_NAME]):
        raise ValueError(
            "Database configuration environment variables are not set. "
            "Please set DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, and DB_NAME."
        )
    SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


class ConfigType(StrEnum):
    """
    Enum for configuration types.

    Attributes
    ----------
    DEVELOPMENT : str
        Development configuration.
    TESTING : str
        Testing configuration.
    PRODUCTION : str
        Production configuration.
    """
    DEVELOPMENT = 'development'
    TESTING = 'testing'
    PRODUCTION = 'production'


configurations = {
    ConfigType.DEVELOPMENT: DevelopmentConfig,
    ConfigType.TESTING: TestingConfig,
    ConfigType.PRODUCTION: ProductionConfig
}


def get_flask_config(current_config=None):
    """
    Get the current Flask configuration based on the FLASK_ENV environment variable.

    Returns
    -------
    BaseConfig
        The configuration object for the current environment.

    Raises
    ------
    ValueError
        If FLASK_ENV is not set or is invalid.
    """
    if current_config is None:
        current_config = os.getenv('FLASK_ENV')

    if current_config is None:
        raise ValueError(
            "FLASK_ENV environment variable is not set. "
            "Please set it to 'development', 'testing', or 'production'."
        )

    flask_cofig = configurations.get(current_config)
    if flask_cofig is None:
        raise ValueError(
            f"Invalid FLASK_ENV value: {current_config}. "
            "Please set it to 'development', 'testing', or 'production'."
        )
    return flask_cofig
