"""Coin-related endpoints."""

from flask import request
from flask_restx import Namespace, Resource

from ...core import game_state


ns = Namespace("coins", description="Coin operations")


@ns.route("/nearby")
class CoinsNearby(Resource):
    """Return coins near a given position."""

    def get(self):
        try:
            x = float(request.args.get("x", 0))
            y = float(request.args.get("y", 0))
        except ValueError:
            return {"error": "Invalid coordinates"}, 400

        coins = game_state.get_nearby_coins(x, y)
        return {"coins": coins}


@ns.route("/collect")
class CollectCoin(Resource):
    """Collect a coin by ID."""

    def post(self):
        data = request.get_json() or {}
        player_id = data.get("player_id")
        coin_id = data.get("coin_id")
        if not player_id or coin_id is None:
            return {"error": "player_id and coin_id required"}, 400

        success = game_state.collect_coin(player_id, int(coin_id))
        if not success:
            return {"error": "coin not found"}, 404

        player = game_state.players[player_id]
        return {"status": "collected", "total_coins": player.coins}

