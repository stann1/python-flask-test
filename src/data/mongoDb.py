from flask_pymongo import PyMongo

mongo = PyMongo()

def init_db(app):
    mongo_uri = app.config["DATABASE_URI"]
    mongo.init_app(app, uri=mongo_uri)
    return mongo