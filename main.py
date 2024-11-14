import time
import psycopg2
from docker import DockerClient

# Подключение к TimescaleDB
conn = psycopg2.connect(
    dbname='postgres',
    user=  'postgres',
    # password='your_password',
    host='192.168.0.143',  # или ваш хост TimescaleDB
    port='5432'
)
cursor = conn.cursor()

# Создание Docker клиента
docker_client = DockerClient(base_url='unix://var/run/docker.sock')

def collect_stats():
    containers = docker_client.containers.list()
    for container in containers:
        stats = container.stats(stream=False)
        cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
        memory_usage = stats['memory_stats']['usage']
        container_id = container.id

        # Вставка данных в TimescaleDB
        cursor.execute(
            "INSERT INTO container_stats (container_id, cpu_usage, memory_usage) VALUES (%s, %s, %s)",
            (container_id, cpu_usage, memory_usage)
        )
        conn.commit()

try:
    while True:
        collect_stats()
        time.sleep(10)  # Интервал сбора статистики
except KeyboardInterrupt:
    cursor.close()
    conn.close()
    print("[INFO] end of collect docker stats")
