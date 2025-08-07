"""Authentication endpoints."""

from flask import request
from flask_jwt_extended import create_access_token
from flask_restx import Namespace, Resource


ns = Namespace("auth", description="Authentication operations")

# Simple in-memory user store for demonstration purposes
_USERS = {"admin": "password"}


@ns.route("/login")
class Login(Resource):
    """Authenticate a user and return a JWT access token."""

    def post(self):
        data = request.get_json() or {}
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"message": "Missing username or password"}, 400

        if _USERS.get(username) != password:
            return {"message": "Invalid credentials"}, 401

        access_token = create_access_token(identity=username)
        return {"access_token": access_token}, 200

