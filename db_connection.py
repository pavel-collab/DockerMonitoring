from docker import DockerClient
import psycopg2
from psycopg2 import OperationalError
import os
import json
import time
import logging

import logger_config

logger = logging.getLogger(__name__)

MAX_CONNECTION_ATTEMPTS = 8
DELAY = 2

class DBConnection:
    def __init__(self, connection_parameters):
        if not set(['dbname', 'host_ip', 'user', 'port']).issubset(set(connection_parameters.keys())):
            raise RuntimeError(f"There are not all parameters in the connection config: {connection_parameters.keys()}")

        self.connect_db(connection_parameters)
        self.start_docker_client()

    def connect_db(self, connection_parameters):
        attempts = 0
        while attempts < MAX_CONNECTION_ATTEMPTS:
            try:
                self.conn = psycopg2.connect(
                    dbname=connection_parameters['dbname'],
                    user=connection_parameters['user'],
                    host=connection_parameters['host_ip'],
                    port=connection_parameters['port']
                )
                self.cursor = self.conn.cursor()
                logger.info("Connection Success!")
                return 
            except OperationalError:
                attempts += 1
                logger.error(f"Attempt {attempts}/{MAX_CONNECTION_ATTEMPTS}", exc_info=True)
                time.sleep(DELAY)
            except Exception:
                logger.critical(f'Exception has been caught during establishing connection to db.', exc_info=True)
            finally:
                if 'connection' in locals() and self.conn is not None:
                    self.conn.close()
        raise RuntimeError("max attempts of connection overlay")

    def start_docker_client(self):
        try:
            self.docker_client = DockerClient(base_url='unix://var/run/docker.sock')
        except Exception:
            logger.error(f'Exception has been caught during starting docker client.', exc_info=True)

    def collect_stats(self):
        containers = self.docker_client.containers.list()
        for container in containers:
            stats = container.stats(stream=False)
            cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']

            if not 'memory_stats' in stats:
                memory_usage = None
            else:
                memory_usage = stats['memory_stats']['usage']
            
            container_id = container.id

            self.cursor.execute(
                "INSERT INTO container_stats (container_id, cpu_usage, memory_usage) VALUES (%s, %s, %s)",
                (container_id, cpu_usage, memory_usage)
            )
            self.conn.commit()

    def close_db_connection(self):
        self.cursor.close()
        self.conn.close()
        logger.info("Closed Connection!")