"""Minimal web interface with secure configuration checks."""
from flask import Flask, request, jsonify, session
from werkzeug.security import check_password_hash
import os

from database import MallDatabase
from i18n import translator, get_locale
from mallquest_wager.wager_routes import wager_bp

REQUIRED_ENV = ["SECRET_KEY", "DATABASE_URL", "JWT_SECRET_KEY"]
for var in REQUIRED_ENV:
    if not os.getenv(var):
        raise RuntimeError(f"{var} is missing")

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]

try:
    from flask_jwt_extended import JWTManager
except Exception:  # pragma: no cover - optional dependency
    JWTManager = None

if JWTManager:
    jwt = JWTManager(app)

mall_db = MallDatabase()
app.register_blueprint(wager_bp, url_prefix='/wager')

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
        return jsonify({'error': translator.gettext('invalid_credentials', lang)}), 401

    session['user_id'] = user_id
    return jsonify({'success': True, 'user_id': user_id})


if __name__ == '__main__':
    app.run(debug=True)
