import psycopg2
from time import sleep

import utils_test

from db_connection import DBConnection

import logging

import logger_config

logger = logging.getLogger(__name__)

DOCKER_IMAGES = {
    "ubuntu": "ubuntu:latest"
}

#TODO: exchange to the config values
DB_NAME = "postgres"
DB_USER = "postgres"
DB_HOST = "192.168.0.143"
DB_PORT = 5432

DB_TABLE_LIST = ["container_info", "container_stats", "container_detailed_statistics", "container_networks"]

PATH_TO_LOG = None
try:
    PATH_TO_LOG = logger_config.get_logfile_path()
    print(f"DEBUG path to logfile {PATH_TO_LOG}")
except RuntimeError as ex:
    print(f"Error -- {ex}")
    exit(1)

def test_collect_container_info():
    utils_test.clear_log(PATH_TO_LOG)
    container = utils_test.start_docker_container(DOCKER_IMAGES["ubuntu"])

    connection_parameters = {
        "dbname": DB_NAME,
        "user": DB_USER,
        "port": DB_PORT,
        "host_ip": DB_HOST
    }

    db_connection = DBConnection(connection_parameters)

    for _ in range(10):
        db_connection.collect_stats()
        sleep(2)

    db_connection.close_db_connection()    
    utils_test.stop_docker_container(container)
    assert utils_test.check_log_file(PATH_TO_LOG)

# def test_check_db_tables():
#     conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, port=DB_PORT)
#     cursor = conn.cursor()
    
#     utils_test.clear_db_tables(cursor, DB_TABLE_LIST)
#     container = utils_test.start_docker_container(DOCKER_IMAGES["ubuntu"])
    
#     utils_test.stop_docker_container(container)    

#     for table_name in DB_TABLE_LIST:
#         assert utils_test.check_table_content_excists(cursor, table_name)
