from logging import getLogger
from logging import basicConfig, INFO

from scripts.health_checks.docker import (
    check_postgres,
    check_zookeeper,
    check_schema_registry,
    check_connect
)

from scripts.health_checks.docker.utils.track_health import health_stats

# Configure logging
basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = getLogger(__name__)


def log_health_stats(stats=health_stats):
    total_checks = len(stats)
    success_number = stats.success
    failure_number = stats.failure
    logger.info(f"Total health checks performed: {total_checks}")
    logger.info(f"Successful checks: {success_number}")
    if failure_number > 0:
        logger.warning(f"Health checks failed: {failure_number}")
    else:
        logger.info(f"Failed checks: {failure_number}")


if __name__ == "__main__":
    # add other health checks here if necessary
    logger.info("Starting health checks for Docker services...")
    check_postgres.check_postgres()
    check_zookeeper.check_zookeeper()
    check_connect.check_connect()
    check_schema_registry.check_schema_registry()
    check_connect.check_connect()
    log_health_stats(stats=health_stats)
    logger.info("All health checks completed.")
    if health_stats.failure > 0:
        logger.error(
            "Some health checks failed."
            "Please check the logs for details."
        )
