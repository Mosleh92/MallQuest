"""Quest-related endpoints."""

from flask_restx import Namespace, Resource


ns = Namespace("quests", description="Quest operations")


@ns.route("/")
class ListQuests(Resource):
    """List available quests."""

    def get(self):
        return {"quests": []}

