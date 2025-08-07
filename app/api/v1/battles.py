"""Battle management endpoints."""

from flask_restx import Namespace, Resource


ns = Namespace("battles", description="Battle operations")


@ns.route("/join")
class JoinBattle(Resource):
    """Join a battle."""

    def post(self):
        return {"status": "not implemented"}, 501

