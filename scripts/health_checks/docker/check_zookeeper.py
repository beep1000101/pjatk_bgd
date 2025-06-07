import os
import socket
from logging import basicConfig, INFO, getLogger

basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = getLogger(__name__)


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


if __name__ == "__main__":
    check_zookeeper()
