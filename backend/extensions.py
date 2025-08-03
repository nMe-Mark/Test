# from flask_jwt_extended import JWTManager
# from pymongo import MongoClient
# from flask import current_app

# jwt = JWTManager()
# mongo_client = MongoClient()  # Will be configured later in app.py

# def get_db():
#     return mongo_client[current_app.config['MONGO_URI'].rsplit('/', 1)[-1]]


# from flask_jwt_extended import JWTManager
# from pymongo import MongoClient
# from flask import current_app

# jwt = JWTManager()
# mongo_client = MongoClient()  # Конфигурира се в app.py

# # getter за достъп до колекции
# def get_db():
#     db_name = current_app.config['MONGO_URI'].rsplit('/', 1)[-1]
#     return mongo_client[db_name]



from flask import current_app
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def get_db():
    return current_app.db

# Премахваме глобалната инстанция mongo_client тук

