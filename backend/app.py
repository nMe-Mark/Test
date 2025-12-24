# from flask import Flask, jsonify
# from config import Config
# from extensions import jwt
# from routes import auth_bp
# from flask_cors import CORS
# from pymongo import MongoClient

# app = Flask(__name__)
# app.config.from_object(Config)

# # JWT
# jwt.init_app(app)

# # Mongo
# app.mongo_client = MongoClient(app.config["MONGO_URI"])
# app.db = app.mongo_client.get_database()

# # Регистриране на blueprint-а
# app.register_blueprint(auth_bp, url_prefix="/api/auth")

# # 🔹 CORS за всички /api/*
# CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     # JWT
#     jwt.init_app(app)

#     # Mongo
#     app.mongo_client = MongoClient(app.config["MONGO_URI"])
#     app.db = app.mongo_client.get_database()

#     # CORS – разрешаваме всички /api/* заявки
#     CORS(app, resources={r"/api/*": {"origins": "*"}})

#     # Blueprints
#     app.register_blueprint(auth_bp, url_prefix="/api/auth")

#     @app.route("/api")
#     def api_index():
#         return jsonify({
#             "message": "API-то е активно",
#             "endpoints": [
#                 "/api/auth/register",
#                 "/api/auth/login",
#                 "/api/auth/tasks",
#                 "/api/auth/team/create"
#             ]
#         })

#     return app

# app = create_app()

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)


from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import jwt
from routes import auth_bp
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ КРИТИЧНО
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        supports_credentials=True
    )

    jwt.init_app(app)

    app.mongo_client = MongoClient(app.config["MONGO_URI"])
    app.db = app.mongo_client.get_database()

    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app

app = create_app()


