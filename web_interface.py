from flask import Flask, request, jsonify, session
from werkzeug.security import check_password_hash

from database import MallDatabase
from i18n import translator, get_locale

app = Flask(__name__)
app.secret_key = 'dev-secret'

# Initialize database
mall_db = MallDatabase()

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
