from flask import Flask

from .data.mongoDb import init_db
from .routes.main import main
from .routes.todos import todos_router

def create_app():
    app = Flask(__name__)
    app.config.from_object('src.config.BaseConfig')

    # init the db
    init_db(app)

    # register routes
    app.register_blueprint(main)
    app.register_blueprint(todos_router)

    return app
