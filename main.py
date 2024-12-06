import time
import json
import os

import db_connection

SLEEP_INTERVAL = 10 # sec

def main():
    db_connection = db_connection.connect_db()
    docker_client = db_connection.start_docker_client()

    try:
        while True:
            db_connection.collect_stats(docker_client=docker_client,
                          db_connection=db_connection)
            time.sleep(SLEEP_INTERVAL)
    except KeyboardInterrupt:
        db_connection.close_db_connection(db_connection=db_connection)
        print("[INFO] end of collect docker stats")

if __name__ == '__main__':
    main()