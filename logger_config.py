import logging
import os

DEFAULT_LOG_DIRECTORY = "logs"
CORE_LOG_FILE = "core.log"

def setup_logger():
    if not os.path.exists(DEFAULT_LOG_DIRECTORY):
        os.makedirs(DEFAULT_LOG_DIRECTORY)
    
    log_file_path = os.path.join(DEFAULT_LOG_DIRECTORY, CORE_LOG_FILE)

    # Here we're able to set particular lever for each handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)

    logging.basicConfig(
        # set up level of the logs DEBUG -- for developers, INFO -- for production
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            stream_handler, # writing logs to logfile
            file_handler    # writing logs to stdout
        ]
    )

setup_logger()