# #  from flask import Flask
# #  from config import Config
# #  from extensions import jwt, mongo_client
# #  from routes import auth_bp

# # def create_app():
# #     app = Flask(__name__)
# #     app.config.from_object(Config)

# #     # Настройване на MongoDB клиента
# #     mongo_client_address = app.config['MONGO_URI']
# #     mongo_client.host = mongo_client_address

# #     # JWT
# #     jwt.init_app(app)

# #     # Регистриране на маршрути
# #     app.register_blueprint(auth_bp)

# #     return app

# # if __name__ == '__main__':
# #     app = create_app()
# #     app.run(host="0.0.0.0", port=5000, debug=True)


# from flask import Flask, jsonify, send_from_directory
# from flask_cors import CORS
# from config import Config
# from extensions import jwt, mongo_client
# from routes import auth_bp
# import os

# def create_app():
#     app = Flask(__name__, static_folder="../frontend_dist", static_url_path="/")
#     app.config.from_object(Config)

#     # Настройване на MongoDB клиента
#     mongo_client.host = app.config['MONGO_URI']

#     # Инициализиране на JWT
#     jwt.init_app(app)

#     # Enable CORS за всички маршрути
#     CORS(app)

#     # Регистриране на Blueprint
#     app.register_blueprint(auth_bp, url_prefix="/api/auth")

#     # Рут за статични файлове от React (ако ползваш build)
#     @app.route("/", defaults={"path": ""})
#     @app.route("/<path:path>")
#     def serve_react(path):
#         if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
#             return send_from_directory(app.static_folder, path)
#         return send_from_directory(app.static_folder, "index.html")

#     # API статус рут
#     @app.route("/api")
#     def index():
#         return jsonify({
#             "message": "Добре дошли в API-то за Task Management",
#             "endpoints": ["/api/auth/register", "/api/auth/login", "/api/auth/tasks"]
#         })

#     return app

# # За стартиране през docker
# app = create_app()

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)






# from flask import Flask
# from config import Config
# from extensions import get_db, jwt, init_mongo
# from routes import auth_bp
# from flask_jwt_extended import JWTManager
# from flask_cors import CORS


from flask import Flask, jsonify
from config import Config
from extensions import jwt
from routes import auth_bp
from flask_cors import CORS
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # JWT
    jwt.init_app(app)

    # Mongo клиент
    app.mongo_client = MongoClient(app.config["MONGO_URI"])
    app.db = app.mongo_client.get_database()

    # Регистриране на blueprint-а с коректен префикс
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # CORS
    CORS(app)

    @app.route("/api")
    def api_index():
        return jsonify({
            "message": "API-то е активно",
            "endpoints": ["/api/auth/register", "/api/auth/login", "/api/auth/tasks"]
        })

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
