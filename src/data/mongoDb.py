from flask_pymongo import PyMongo

mongo = PyMongo()

def initDB(app):
    mongoUri = app.config["DATABASE_URI"]
    mongo.init_app(app, uri=mongoUri)
    return mongo