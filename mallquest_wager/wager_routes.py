from flask import Blueprint, request, jsonify

try:  # pragma: no cover - fallback if wager_system is missing
    from . import wager_system
except Exception:  # pragma: no cover
    class _FallbackWagerSystem:
        """Fallback implementations if wager_system is unavailable."""

        @staticmethod
        def create_wager(*args, **kwargs):
            return {"success": False, "error": "wager system not available"}

        @staticmethod
        def join_wager(*args, **kwargs):
            return {"success": False, "error": "wager system not available"}

        @staticmethod
        def redeem_wager(*args, **kwargs):
            return {"success": False, "error": "wager system not available"}

    wager_system = _FallbackWagerSystem()


wager_bp = Blueprint("wager", __name__)


@wager_bp.route("/create", methods=["POST"])
def create_wager_route():
    """Create a new wager."""
    data = request.get_json() or {}
    creator_id = data.get("creator_id")
    amount = data.get("amount")
    if not creator_id or amount is None:
        return jsonify({"error": "creator_id and amount required"}), 400
    result = wager_system.create_wager(creator_id, amount)
    return jsonify(result)


@wager_bp.route("/join", methods=["POST"])
def join_wager_route():
    """Join an existing wager."""
    data = request.get_json() or {}
    wager_id = data.get("wager_id")
    user_id = data.get("user_id")
    if not wager_id or not user_id:
        return jsonify({"error": "wager_id and user_id required"}), 400
    result = wager_system.join_wager(wager_id, user_id)
    return jsonify(result)


@wager_bp.route("/redeem", methods=["POST"])
def redeem_wager_route():
    """Redeem a completed wager."""
    data = request.get_json() or {}
    wager_id = data.get("wager_id")
    user_id = data.get("user_id")
    if not wager_id or not user_id:
        return jsonify({"error": "wager_id and user_id required"}), 400
    result = wager_system.redeem_wager(wager_id, user_id)
    return jsonify(result)
