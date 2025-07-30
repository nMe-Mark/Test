from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from flask import current_app

jwt = JWTManager()
mongo_client = MongoClient()  # Will be configured later in app.py

def get_db():
    return mongo_client[current_app.config['MONGO_URI'].rsplit('/', 1)[-1]]
