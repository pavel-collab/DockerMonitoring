import sys
import secrets

from flask import Flask
from logging.config import dictConfig
import psycopg as dbm

from containers.containers import containers_bp
from general.general import general_bp
from utils.config import load_webapp_config
from utils.logging import get_webapp_dictConfig
from utils.cache import cache

DEFAULT_LOG_DIRECTORY = "logs"
CORE_LOG_FILE = "webapp_logs.log"

try:
    dict_config = get_webapp_dictConfig(DEFAULT_LOG_DIRECTORY, CORE_LOG_FILE)
except OSError:
    print("Setting up custom log config failed. Using default.")
else:
    dictConfig(dict_config)

try:
    app = Flask(__name__)
except Exception:
    print("Can't create Flask app! Interrupting app run.")
    sys.exit(1)

try:
    with app.app_context():
        config = load_webapp_config('config.json')
except Exception:
    app.logger.critical("Can't retrieve settings from config! Interrupting app run.", exc_info=True)
    sys.exit(1)
else:
    app.config.from_object(config)

conn = None
try:
    conn = dbm.connect(app.config["DB_URI"])
except Exception:
    if conn is not None:
        conn.close()
    app.logger.critical("Error during test connection to database. "
                        "Check logs and verify that all config settings are correct. "
                        "Interrupting app run.", exc_info=True)
    sys.exit(1)
else:
    if conn is not None:
        conn.close()
    

try:
    secret = secrets.token_hex()
    app.config.update(
        SECRET_KEY=secret
    )
except Exception:
    app.logger.critical("Can't generate secret key for secure connection! Interrupting app run.", exc_info=True)
    sys.exit(1)

try:
    with app.app_context():
        app.register_blueprint(general_bp)
        app.register_blueprint(containers_bp, url_prefix='/containers')
except Exception:
    app.logger.critical("Can't register blueprints for app! Interrupting app run.", exc_info=True)
    sys.exit(1)

try:
    cache.init_app(app)
except Exception:
    app.logger.critical("Error while configuring cache! Interrupting app run.", exc_info=True)
    sys.exit(1)

if __name__ == '__main__':
    try:
        app.run(app.config["FLASK_SERVER_IP"], port=app.config["FLASK_SERVER_PORT"])
    except Exception:
        app.logger.critical("Error while running app! Interrupting app run.", exc_info=True)
        sys.exit(1)
    