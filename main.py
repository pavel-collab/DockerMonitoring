import time
import os
import logging
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src/backend')))
 
import logger_config

logger = logging.getLogger(__name__)

from db_connection import DBConnection
from arguments_parsing import parse_connection_arguments


APP_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = APP_ROOT_DIR + "/conf/"
CONNECTION_CONFIG_NAME = "connection.json"

SLEEP_INTERVAL = 10 # sec

def main():
    try:
        connection_parameters = parse_connection_arguments(CONFIG_PATH, CONNECTION_CONFIG_NAME)
    except RuntimeError:
        logger.critical(f'Exception has been caught during argument parsing.', exc_info=True)

    try:
        db_connection = DBConnection(connection_parameters)
    except Exception:
        logger.critical(f'Exception has been caught during creating db connection.', exc_info=True)
        exit(1)

    try:
        while True:
            db_connection.collect_stats()
            time.sleep(SLEEP_INTERVAL)
    except KeyboardInterrupt:
        db_connection.close_db_connection()
        logger.info("End of collect docker stats")

if __name__ == '__main__':
    main()