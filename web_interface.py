# Web Interface for Mall Gamification AI Control Panel
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, abort
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel, gettext as _
from mall_gamification_system import MallGamificationSystem, User
from coin_duel import CoinDuelManager
from security_module import (
    SecurityManager,
    SecureDatabase,
    InputValidator,
    RateLimiter,
    log_security_event,
)
from performance_module import PerformanceManager, record_performance_event
from voucher_system import voucher_system  # noqa: F401
from leaderboard_service import LeaderboardService
from milestone_rewards import MilestoneRewards
from i18n import translator
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

app.config["BABEL_DEFAULT_LOCALE"] = "en"
app.config["BABEL_SUPPORTED_LOCALES"] = ["en", "ar"]
app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations"


def get_locale():
    return session.get("language", "en")


babel = Babel(app, locale_selector=get_locale)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize the mall system and security components
mall_system = MallGamificationSystem()
security_manager = SecurityManager()
secure_db = SecureDatabase()
input_validator = InputValidator()
rate_limiter = RateLimiter()
performance_manager = PerformanceManager()
leaderboard_service = LeaderboardService(mall_system)
coin_duel_manager = CoinDuelManager(mall_system)
milestone_rewards = MilestoneRewards()


@app.context_processor
def inject_translations():
    lang = get_locale()
    return {"t": lambda key: translator.gettext(key, lang)}


@app.route("/locales/<lang>.json")
def serve_locale(lang):
    """Return localization dictionary for client-side use"""
    data = translator.translations.get(lang)
    if not data:
        lang = translator.default_locale
        data = translator.translations.get(lang, {})
    session["lang"] = lang
    return jsonify(data)


# -----------------------------
# AUTHENTICATION ROUTES
# -----------------------------


@app.route("/login", methods=["GET", "POST"])
@rate_limiter.limit(max_requests=5, window_seconds=300)
def login():
    """Login page with MFA support"""
    start_time = datetime.now()

    if request.method == "GET":
        response_time = (datetime.now() - start_time).total_seconds()
        record_performance_event("login_page_load", response_time)
        return render_template("login.html")

    data = request.get_json() if request.is_json else request.form
    user_id = data.get("user_id")
    password = data.get("password")
    otp = data.get("otp")

    response_time = (datetime.now() - start_time).total_seconds()

    if not user_id or not password:
        return jsonify({"error": _("user_id_password_required")}), 400

    user = mall_system.get_user(user_id)
    if not user:
        return jsonify({"error": _("user_not_found")}), 404

    if password != "demo123":  # Replace with proper password verification
        return jsonify({"error": _("invalid_credentials")}), 401

    mfa_settings = secure_db.get_mfa_settings(user_id)

    if mfa_settings and mfa_settings["mfa_enabled"]:
        if not otp:
            return jsonify({"error": _("otp_required"), "mfa_required": True}), 401

        if not security_manager.verify_otp(mfa_settings["mfa_secret"], otp):
            secure_db.log_mfa_attempt(user_id, "otp", False)
            return jsonify({"error": _("invalid_otp"), "mfa_required": True}), 403

        secure_db.log_mfa_attempt(user_id, "otp", True)

    user.login()
    session["user_id"] = user_id
    session["authenticated"] = True

    secure_db.log_security_event(user_id, "login_success", f"Login from {request.remote_addr}")
    log_security_event("login_success", {"user_id": user_id, "ip": request.remote_addr})

    record_performance_event("login_success", response_time)

    return jsonify(
        {
            "success": True,
            "user_id": user_id,
            "redirect_url": url_for("player_dashboard", user_id=user_id),
        }
    )


@app.route("/logout")
def logout():
    """Logout user"""
    if "user_id" in session:
        user_id = session["user_id"]
        secure_db.log_security_event(user_id, "logout", f"Logout from {request.remote_addr}")

    session.clear()
    return redirect(url_for("index"))


@app.route("/mfa/setup", methods=["GET", "POST"])
def mfa_setup():
    """Setup MFA for user"""
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    if request.method == "GET":
        mfa_secret = security_manager.generate_mfa_secret()
        qr_code_url = security_manager.generate_mfa_qr_code(user_id, mfa_secret)
        backup_codes = security_manager.generate_backup_codes()

        session["mfa_setup"] = {
            "secret": mfa_secret,
            "backup_codes": backup_codes,
        }

        return render_template(
            "mfa_setup.html",
            qr_code_url=qr_code_url,
            backup_codes=backup_codes,
            user_id=user_id,
        )

    data = request.get_json() if request.is_json else request.form
    otp = data.get("otp")

    if not otp:
        return jsonify({"error": _("otp_required")}), 400

    mfa_setup_data = session.get("mfa_setup")
    if not mfa_setup_data:
        return jsonify({"error": _("mfa_setup_session_expired")}), 400

    if not security_manager.verify_otp(mfa_setup_data["secret"], otp):
        return jsonify({"error": _("invalid_otp")}), 403

    if secure_db.save_mfa_settings(
        user_id, mfa_setup_data["secret"], mfa_setup_data["backup_codes"]
    ):
        secure_db.enable_mfa(user_id)
        session.pop("mfa_setup", None)
        secure_db.log_security_event(user_id, "mfa_enabled", "MFA setup completed")
        return jsonify({"success": True, "message": _("mfa_enabled_success")})
    else:
        return jsonify({"error": _("failed_to_save_mfa_settings")}), 500


@app.route("/mfa/verify", methods=["POST"])
def mfa_verify():
    """Verify MFA code"""
    data = request.get_json() if request.is_json else request.form
    user_id = data.get("user_id")
    otp = data.get("otp")
    backup_code = data.get("backup_code")

    if not user_id:
        return jsonify({"error": _("user_id_required")}), 400

    mfa_settings = secure_db.get_mfa_settings(user_id)
    if not mfa_settings or not mfa_settings["mfa_enabled"]:
        return jsonify({"error": _("mfa_not_enabled")}), 400

    success = False
    attempt_type = None

    if otp:
        success = security_manager.verify_otp(mfa_settings["mfa_secret"], otp)
        attempt_type = "otp"
    elif backup_code:
        success = security_manager.verify_backup_code(
            mfa_settings["backup_codes"], backup_code
        )
        if success:
            secure_db.update_backup_codes(user_id, mfa_settings["backup_codes"])
        attempt_type = "backup"
    else:
        return jsonify({"error": _("otp_or_backup_required")}), 400

    secure_db.log_mfa_attempt(user_id, attempt_type, success)

    if success:
        return jsonify({"success": True, "message": _("mfa_verification_success")})
    else:
        return jsonify({"error": _("invalid_otp")}), 403


@app.route("/mfa/disable", methods=["POST"])
def mfa_disable():
    """Disable MFA for user"""
    if "user_id" not in session:
        return jsonify({"error": _("authentication_required")}), 401

    user_id = session["user_id"]
    data = request.get_json() if request.is_json else request.form
    otp = data.get("otp")

    mfa_settings = secure_db.get_mfa_settings(user_id)
    if not mfa_settings or not mfa_settings["mfa_enabled"]:
        return jsonify({"error": _("mfa_not_enabled")}), 400

    if not security_manager.verify_otp(mfa_settings["mfa_secret"], otp):
        return jsonify({"error": _("invalid_otp")}), 403

    if secure_db.disable_mfa(user_id):
        secure_db.log_security_event(user_id, "mfa_disabled", "MFA disabled by user")
        return jsonify({"success": True, "message": _("mfa_disabled_success")})
    else:
        return jsonify({"error": _("failed_to_disable_mfa")}), 500


# -----------------------------
# ROUTES FOR DIFFERENT DASHBOARDS
# -----------------------------


@app.route("/")
def index():
    """Main landing page with language selection"""
    return render_template("index.html")


@app.route("/player/<user_id>")
def player_dashboard(user_id):
    """Player Dashboard - Main user interface"""
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))

    user = mall_system.get_user(user_id)
    if not user:
        user = mall_system.create_user(user_id, "en")

    user.login()
    dashboard_data = mall_system.get_user_dashboard(user_id)

    milestone_rewards.update_progress(user_id, user.xp)
    available_milestones = milestone_rewards.get_available_milestones(user_id)

    return render_template(
        "player_dashboard.html",
        user=user,
        dashboard=dashboard_data,
        duels=coin_duel_manager.get_user_duels(user_id),
        milestones=available_milestones,
    )


if __name__ == "__main__":
    app.run(debug=True)

