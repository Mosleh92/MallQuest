
"""Socket.IO event handlers implementing basic game logic."""

from flask_socketio import emit

from . import socketio
from ..core import game_state


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
    """Receive a location update from the client and reply with nearby coins."""
    player_id = data.get("player_id", "anon")
    x = float(data.get("x", 0))
    y = float(data.get("y", 0))
    game_state.update_location(player_id, x, y)
    coins = game_state.get_nearby_coins(x, y)
    emit("location_ack", {"nearby_coins": coins})


@socketio.on("join_battle")
def handle_join_battle(data):
    """Handle a request to join a battle."""
    player_id = data.get("player_id", "anon")
    battle = game_state.join_battle(player_id)
    emit(
        "battle_update",
        {"battle_id": battle.battle_id, "players": battle.players},
        broadcast=True,
    )


@socketio.on("collect_coin")
def handle_collect_coin(data):
    """Handle coin collection events."""
    player_id = data.get("player_id", "anon")
    coin_id = int(data.get("coin_id", 0))
    success = game_state.collect_coin(player_id, coin_id)
    if success:
        total = game_state.players[player_id].coins
        emit("coin_collected", {"coin_id": coin_id, "total_coins": total})
    else:
        emit("coin_collected", {"error": "coin not found"})

