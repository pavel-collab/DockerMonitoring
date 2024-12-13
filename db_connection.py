from docker import DockerClient
import psycopg2
from psycopg2 import OperationalError, errors
import os
import json
import time
import logging

import logger_config

logger = logging.getLogger(__name__)

from utils import ns2hours, byte2Kb

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
        # containers on the host
        host_containers = self.docker_client.containers.list()
        host_containers_ids = set([container.id for container in host_containers])
        if len(containers) == 0:
            return

        # containers, saved in the db table
        self.cursor.execute("SELECT * FROM container_info WHERE status = 'active'");
        saved_containers = self.cursor.fetchall()
        saved_containers_id = set([container[0] for container in saved_containers])

        # we're using operations with set to know, what containers has died
        died_containers = saved_containers_id - host_containers_ids
        # update status for all of the containers which died
        for container_id in died_containers:
            self.cursor.execute("UPDATE container_info SET status = 'died' WHERE id = %s", (container_id,))
        
        # now process the case when container has been already exists in table but with status 'died'
        # in this case we have to set it's status to active again
        existed_died_containers = host_containers_ids & saved_containers_id # intersection
        for container_id in existed_died_containers:
            self.cursor.execute("UPDATE container_info SET status = 'active' WHERE id = %s", (container_id))

        for container in host_containers:
            stats = container.stats(stream=False)

            container_name = stats['name']
            container_id = stats['id']

            memory_stats = self.get_container_memory_statistics(stats)
            cpu_stats = self.get_container_cpu_statistics(stats)
            network_stats = self.get_container_network_stats(stats)
            
            try:
                self.cursor.execute("SELECT EXISTS(SELECT 1 FROM container_info WHERE id = %s);", (container_id,))
                container_exists = self.cursor.fetchone()[0]
                if not container_exists:
                    self.cursor.execute(
                        "INSERT INTO container_info (id, name, memory_limit, status) VALUES (%s, %s, %s, 'active')",
                        (container_id, container_name, memory_stats['memory_limit'])
                    )

                self.cursor.execute(
                    "INSERT INTO container_stats (container_id, cpu_usage, memory_usage) VALUES (%s, %s, %s)",
                    (container_id, cpu_stats['cpu_usage'], memory_stats['memory_usage'])
                )
                self.cursor.execute(
                    "INSERT INTO container_detailed_statistics (id, kernel_cpu_usage, user_cpu_usage, system_cpu_usage) VALUES (%s, %s, %s, %s)",
                    (container_id, cpu_stats['kernel_cpu_usage'], cpu_stats['user_cpu_usage'], cpu_stats['system_cpu_usage'])
                )

                for network, net_stat in network_stats.items():
                    self.cursor.execute(
                        "INSERT INTO container_networks (id, network_name, resieved_bytes, transmited_bytes) VALUES (%s, %s, %s, %s)",
                        (container_id, network, net_stat['resieved_bytes'], net_stat['transmited_bytes'])
                    )
                self.conn.commit()
            except Exception:
                logger.critical(f"Exception was caught while tring to collect statistics", exc_info=True)

    def close_db_connection(self):
        self.cursor.close()
        self.conn.close()
        logger.info("Closed Connection!")

    def get_container_cpu_statistics(self, stats):
        '''
        This metrics in nanoseconds -- how many nanoseconds container take on a cpu, in user mode, etc
        '''
        cpu_usage        = stats['cpu_stats']['cpu_usage']['total_usage']
        kernel_cpu_usage = stats['cpu_stats']['cpu_usage']['usage_in_kernelmode']
        user_cpu_usage   = stats['cpu_stats']['cpu_usage']['usage_in_usermode']
        system_cpu_usage = stats['cpu_stats']['system_cpu_usage']

        cpu_stats = {
            "cpu_usage": ns2hours(cpu_usage),
            "kernel_cpu_usage": ns2hours(kernel_cpu_usage),
            "user_cpu_usage": ns2hours(user_cpu_usage),
            "system_cpu_usage": ns2hours(system_cpu_usage)
        }
        return cpu_stats

    def get_container_memory_statistics(self, stats):
        memory_usage = stats['memory_stats']['usage']
        memory_limit = stats['memory_stats']['limit']

        memory_stats = {
            'memory_usage': byte2Kb(memory_usage),
            'memory_limit': byte2Kb(memory_limit)
        }
        return memory_stats
    
    def get_container_network_stats(self, stats):
        network_stats = {}
        for network in stats['networks'].keys():
            network_stats[network] = {
                "resieved_bytes": stats['networks'][network]['rx_bytes'],
                "transmited_bytes": stats['networks'][network]['tx_packets']
            }
        return network_stats
