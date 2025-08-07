"""Authentication endpoints."""

from flask_restx import Namespace, Resource


ns = Namespace("auth", description="Authentication operations")


@ns.route("/login")
class Login(Resource):
    """Simple login placeholder."""

    def post(self):
        return {"message": "login not implemented"}, 501

