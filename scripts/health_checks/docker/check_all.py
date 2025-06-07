from logging import getLogger
from logging import basicConfig, INFO

from scripts.health_checks.docker import (
    check_postgres,
    check_zookeeper,
    check_schema_registry,
    check_connect
)

# Configure logging
basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = getLogger(__name__)

if __name__ == "__main__":
    # add other health checks here if necessary
    logger.info("Starting health checks for Docker services...")
    check_postgres.check_postgres()
    check_zookeeper.check_zookeeper()
    check_connect.check_connect()
    check_schema_registry.check_schema_registry()
    check_connect.check_connect()
    logger.info("All health checks completed.")
