# import os
# from pathlib import Path
# from enum import StrEnum

# from dotenv import load_dotenv

# load_dotenv()
# basedir = Path(__file__).resolve().parent


# class BaseConfig:
#     """
#     Shared settings for all configurations.

#     Attributes
#     ----------
#     SECRET_KEY : str
#         The secret key for the application.
#     SQLALCHEMY_TRACK_MODIFICATIONS : bool
#         Whether to track modifications of objects in SQLAlchemy.
#     JSON_SORT_KEYS : bool
#         Whether to sort keys in JSON responses.
#     """
#     SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     JSON_SORT_KEYS = False


# class DevelopmentConfig(BaseConfig):
#     """
#     Configuration for local development.

#     Attributes
#     ----------
#     DEBUG : bool
#         Enables debug mode.
#     db_name : str
#         The name of the SQLite database file.
#     SQLALCHEMY_DATABASE_URI : str
#         The URI for the SQLite database.
#     """
#     DEBUG = True
#     db_name = os.getenv('DB_NAME')
#     SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / db_name}"


# class TestingConfig(BaseConfig):
#     """
#     Configuration for testing.

#     Attributes
#     ----------
#     TESTING : bool
#         Enables testing mode.
#     SQLALCHEMY_DATABASE_URI : str
#         The URI for the in-memory SQLite database.
#     """
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


# class ProductionConfig(BaseConfig):
#     """
#     Configuration for production using a POSTGRES database.
#     """
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = os.getenv(
#         'DATABASE_URL', 'postgresql://user:password@localhost/dbname')


# class ConfigType(StrEnum):
#     """
#     Enum for configuration types.

#     Attributes
#     ----------
#     DEVELOPMENT : str
#         Development configuration.
#     TESTING : str
#         Testing configuration.
#     PRODUCTION : str
#         Production configuration.
#     """
#     DEVELOPMENT = 'development'
#     TESTING = 'testing'
#     PRODUCTION = 'production'


# configurations = {
#     ConfigType.DEVELOPMENT: DevelopmentConfig,
#     ConfigType.TESTING: TestingConfig,
#     ConfigType.PRODUCTION: ProductionConfig
# }
