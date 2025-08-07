"""Application factory for MallQuest."""

import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .api.v1 import api_bp
from .websocket import init_app as init_socketio, socketio
from celery import Celery


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Basic configuration
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_secret")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt_secret")

    CORS(app)
    JWTManager(app)
    Limiter(key_func=get_remote_address).init_app(app)

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    # Initialize SocketIO
    init_socketio(app)

    return app


def create_celery(app=None):
    """Create a Celery instance tied to the Flask app."""
    app = app or create_app()
    celery = Celery(
        app.import_name,
        broker=app.config.get("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    )
    celery.conf.update(app.config)
    return celery


def run_app():
    """Convenience method to run the app with SocketIO."""
    app = create_app()
    socketio.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))


__all__ = ["create_app", "socketio", "run_app", "create_celery"]

