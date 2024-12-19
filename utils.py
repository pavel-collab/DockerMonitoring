from docker import DockerClient
import logger_config
import logging

logger = logging.getLogger(__name__)

def start_docker_client():
    try:
        docker_client = DockerClient(base_url='unix://var/run/docker.sock')
    except Exception:
        logger.error(f'Exception has been caught during starting docker client.', exc_info=True)
    return docker_client