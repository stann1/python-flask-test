from flask_pymongo import PyMongo

MONGO_URI = 'mongodb://localhost:27018/todos'

def initDB(app):
    app.config["MONGO_URI"] = MONGO_URI
    mongo = PyMongo(app)
    return mongo