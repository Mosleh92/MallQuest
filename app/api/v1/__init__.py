"""Version 1 of the MallQuest REST API."""

from flask import Blueprint
from flask_restx import Api


api_bp = Blueprint("api_v1", __name__)
api = Api(api_bp, doc="/docs", title="MallQuest API", version="1.0")


# Import namespaces to register them with the API
from . import auth, coins, battles, quests, crm  # noqa: F401

api.add_namespace(auth.ns, path="/auth")
api.add_namespace(coins.ns, path="/coins")
api.add_namespace(battles.ns, path="/battles")
api.add_namespace(quests.ns, path="/quests")
api.add_namespace(crm.ns, path="/crm")

