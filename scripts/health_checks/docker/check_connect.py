import os
import requests
from logging import basicConfig, INFO, getLogger

from scripts.health_checks.docker.utils.track_health import track_health

basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = getLogger(__name__)


@track_health()
def check_connect():
    logger.info("Checking Kafka Connect health...")
    url = f"http://{os.getenv('CONNECT_HOST', 'localhost')}:{os.getenv('CONNECT_PORT', 8083)}/connectors"
    logger.info(f"Connecting to Kafka Connect at {url}")
    try:
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            logger.info("Kafka Connect is healthy")
        else:
            logger.warning(
                f"Kafka Connect returned unexpected status: {r.status_code}")
    except Exception as e:
        logger.error(f"Kafka Connect health check failed: {e}")


if __name__ == "__main__":
    check_connect()
