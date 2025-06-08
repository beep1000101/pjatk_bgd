import os
from logging import basicConfig, INFO, getLogger

import requests

from scripts.health_checks.docker.utils.track_health import track_health
from scripts.health_checks.docker.utils.health_exception import HealthCheckError

basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = getLogger(__name__)


@track_health()
def check_schema_registry():
    logger.info("Checking Schema Registry health...")
    url = f"http://{os.getenv('SCHEMA_REGISTRY_HOST', 'localhost')}:{os.getenv('SCHEMA_REGISTRY_PORT', 8081)}/subjects"
    logger.info(f"Connecting to Schema Registry at {url}")
    try:
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            logger.info("Schema Registry is healthy")
        else:
            logger.warning(
                f"Schema Registry returned unexpected status: {r.status_code}")
    except Exception as e:
        logger.error(f"Schema Registry health check failed: {e}")
        raise HealthCheckError(f"Schema Registry health check failed: {e}")


if __name__ == "__main__":
    check_schema_registry()
