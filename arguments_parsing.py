import os
import json

APP_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_POSTGRES_PORT = 5432
DEFAULT_POSTGRES_USER = "postgres"
DEFAULT_POSTGRES_DB = "postgres"

CONFIG_PATH = APP_ROOT_DIR + "/conf/"
CONNECTION_CONFIG_NAME = "connection.json"

def parse_connection_arguments():
    connection_parameters = {}
    config_file_path = f"{CONFIG_PATH}/{CONNECTION_CONFIG_NAME}"
    if not os.path.isfile(config_file_path):
        print(f"Error, there is no file {config_file_path}")
        raise Exception(f"Error, there is no file {config_file_path}")

    with open() as connection_config_file:
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