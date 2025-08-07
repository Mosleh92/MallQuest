"""Coin-related endpoints."""

from flask_restx import Namespace, Resource


ns = Namespace("coins", description="Coin operations")


@ns.route("/nearby")
class CoinsNearby(Resource):
    """Return nearby coins."""

    def get(self):
        return {"coins": []}


@ns.route("/collect")
class CollectCoin(Resource):
    """Collect a coin."""

    def post(self):
        return {"status": "not implemented"}, 501

