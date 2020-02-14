from flask import Flask

from .data.mongoDb import initDB
from .routes.main import main

def create_app():
    app = Flask(__name__)
    app.config.from_object('src.config.BaseConfig')
    initDB(app)
    app.register_blueprint(main)

    return app
