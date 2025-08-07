"""Minimal web interface with secure configuration checks."""
from flask import Flask, request, jsonify, session, render_template
from werkzeug.security import check_password_hash, generate_password_hash
import os
from datetime import datetime, timedelta
from collections import defaultdict
from functools import wraps

 codex/add-authentication-to-/admin/crm-route
# codex/add-crm-route-and-template
from database import MallDatabase, User, Receipt
# =======
# from database import MallDatabase
from app.services import segmentation_service
# main
=======
from database import MallDatabase, User, Receipt
from app.services import segmentation_service
 main
from i18n import translator, get_locale
from mallquest_wager.wager_routes import wager_bp
from mall_gamification_system import MallGamificationSystem

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
segmentation_service.schedule_daily_update()
app.register_blueprint(wager_bp, url_prefix='/wager')
mall_system = MallGamificationSystem()

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

 codex/add-authentication-to-/admin/crm-route

# codex/add-post-endpoint-for-purchases
=======
 main
@app.route('/api/pos/purchase', methods=['POST'])
def pos_purchase():
    """Record POS purchase and forward to purchase logger."""
    data = request.get_json() or {}
    required = ['store_id', 'user_id', 'amount', 'items', 'timestamp']
    for field in required:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    store_id = data['store_id']
    user_id = data['user_id']
    items = data['items']

    try:
        amount = float(data['amount'])
        timestamp = datetime.fromisoformat(data['timestamp'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid amount or timestamp'}), 400

    if not mall_system.add_purchase_record(store_id, user_id, amount, items, timestamp):
        return jsonify({'error': 'Unable to record purchase'}), 400

    return jsonify({'success': True}), 201
 codex/add-authentication-to-/admin/crm-route
# =======
# codex/add-crm-route-and-template


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function


=======
 main
@app.route('/admin/crm', methods=['GET', 'POST'])
@login_required
def admin_crm():
    """CRM dashboard providing user metrics and campaign tools."""
    user_id = session.get('user_id')
    user = mall_db.get_user(user_id)
    if not user or user.get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    if request.method == 'POST':
        data = request.get_json() or {}
        min_spend = float(data.get('spend') or 0)
        brand = data.get('brand') or ''
        inactivity = int(data.get('inactivity') or 0)
        min_age = int(data.get('age') or 0)
        message = data.get('message') or ''

        sent = 0
        now = datetime.utcnow()
        for maker in mall_db.sessions:
            session_db = maker()
            try:
                users = session_db.query(User).all()
                for user in users:
                    if min_spend and (user.total_spent or 0) < min_spend:
                        continue
                    receipts = session_db.query(Receipt).filter_by(user_id=user.user_id).all()
                    if brand and not any(r.store == brand for r in receipts):
                        continue
                    if inactivity:
                        last_receipt = max((r.created_at for r in receipts), default=None)
                        if not last_receipt or (now - last_receipt).days < inactivity:
                            continue
                    if min_age and user.date_of_birth:
                        age = now.year - user.date_of_birth.year - (
                            (now.month, now.day) < (user.date_of_birth.month, user.date_of_birth.day)
                        )
                        if age < min_age:
                            continue
                    # Placeholder for mass notification
                    print(f"Campaign to {user.user_id}: {message}")
                    sent += 1
            finally:
                session_db.close()

        return jsonify({'status': 'sent', 'count': sent})

    now = datetime.utcnow()
    seven_days_ago = now - timedelta(days=7)
    thirty_days_ago = now - timedelta(days=30)

    active_users = set()
    inactive_users = set()
    top_store_sales = defaultdict(float)
    visit_diffs = []
    entry_counts = defaultdict(int)
    retention_counts = defaultdict(set)

    for maker in mall_db.sessions:
        session_db = maker()
        try:
            receipts_30 = session_db.query(Receipt).filter(Receipt.created_at >= thirty_days_ago).all()
            for r in receipts_30:
                if r.created_at >= seven_days_ago:
                    active_users.add(r.user_id)
                top_store_sales[r.store] += r.amount or 0
                day = r.created_at.date()
                entry_counts[day] += 1
                retention_counts[day].add(r.user_id)

            users = session_db.query(User).all()
            for u in users:
                last_receipt = session_db.query(Receipt).filter_by(user_id=u.user_id).order_by(Receipt.created_at.desc()).first()
                if not last_receipt or last_receipt.created_at < thirty_days_ago:
                    inactive_users.add(u.user_id)

            user_receipts = session_db.query(Receipt).order_by(Receipt.user_id, Receipt.created_at).all()
            last_dates = {}
            for rec in user_receipts:
                if rec.user_id in last_dates:
                    diff = (rec.created_at - last_dates[rec.user_id]).days
                    if diff > 0:
                        visit_diffs.append(diff)
                last_dates[rec.user_id] = rec.created_at
        finally:
            session_db.close()

    avg_visit_interval = sum(visit_diffs) / len(visit_diffs) if visit_diffs else 0
    top_store_sales = dict(sorted(top_store_sales.items(), key=lambda x: x[1], reverse=True)[:5])

    labels = []
    entry_data = []
    retention_data = []
    for i in range(30):
        day = (now - timedelta(days=29 - i)).date()
        labels.append(day.strftime('%m-%d'))
        entry_data.append(entry_counts.get(day, 0))
        retention_data.append(len(retention_counts.get(day, set())))

    return render_template(
        'admin_crm.html',
        active_users=len(active_users),
        inactive_users=len(inactive_users),
        average_visit_interval=round(avg_visit_interval, 2),
        top_store_sales=top_store_sales,
        chart_labels=labels,
        entry_data=entry_data,
        retention_data=retention_data,
    )
 codex/add-authentication-to-/admin/crm-route
# =======
# codex/add-last_purchase_at-to-user-model
=======
 main
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
 codex/add-authentication-to-/admin/crm-route
# =======
=======
 main
@app.route('/api/purchases', methods=['GET'])
def purchase_stats():
    """Return aggregated purchase statistics."""
    if 'user_id' not in session:
        return jsonify({'error': 'authentication required'}), 401
    range_param = request.args.get('range', 'daily')
    stats = mall_db.get_purchase_stats(range_param)
    return jsonify({'range': range_param, 'stats': stats})
 codex/add-authentication-to-/admin/crm-route
# main
# main
# main
=======
 main


if __name__ == '__main__':
    app.run(debug=True)
