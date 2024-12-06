# webapp config
from os import environ, path

# importing secret key from environment variable
basedir = path.abspath(path.dirname(__file__))

class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    FLASK_SERVER_IP = '0.0.0.0'
    FLASK_SERVER_PORT = 5010
    DB_TYPE = 'postgresql'
    DB_NAME = 'containers'
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_USER = 'postgres'
    DB_PASSWORD = ''

    @property
    def DB_URI(self): 
        return "{}://{}:{}@{}:{}/{}".format(
            self.DB_TYPE, self.DB_USER, self.DB_PASSWORD,
            self.DB_HOST, self.DB_PORT, self.DB_NAME
        )


class ProdConfig(Config):
    DEBUG = False
    FLASK_SERVER_IP = environ.get('FLASK_SERVER_IP')

class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    DB_URI = environ.get('DEV_DATABASE_URI')
    # TODO: Is it possible to check this DB_URI before assignment?
    # Definitely yes, but if inside property works badly