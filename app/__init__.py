import os

from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "dev-insecure-key")

    from app.routes import bp
    app.register_blueprint(bp)

    return app