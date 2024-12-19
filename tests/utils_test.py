import docker
import psycopg2

def clear_db_tables(cursor, table_list: list):
    for table_name in table_list:
        cursor.execute(f"DELETE FROM TABLE {table_name};")

#TODO: write clean views
def clear_db_views(cursor):
    ...

def clear_log(path_to_logfile):
    fd = open(path_to_logfile, "w")
    fd.write("")
    fd.close()

def check_log_file(path_to_logfile):
    with open(path_to_logfile, "r") as fd:
        log_content = fd.read().split('\n')
        for line in log_content:
            if "ERROR" in line or "CRITICAL" in line:
                return False
    return True

def check_docker_image_excists(image_name):
    client = docker.from_env()
    images = client.images.list()
    image_exists = any(image_name in str(image.tags) for image in images)
    return image_exists

def start_docker_container(image_name: str):
    # Создаем клиент Docker
    client = docker.from_env()

    #TODO: refactor
    if not check_docker_image_excists(image_name):
        print(f"Error there is no such image {image_name} in system.\nTry to use docker pull {image_name} and start test again.")
        exit(1)

    try:
        # Запускаем контейнер
        container = client.containers.run(image_name, detach=True)
    #TODO: process exception
    except Exception as ex:
        exit(1)
    
    return container

def stop_docker_container(container):
    try:
        container.stop()
    #TODO: process exception
    except Exception as ex:
        exit(1)

def check_table_content_excists(cursor, table_name):
    cursor.execute(f'SELECT COUNT(*) FROM {table_name};')
    count = cursor.fetchone()[0]
    return count > 0