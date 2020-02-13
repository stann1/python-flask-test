from flask_pymongo import PyMongo

def initDB(app):
    mongoUri = app.config["DATABASE_URI"]
    mongo = PyMongo(app, uri=mongoUri)
    return mongo