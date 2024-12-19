import psycopg2
from time import sleep

import utils_test

PATH_TO_LOG = ""
DOCKER_IMAGES = {
    "ubuntu": "ubuntu:latest"
}

#TODO: exchange to the config values
DB_NAME = "postgres"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = 5432

DB_TABLE_LIST = ["container_info", "container_stats", "container_detailed_statistics", "container_networks"]

def test_collect_container_info():
    utils_test.clear_log(PATH_TO_LOG)
    container = utils_test.start_docker_container(DOCKER_IMAGES["ubuntu"])
    sleep(10)
    utils_test.stop_docker_container(container)
    assert utils_test.check_log_file(PATH_TO_LOG)

def test_check_db_tables():
    conn = psycopg2.connect(DB_NAME, DB_USER, DB_HOST, DB_PORT)
    cursor = conn.cursor()
    
    utils_test.clear_db_tables(cursor, DB_TABLE_LIST)
    container = utils_test.start_docker_container(DOCKER_IMAGES["ubuntu"])
    sleep(10)
    utils_test.stop_docker_container(container)    

    for table_name in DB_TABLE_LIST:
        assert utils_test.check_table_content_excists(cursor, table_name)
