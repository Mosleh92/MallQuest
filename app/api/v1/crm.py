"""CRM and analytics endpoints."""

from flask_restx import Namespace, Resource


ns = Namespace("crm", description="CRM operations")


@ns.route("/campaigns")
class Campaigns(Resource):
    """Manage marketing campaigns."""

    def get(self):
        return {"campaigns": []}


@ns.route("/analytics")
class Analytics(Resource):
    """Return simple analytics data."""

    def get(self):
        return {"stats": {}}

