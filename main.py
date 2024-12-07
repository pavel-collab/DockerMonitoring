import time
import json
import os

from db_connection import DBConnection
from arguments_parsing import parse_connection_arguments

SLEEP_INTERVAL = 10 # sec

def main():
    try:
        connection_parameters = parse_connection_arguments()
    except RuntimeError as ex:
        print(f'[Err] exception has been caught during argument parsing: {ex}')

    try:
        db_connection = DBConnection(connection_parameters)
    except Exception as ex:
        print(f'[Err] exception has been caught during creating db connection: {ex}')

    try:
        while True:
            db_connection.collect_stats()
            time.sleep(SLEEP_INTERVAL)
    except KeyboardInterrupt:
        db_connection.close_db_connection()
        print("[INFO] end of collect docker stats")

if __name__ == '__main__':
    main()