"""CRM and analytics endpoints."""

from flask_restx import Namespace, Resource

from ...core import game_state


ns = Namespace("crm", description="CRM operations")


@ns.route("/campaigns")
class Campaigns(Resource):
    """Return configured marketing campaigns."""

    def get(self):
        return {"campaigns": game_state.campaign_list()}


@ns.route("/analytics")
class Analytics(Resource):
    """Return simple analytics data."""

    def get(self):
        return {"stats": game_state.analytics_summary()}

