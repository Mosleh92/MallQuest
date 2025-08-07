"""Quest-related endpoints."""

from flask_restx import Namespace, Resource

from ...core import game_state


ns = Namespace("quests", description="Quest operations")


@ns.route("/")
class ListQuests(Resource):
    """List available quests."""

    def get(self):
        return {"quests": game_state.list_quests()}

