from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from mall_gamification_system import MallGamificationSystem
from coin_duel import CoinDuelManager
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret')

# Core systems
mall_system = MallGamificationSystem()
coin_duel_manager = CoinDuelManager(mall_system)


@app.route('/')
def index():
    """Landing page."""
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    """Simple login to establish a session."""
    data = request.get_json() or request.form
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
    mall_system.create_user(user_id, 'en')
    session['user_id'] = user_id
    return redirect(url_for('player_dashboard', user_id=user_id))


@app.route('/player/<user_id>')
def player_dashboard(user_id):
    """Player dashboard showing active duels."""
    if session.get('user_id') != user_id:
        return redirect(url_for('index')), 401
    user = mall_system.get_user(user_id)
    if not user:
        user = mall_system.create_user(user_id, 'en')
    dashboard_data = mall_system.get_user_dashboard(user_id)
    return render_template(
        'player_dashboard.html',
        user=user,
        dashboard=dashboard_data,
        duels=coin_duel_manager.get_user_duels(user_id)
    )


@app.route('/duel/start', methods=['POST'])
def duel_start():
    """Start a coin duel with another player."""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    data = request.get_json() or request.form
    opponent_id = data.get('opponent_id')
    if not opponent_id:
        return jsonify({'error': 'Opponent ID required'}), 400
    duel_id = coin_duel_manager.start_duel(session['user_id'], opponent_id)
    return jsonify({'duel_id': duel_id})


@app.route('/duel/update', methods=['POST'])
def duel_update():
    """Update score for current user in a duel."""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    data = request.get_json() or request.form
    duel_id = data.get('duel_id')
    score = data.get('score')
    if duel_id is None or score is None:
        return jsonify({'error': 'Duel ID and score required'}), 400
    try:
        score = int(score)
    except ValueError:
        return jsonify({'error': 'Score must be integer'}), 400
    success = coin_duel_manager.update_score(duel_id, session['user_id'], score)
    if not success:
        return jsonify({'error': 'Invalid duel'}), 404
    return jsonify({'success': True})


@app.route('/duel/finish', methods=['POST'])
def duel_finish():
    """Conclude a duel and determine the winner."""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    data = request.get_json() or request.form
    duel_id = data.get('duel_id')
    if not duel_id:
        return jsonify({'error': 'Duel ID required'}), 400
    result = coin_duel_manager.conclude_duel(duel_id)
    if not result:
        return jsonify({'error': 'Invalid duel'}), 404
    return jsonify(result)


@app.route('/duel/status/<duel_id>')
def duel_status(duel_id):
    """Get current status of a duel."""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    duel = coin_duel_manager.get_duel(duel_id)
    if not duel:
        return jsonify({'error': 'Duel not found'}), 404
    return jsonify(duel)


if __name__ == '__main__':
    app.run(debug=True)
