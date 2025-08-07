"""Minimal web interface with secure configuration checks."""
from flask import Flask, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
import os
from datetime import datetime

from database import MallDatabase
from app.services import segmentation_service
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
segmentation_service.schedule_daily_update(mall_db)
app.register_blueprint(wager_bp, url_prefix='/wager')

# Seed demo user for testing and development
if not mall_db.get_user('demo'):
    mall_db.add_user({
        'user_id': 'demo',
        'name': 'Demo User',
        'email': 'demo@example.com',
        'password_hash': generate_password_hash('demo123'),
        'date_of_birth': datetime(2000, 1, 1)
    })

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

    dob = user_record.get('date_of_birth')
    if dob:
        if isinstance(dob, str):
            dob_dt = datetime.fromisoformat(dob)
        else:
            dob_dt = dob
        today = datetime.utcnow().date()
        age = today.year - dob_dt.year - ((today.month, today.day) < (dob_dt.month, dob_dt.day))
        if age < 17:
            return jsonify({'error': translator.gettext('age_restricted', lang)}), 403

    session['user_id'] = user_id
    return jsonify({'success': True, 'user_id': user_id})


 codex/add-last_purchase_at-to-user-model
@app.route('/admin/inactive-users')
def inactive_users():
    """Return lists of dormant and lost users."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    user = mall_db.get_user(user_id)
    if not user or user.get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    segment = request.args.get('segment')
    if segment:
        users = segmentation_service.get_users_by_segment(segment)
        return jsonify({segment: users})
    return jsonify(
        {
            'dormant': segmentation_service.get_users_by_segment('dormant'),
            'lost': segmentation_service.get_users_by_segment('lost'),
        }
    )
=======
@app.route('/api/purchases', methods=['GET'])
def purchase_stats():
    """Return aggregated purchase statistics."""
    if 'user_id' not in session:
        return jsonify({'error': 'authentication required'}), 401
    range_param = request.args.get('range', 'daily')
    stats = mall_db.get_purchase_stats(range_param)
    return jsonify({'range': range_param, 'stats': stats})
 main


if __name__ == '__main__':
    app.run(debug=True)
