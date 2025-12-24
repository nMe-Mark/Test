
from flask import current_app
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def get_db():
    return current_app.db