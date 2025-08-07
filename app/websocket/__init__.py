"""WebSocket handlers for real-time game events."""

from flask_socketio import SocketIO


socketio = SocketIO(cors_allowed_origins="*")


def init_app(app):
    """Initialize SocketIO with the given Flask app and register events."""
    socketio.init_app(app, cors_allowed_origins="*")
    # Importing events registers the handlers with SocketIO
    from . import events  # noqa: F401

