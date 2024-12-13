import os
import json
import logging

import src.backend.logger_config

logger = logging.getLogger(__name__)

DEFAULT_POSTGRES_PORT = 5432
DEFAULT_POSTGRES_USER = "postgres"
DEFAULT_POSTGRES_DB = "postgres"
DEFAULT_POSTGRES_HOST = 'localhost'

DEFAULT_PARAMETERS = {
    'dbname': DEFAULT_POSTGRES_DB,
    'user': DEFAULT_POSTGRES_USER,
    'port': DEFAULT_POSTGRES_PORT,
    'host_ip': DEFAULT_POSTGRES_HOST
}

def get_parameter_from_json(parameter_name, json_parameters, connection_parameters):
    if (parameter_name not in json_parameters.keys()) or (json_parameters[parameter_name] == 'default'):
        connection_parameters[parameter_name] = DEFAULT_PARAMETERS[parameter_name]
    else:
        connection_parameters[parameter_name] = json_parameters[parameter_name]

def parse_connection_arguments(config_path, connection_config_name):
    connection_parameters = {}
    config_file_path = f"{config_path}/{connection_config_name}"

    try:
        with open(config_file_path) as connection_config_file:
            json_parameters = json.load(connection_config_file)
            
            get_parameter_from_json('dbname', json_parameters, connection_parameters)
            get_parameter_from_json('user', json_parameters, connection_parameters)
            get_parameter_from_json('port', json_parameters, connection_parameters)     
            get_parameter_from_json('host_ip', json_parameters, connection_parameters)
    except FileNotFoundError:
        logger.error(f"File not found: {config_file_path}", exc_info=True)
    except PermissionError:
        logger.error(f"File permission denied: {config_file_path}", exc_info=True)
    except Exception:
        logger.error(f"Error during file open", exc_info=True)

    return connection_parameters.copy()