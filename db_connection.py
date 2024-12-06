from docker import DockerClient
import psycopg2
import os
import json

APP_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_POSTGRES_PORT = 5432
DEFAULT_POSTGRES_USER = "postgres"
DEFAULT_POSTGRES_DB = "postgres"

CONFIG_PATH = {APP_ROOT_DIR} + "/conf/"
CONNECTION_CONFIG_NAME = "connection.json"

def parse_connection_arguments():
    connection_parameters = {}
    with open(CONFIG_PATH + "/" + CONNECTION_CONFIG_NAME) as connection_config_file:
        json_parameters = json.load(connection_config_file)
        if not set(['dbname', 'host_ip', 'user', 'port']).issubset(set(json_parameters.keys())):
            raise RuntimeError("There are not all parameters in the connection configuration file.")
        
        connection_parameters['dbname'] = DEFAULT_POSTGRES_DB if json_parameters['dbname'] == 'default' else json_parameters['dbname']
        connection_parameters['user'] = DEFAULT_POSTGRES_USER if json_parameters['user'] == 'default' else json_parameters['user']
        connection_parameters['port'] = DEFAULT_POSTGRES_PORT if json_parameters['port'] == 'default' else json_parameters['port']
        connection_parameters['host_ip'] = json_parameters['host_ip']
        if json_parameters['password'] != "":
            connection_parameters['password'] = json_parameters['password']

    return connection_parameters

#! need to make a real class, on this stage it uses more like C-structures (collection of the objects)
#! need to move connect_db and close_connection to the class methods
class DBConnection:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

def connect_db():
    try:
        connection_parameters = parse_connection_arguments()
    except RuntimeError as ex:
        print(f'[Err] exception has been caught during argument parsing: {ex}')

    try:
        conn = psycopg2.connect(
            dbname=connection_parameters['dbname'],
            user=connection_parameters['user'],
            host=connection_parameters['host_ip'],
            port=connection_parameters['port']
        )
        cursor = conn.cursor()
    except Exception as ex:
        print(f'[Err] exception has been caught during establishing connection to db: {ex}')

    db_connection = DBConnection(conn=conn,
                                 cur=cursor)
    return db_connection

def start_docker_client():
    try:
        docker_client = DockerClient(base_url='unix://var/run/docker.sock')
    except Exception as ex:
        print(f'[Err] exception has been caught during starting docker client: {ex}')
    return docker_client

def collect_stats(docker_client, db_connection):
    containers = docker_client.containers.list()
    for container in containers:
        stats = container.stats(stream=False)
        cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
        memory_usage = stats['memory_stats']['usage']
        container_id = container.id

        # Вставка данных в TimescaleDB
        db_connection.cursor.execute(
            "INSERT INTO container_stats (container_id, cpu_usage, memory_usage) VALUES (%s, %s, %s)",
            (container_id, cpu_usage, memory_usage)
        )
        db_connection.conn.commit()

def close_db_connection(db_connection):
    db_connection.cursor.close()
    db_connection.conn.close()