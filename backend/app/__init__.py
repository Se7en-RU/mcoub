import os

from flask import Flask

from app.routes import route
from app.config import config, init_config

def create_flask_app():
    app = Flask(__name__)

    route(app)

    path = os.environ.get('CONFIG_PATH') if os.environ.get(
        'CONFIG_PATH') else "./settings.ini"
    init_config(path)
    try:
        app.config.update(dict(
            SECRET_KEY=str(config['FLASK_APP']['FLASK_APP_SECRET_KEY'])
        ))
    except KeyError:
        print(f"\033[31m File {path} not found or incorrect")

    return app