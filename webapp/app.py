from flask import Flask

from containers.containers import containers_bp
from general.general import general_bp

app = Flask(__name__)

app.config.from_object('config.ProdConfig')

app.register_blueprint(general_bp)
app.register_blueprint(containers_bp, url_prefix='/containers')

if __name__ == '__main__':
    app.run(app.config["FLASK_SERVER_IP"], 
            port=app.config["FLASK_SERVER_PORT"])