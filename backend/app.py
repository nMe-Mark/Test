from flask import Flask
from config import Config
from extensions import jwt, mongo_client
from routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Настройване на MongoDB клиента
    mongo_client_address = app.config['MONGO_URI']
    mongo_client.host = mongo_client_address

    # JWT
    jwt.init_app(app)

    # Регистриране на маршрути
    app.register_blueprint(auth_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
