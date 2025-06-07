import os
from logging import basicConfig, INFO, getLogger

import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Configure logging
basicConfig(
    level=INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = getLogger(__name__)


def check_postgres():
    logger.info("Starting PostgreSQL health check...")
    try:
        # log host and port for debugging
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", 5432)
        logger.info(f"Connecting to PostgreSQL at {host}:{port}")
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB", "postgres"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "postgres"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", 5432),
            connect_timeout=3
        )
        conn.close()
        logger.info("PostgreSQL health check passed.")
    except Exception as e:
        logger.error(f"PostgreSQL health check failed: {e}")


if __name__ == "__main__":
    check_postgres()
