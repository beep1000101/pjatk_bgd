import os
import socket
from logging import basicConfig, INFO, getLogger

from scripts.health_checks.docker.utils.track_health import track_health
from scripts.health_checks.docker.utils.health_exception import HealthCheckError

basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = getLogger(__name__)


@track_health()
def check_zookeeper():
    logger.info("Checking Zookeeper health...")
    host = os.getenv("ZOOKEEPER_HOST", "localhost")
    port = int(os.getenv("ZOOKEEPER_PORT", 2181))
    logger.info(f"Connecting to Zookeeper at {host}:{port}")
    try:
        with socket.create_connection((host, port), timeout=3):
            logger.info("Zookeeper is healthy")
    except Exception as e:
        logger.error(f"Zookeeper health check failed: {e}")
        raise HealthCheckError(f"Zookeeper health check failed: {e}")


if __name__ == "__main__":
    check_zookeeper()
