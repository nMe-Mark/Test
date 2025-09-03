
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

    # Регистриране на blueprint-а
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
