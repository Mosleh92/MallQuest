"""Battle management endpoints."""

from flask import request
from flask_restx import Namespace, Resource

from ...core import game_state


ns = Namespace("battles", description="Battle operations")


@ns.route("/join")
class JoinBattle(Resource):
    """Join the default battle and return current participants."""

    def post(self):
        data = request.get_json() or {}
        player_id = data.get("player_id")
        if not player_id:
            return {"error": "player_id required"}, 400

        battle = game_state.join_battle(player_id)
        return {"battle_id": battle.battle_id, "players": battle.players}

