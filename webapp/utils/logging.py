import logging
import os
from pathlib import Path

# Special formatter for console messages. 
# Only want to see exception info in logfile.
class ConsoleFormatter(logging.Formatter):
    def format(self, record):
        if record.exc_info:
            record.exc_info = (None, record.exc_info[1], None)
            record.exc_text = None
        result = super().format(record)
        return result


custom_dict_config = {
    'version': 1,
    'formatters': {
        'file': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
        'console' : {
            '()': 'utils.logging.ConsoleFormatter',
            'format': '%(message)s',
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'file',
            'level': 'DEBUG',
            'filename': 'logconfig.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7
        },
        'console': {
            'class' : 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'console',
            'level': 'ERROR'
        }
    },
    'loggers': {
        'root': {
            'level': 'INFO',
            'handlers': ['file', 'console'],
        }
    }
}

def get_webapp_dictConfig(log_dir, log_filename) -> dict:
    """
    Checks if it is possible to access log directory and
    logfile and returns dictconfig or raises exception 
    depending on the result.
    """
    try:
        Path(log_dir).mkdir(parents=True, exist_ok=True)
    except OSError:
        print("Can't access or create logs directory. Using root for log files.")
        log_file_path = log_filename
    else:
        log_file_path = os.path.join(log_dir, log_filename)

    if not os.path.exists(log_file_path):
        print('Logfile does not exists. Creating.')
        try:
            open(log_file_path, 'w').close()
        except OSError:
            print('Error during creating logfile.')
            raise
        
    custom_dict_config['handlers']['file']['filename'] = log_file_path

    return custom_dict_config
        


    