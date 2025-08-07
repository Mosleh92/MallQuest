"""Socket.IO event handlers for MallQuest."""

from flask_socketio import emit

from . import socketio


@socketio.on("connect")
def handle_connect():
    """Handle a new WebSocket connection."""
    emit("connected", {"message": "connected"})


@socketio.on("disconnect")
def handle_disconnect():
    """Handle a WebSocket disconnection."""
    print("Client disconnected")


@socketio.on("location_update")
def handle_location_update(data):
    """Receive a location update from the client."""
    emit("location_ack", data)


@socketio.on("join_battle")
def handle_join_battle(data):
    """Handle a request to join a battle."""
    emit("battle_joined", data)


@socketio.on("collect_coin")
def handle_collect_coin(data):
    """Handle coin collection events."""
    emit("coin_collected", data)

