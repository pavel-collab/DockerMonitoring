import json

from flask import current_app

class Config:
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

def load_webapp_config(config_filename : str) -> Config:
    """
    Load web app config from passed file, check its fields 
    and return config instance, prepared for use with flask config.

    Parameters
    ----------
    config_filename : str
        Name of config file

    Returns
    ----------
    config : Config
        Processed config.
    """
    config = Config()
    try:
        with open(config_filename, 'r') as config_file:
            config_data = json.load(config_file)
    except OSError:
        print("Error while opening config file! Using default settings.")
        current_app.logger.error("Error while opening config file! Using default settings.", exc_info=True)
        return config
    
    for key, def_value in vars(config).items():
        if key in config_data:
            passed_value = config_data[key]
            if type(def_value) is type(passed_value):
                setattr(config, key, passed_value)
            else:
                current_app.logger.error(f"Value for key {key} from passed config has different from default value type. "
                                         f"Passed value type is {type(passed_value)}, but default value type is {type(def_value)}.")
        else:
            current_app.logger.error(f"There is no key {key} in passed config. Using default value: {def_value}")

    return config
    
    


    