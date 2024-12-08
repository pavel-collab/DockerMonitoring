import logging
import os

DEFAULT_LOG_DIRECTORY = "logs"
CORE_LOG_FILE = "core.log"

def setup_logger():
    if not os.path.exists(DEFAULT_LOG_DIRECTORY):
        os.makedirs(DEFAULT_LOG_DIRECTORY)
    
    log_file_path = os.path.join(DEFAULT_LOG_DIRECTORY, CORE_LOG_FILE)
    
    logging.basicConfig(
        # set up level of the logs DEBUG -- for developers, INFO -- for production
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path), # writing logs to logfile
            logging.StreamHandler()             # writing logs to stdout
        ]
    )

setup_logger()