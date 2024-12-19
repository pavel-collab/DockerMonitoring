import time
import json
import os
import logging

import logger_config

logger = logging.getLogger(__name__)

from db_connection import DBConnection, StatsCollector
from arguments_parsing import parse_connection_arguments
from utils import start_docker_client

SLEEP_INTERVAL = 10 # sec

def main():
    try:
        connection_parameters = parse_connection_arguments()
    except RuntimeError:
        logger.critical(f'Exception has been caught during argument parsing.', exc_info=True)

    try:
        db_connection = DBConnection(connection_parameters)
    except Exception:
        logger.critical(f'Exception has been caught during creating db connection.', exc_info=True)
        exit(1)

    docker_client = start_docker_client()

    stats_collector = StatsCollector(db_connection, docker_client)

    try:
        while True:
            stats_collector.collect_stats()
            time.sleep(SLEEP_INTERVAL)
    except KeyboardInterrupt:
        db_connection.close_db_connection()
        logger.info("End of collect docker stats")

if __name__ == '__main__':
    main()