 codex/refactor-password-validation-in-web_interface
from flask import Flask, request, jsonify, session
from werkzeug.security import check_password_hash

from database import MallDatabase
from i18n import translator, get_locale

app = Flask(__name__)
app.secret_key = 'dev-secret'

# Initialize database
=======
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, g, abort
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel
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
from discounts_service import DiscountsService
from wheel_of_fortune import WheelOfFortune
from werkzeug.security import check_password_hash
from database import MallDatabase
from voucher_system import voucher_system  # noqa: F401
from leaderboard_service import LeaderboardService
from milestone_rewards import MilestoneRewards
from i18n import translator, get_locale
from config import BaseConfig, TenantManager
from datetime import datetime
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")

# Localization configuration
app.config["BABEL_DEFAULT_LOCALE"] = "en"
app.config["BABEL_SUPPORTED_LOCALES"] = ["en", "ar"]
app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations"
BaseConfig.load_tenants()

babel = Babel(app, locale_selector=lambda: session.get("language", "en"))
csrf = CSRFProtect(app)

# Core systems
mall_system = MallGamificationSystem()
coin_duel_manager = CoinDuelManager(mall_system)
security_manager = SecurityManager()
secure_db = SecureDatabase()
input_validator = InputValidator()
rate_limiter = RateLimiter()
performance_manager = PerformanceManager()
discounts_service = DiscountsService()
leaderboard_service = LeaderboardService(mall_system)
 main
mall_db = MallDatabase()
milestone_rewards = MilestoneRewards()

 codex/refactor-password-validation-in-web_interface
@app.route('/login', methods=['POST'])
def login():
    """Authenticate user using hashed password stored in the database."""
    lang = get_locale()
    data = request.get_json() or request.form
    user_id = data.get('user_id')
    password = data.get('password')

    if not user_id or not password:
        return jsonify({'error': translator.gettext('user_password_required', lang)}), 400

    user_record = mall_db.get_user(user_id)
    if (
        not user_record
        or not user_record.get('password_hash')
        or not check_password_hash(user_record['password_hash'], password)
    ):
        # Return localized invalid credentials message
        return jsonify({'error': translator.gettext('invalid_credentials', lang)}), 401

    # Successful login
    session['user_id'] = user_id
    return jsonify({'success': True, 'user_id': user_id})

if __name__ == '__main__':
    app.run(debug=True)
=======
# Initialize Wheel of Fortune with default prizes
wheel = WheelOfFortune(
    mall_system,
    prizes={
        "small_coins": {"probability": 0.6, "inventory": 100, "reward": {"coins": 5}},
        "medium_coins": {"probability": 0.3, "inventory": 50, "reward": {"coins": 20}},
        "jackpot": {"probability": 0.1, "inventory": 10, "reward": {"coins": 100}},
    },
)

# Tenant-specific system caches
tenant_systems = {}
tenant_dbs = {}

@app.before_request
def load_tenant():
    """Middleware to load tenant configuration based on request domain."""
    host = request.host.split(":")[0]
    tenant = TenantManager.get_tenant(host)
    if tenant:
        g.tenant = tenant
        g.branding = {
            "name": tenant.get("name", BaseConfig.MALL_NAME),
            "theme": tenant.get("theme", "default"),
            "logo": tenant.get("logo", ""),
        }
    else:
        g.branding = {"name": BaseConfig.MALL_NAME, "theme": "default", "logo": ""}

    global mall_system, secure_db
    if tenant:
        if host not in tenant_systems:
            tenant_systems[host] = MallGamificationSystem()
            tenant_dbs[host] = SecureDatabase(tenant.get("schema"))
        mall_system = tenant_systems[host]
        secure_db = tenant_dbs[host]

@app.context_processor
def inject_translations():
    lang = session.get("lang", translator.default_locale)
    return {"t": lambda key: translator.gettext(key, lang)}

@app.context_processor
def inject_branding():
    return {"branding": getattr(g, "branding", {})}

@app.route("/")
def index():
    """Landing page."""
    return render_template("index.html")

@app.route("/locales/<lang>.json")
def serve_locale(lang):
    """Return localization dictionary for client-side use"""
    data = translator.translations.get(lang)
    if not data:
        lang = translator.default_locale
        data = translator.translations.get(lang, {})
    session["lang"] = lang
    return jsonify(data)

@app.route("/login", methods=["GET", "POST"])
@rate_limiter.limit(max_requests=5, window_seconds=300)
def login():
    """Login page with MFA support"""
    start_time = datetime.now()
    lang = get_locale()

    if request.method == "GET":
        response_time = (datetime.now() - start_time).total_seconds()
        record_performance_event("login_page_load", response_time)
        return render_template("login.html")

    data = request.get_json() if request.is_json else request.form
    user_id = data.get("user_id")
    password = data.get("password")
    otp = data.get("otp")

    if not user_id or not password:
        return jsonify({"error": translator.gettext("user_password_required", lang)}), 400

    # Fetch user credentials from database
    user_record = mall_db.get_user(user_id)
    if not user_record:
        return jsonify({"error": translator.gettext("user_not_found", lang)}), 404

    # Verify password against stored hash
    if not user_record.get("password_hash") or not check_password_hash(user_record["password_hash"], password):
        return jsonify({"error": translator.gettext("invalid_credentials", lang)}), 401

    # Ensure user exists in mall system
    user = mall_system.get_user(user_id)
    if not user:
        user = mall_system.create_user(user_id, lang)

    # Check if MFA is enabled for this user
    mfa_settings = secure_db.get_mfa_settings(user_id)
    if mfa_settings and mfa_settings.get("mfa_enabled"):
        if not otp:
            return jsonify({"error": translator.gettext("otp_required", lang), "mfa_required": True}), 401
        if not security_manager.verify_otp(mfa_settings["mfa_secret"], otp):
            secure_db.log_mfa_attempt(user_id, "otp", False)
            return jsonify({"error": translator.gettext("otp_invalid", lang), "mfa_required": True}), 403
        secure_db.log_mfa_attempt(user_id, "otp", True)

    # Login successful
    user.login()
    session["user_id"] = user_id
    session["authenticated"] = True

    secure_db.log_security_event(user_id, "login_success", f"Login from {request.remote_addr}")
    log_security_event("login_success", {"user_id": user_id, "ip": request.remote_addr})

    response_time = (datetime.now() - start_time).total_seconds()
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
    lang = get_locale()

    if request.method == "GET":
        mfa_secret = security_manager.generate_mfa_secret()
        qr_code_url = security_manager.generate_mfa_qr_code(user_id, mfa_secret)
        backup_codes = security_manager.generate_backup_codes()
        session["mfa_setup"] = {"secret": mfa_secret, "backup_codes": backup_codes}
        return render_template(
            "mfa_setup.html",
            qr_code_url=qr_code_url,
            backup_codes=backup_codes,
            user_id=user_id,
        )

    data = request.get_json() if request.is_json else request.form
    otp = data.get("otp")

    if not otp:
        return jsonify({"error": translator.gettext("otp_required", lang)}), 400

    mfa_setup_data = session.get("mfa_setup")
    if not mfa_setup_data:
        return jsonify({"error": translator.gettext("mfa_setup_session_expired", lang)}), 400

    if not security_manager.verify_otp(mfa_setup_data["secret"], otp):
        return jsonify({"error": translator.gettext("otp_invalid", lang)}), 403

    if secure_db.save_mfa_settings(user_id, mfa_setup_data["secret"], mfa_setup_data["backup_codes"]):
        secure_db.enable_mfa(user_id)
        session.pop("mfa_setup", None)
        secure_db.log_security_event(user_id, "mfa_enabled", "MFA setup completed")
        return jsonify({"success": True, "message": translator.gettext("mfa_enabled_success", lang)})
    else:
        return jsonify({"error": translator.gettext("failed_save_mfa", lang)}), 500

@app.route("/mfa/verify", methods=["POST"])
def mfa_verify():
    """Verify MFA code"""
    data = request.get_json() if request.is_json else request.form
    lang = get_locale()
    user_id = data.get("user_id")
    otp = data.get("otp")
    backup_code = data.get("backup_code")

    if not user_id:
        return jsonify({"error": translator.gettext("user_id_required", lang)}), 400

    mfa_settings = secure_db.get_mfa_settings(user_id)
    if not mfa_settings or not mfa_settings.get("mfa_enabled"):
        return jsonify({"error": translator.gettext("mfa_not_enabled", lang)}), 400

    if otp and security_manager.verify_otp(mfa_settings["mfa_secret"], otp):
        secure_db.log_mfa_attempt(user_id, "otp", True)
        return jsonify({"success": True})

    if backup_code and security_manager.verify_backup_code(mfa_settings["backup_codes"], backup_code):
        secure_db.log_mfa_attempt(user_id, "backup", True)
        secure_db.invalidate_backup_code(user_id, backup_code)
        return jsonify({"success": True})

    secure_db.log_mfa_attempt(user_id, "otp" if otp else "backup", False)
    return jsonify({"error": translator.gettext("otp_invalid", lang)}), 403

@app.route("/player/<user_id>")
def player_dashboard(user_id):
    """Player dashboard"""
    if "user_id" not in session or session["user_id"] != user_id:
        return "Unauthorized", 401

    user = mall_system.get_user(user_id)
    if not user:
        return "User not found", 404

    dashboard_data = mall_system.get_player_dashboard(user_id)
    available_milestones = milestone_rewards.get_available_milestones(user_id)

    return render_template(
        "player_dashboard.html",
        user=user,
        dashboard=dashboard_data,
        duels=coin_duel_manager.get_user_duels(user_id),
        milestones=available_milestones,
    )

 main
