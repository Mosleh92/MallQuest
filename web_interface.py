# Web Interface for Mall Gamification AI Control Panel
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, abort
from flask_wtf.csrf import CSRFProtect
from mall_gamification_system import MallGamificationSystem, User
from security_module import SecurityManager, SecureDatabase, InputValidator, RateLimiter, log_security_event
from performance_module import PerformanceManager, record_performance_event
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'deerfields_mall_secret_key_2024'

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize the mall system and security components
mall_system = MallGamificationSystem()
security_manager = SecurityManager()
secure_db = SecureDatabase()
input_validator = InputValidator()
rate_limiter = RateLimiter()
performance_manager = PerformanceManager()

# -----------------------------
# AUTHENTICATION ROUTES
# -----------------------------

@app.route('/login', methods=['GET', 'POST'])
@rate_limiter.limit(max_requests=5, window_seconds=300)
def login():
    """Login page with MFA support"""
    start_time = datetime.now()
    
    if request.method == 'GET':
        response_time = (datetime.now() - start_time).total_seconds()
        record_performance_event('login_page_load', response_time)
        return render_template('login.html')
    
    # Handle login form submission
    data = request.get_json() if request.is_json else request.form
    user_id = data.get('user_id')
    password = data.get('password')
    otp = data.get('otp')
    
    # Record performance
    response_time = (datetime.now() - start_time).total_seconds()
    
    # Validate input
    if not user_id or not password:
        return jsonify({'error': 'User ID and password are required'}), 400
    
    # Get user
    user = mall_system.get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Verify password (simplified for demo - in production use proper password hashing)
    if password != "demo123":  # Replace with proper password verification
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Check if MFA is enabled for this user
    mfa_settings = secure_db.get_mfa_settings(user_id)
    
    if mfa_settings and mfa_settings['mfa_enabled']:
        # MFA is enabled, verify OTP
        if not otp:
            return jsonify({'error': 'OTP required', 'mfa_required': True}), 401
        
        # Verify OTP
        if not security_manager.verify_otp(mfa_settings['mfa_secret'], otp):
            # Log failed attempt
            secure_db.log_mfa_attempt(user_id, 'otp', False)
            return jsonify({'error': 'کد OTP نامعتبر', 'mfa_required': True}), 403
        
        # Log successful attempt
        secure_db.log_mfa_attempt(user_id, 'otp', True)
    
    # Login successful
    user.login()
    session['user_id'] = user_id
    session['authenticated'] = True
    
    # Log security event
    secure_db.log_security_event(user_id, 'login_success', f'Login from {request.remote_addr}')
    log_security_event('login_success', {'user_id': user_id, 'ip': request.remote_addr})
    
    # Record performance
    record_performance_event('login_success', response_time)
    
    return jsonify({
        'success': True,
        'user_id': user_id,
        'redirect_url': url_for('player_dashboard', user_id=user_id)
    })

@app.route('/logout')
def logout():
    """Logout user"""
    if 'user_id' in session:
        user_id = session['user_id']
        secure_db.log_security_event(user_id, 'logout', f'Logout from {request.remote_addr}')
    
    session.clear()
    return redirect(url_for('index'))

@app.route('/mfa/setup', methods=['GET', 'POST'])
def mfa_setup():
    """Setup MFA for user"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    if request.method == 'GET':
        # Generate new MFA secret
        mfa_secret = security_manager.generate_mfa_secret()
        qr_code_url = security_manager.generate_mfa_qr_code(user_id, mfa_secret)
        backup_codes = security_manager.generate_backup_codes()
        
        # Store temporarily in session
        session['mfa_setup'] = {
            'secret': mfa_secret,
            'backup_codes': backup_codes
        }
        
        return render_template('mfa_setup.html', 
                             qr_code_url=qr_code_url, 
                             backup_codes=backup_codes,
                             user_id=user_id)
    
    # Handle MFA setup confirmation
    data = request.get_json() if request.is_json else request.form
    otp = data.get('otp')
    
    if not otp:
        return jsonify({'error': 'OTP is required'}), 400
    
    mfa_setup_data = session.get('mfa_setup')
    if not mfa_setup_data:
        return jsonify({'error': 'MFA setup session expired'}), 400
    
    # Verify OTP
    if not security_manager.verify_otp(mfa_setup_data['secret'], otp):
        return jsonify({'error': 'کد OTP نامعتبر'}), 403
    
    # Save MFA settings
    if secure_db.save_mfa_settings(user_id, mfa_setup_data['secret'], mfa_setup_data['backup_codes']):
        # Enable MFA
        secure_db.enable_mfa(user_id)
        
        # Clear setup session
        session.pop('mfa_setup', None)
        
        # Log security event
        secure_db.log_security_event(user_id, 'mfa_enabled', 'MFA setup completed')
        
        return jsonify({'success': True, 'message': 'MFA enabled successfully'})
    else:
        return jsonify({'error': 'Failed to save MFA settings'}), 500

@app.route('/mfa/verify', methods=['POST'])
def mfa_verify():
    """Verify MFA code"""
    data = request.get_json() if request.is_json else request.form
    user_id = data.get('user_id')
    otp = data.get('otp')
    backup_code = data.get('backup_code')
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    # Get MFA settings
    mfa_settings = secure_db.get_mfa_settings(user_id)
    if not mfa_settings or not mfa_settings['mfa_enabled']:
        return jsonify({'error': 'MFA not enabled for this user'}), 400
    
    success = False
    attempt_type = None
    
    if otp:
        # Verify OTP
        success = security_manager.verify_otp(mfa_settings['mfa_secret'], otp)
        attempt_type = 'otp'
    elif backup_code:
        # Verify backup code
        success = security_manager.verify_backup_code(mfa_settings['backup_codes'], backup_code)
        if success:
            # Update backup codes in database
            secure_db.update_backup_codes(user_id, mfa_settings['backup_codes'])
        attempt_type = 'backup'
    else:
        return jsonify({'error': 'OTP or backup code is required'}), 400
    
    # Log attempt
    secure_db.log_mfa_attempt(user_id, attempt_type, success)
    
    if success:
        return jsonify({'success': True, 'message': 'MFA verification successful'})
    else:
        return jsonify({'error': 'کد OTP نامعتبر'}), 403

@app.route('/mfa/disable', methods=['POST'])
def mfa_disable():
    """Disable MFA for user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    user_id = session['user_id']
    data = request.get_json() if request.is_json else request.form
    otp = data.get('otp')
    
    # Get MFA settings
    mfa_settings = secure_db.get_mfa_settings(user_id)
    if not mfa_settings or not mfa_settings['mfa_enabled']:
        return jsonify({'error': 'MFA not enabled for this user'}), 400
    
    # Verify OTP before disabling
    if not security_manager.verify_otp(mfa_settings['mfa_secret'], otp):
        return jsonify({'error': 'کد OTP نامعتبر'}), 403
    
    # Disable MFA
    if secure_db.disable_mfa(user_id):
        secure_db.log_security_event(user_id, 'mfa_disabled', 'MFA disabled by user')
        return jsonify({'success': True, 'message': 'MFA disabled successfully'})
    else:
        return jsonify({'error': 'Failed to disable MFA'}), 500

# -----------------------------
# ROUTES FOR DIFFERENT DASHBOARDS
# -----------------------------

@app.route('/')
def index():
    """Main landing page with language selection"""
    return render_template('index.html')

@app.route('/player/<user_id>')
def player_dashboard(user_id):
    """Player Dashboard - Main user interface"""
    # Check authentication
    if 'user_id' not in session or session['user_id'] != user_id:
        return redirect(url_for('login'))
    
    user = mall_system.get_user(user_id)
    if not user:
        user = mall_system.create_user(user_id, "en")
    
    user.login()
    dashboard_data = mall_system.get_user_dashboard(user_id)
    
    return render_template('player_dashboard.html', 
                         user=user, 
                         dashboard=dashboard_data)

@app.route('/admin')
def admin_dashboard():
    """Super Admin Dashboard - System management"""
    # Check authentication and admin role
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # In production, check if user has admin role
    # For demo purposes, allow any authenticated user
    dashboard_data = mall_system.get_admin_dashboard()
    return render_template('admin_dashboard.html', dashboard=dashboard_data)

@app.route('/shopkeeper/<shop_id>')
def shopkeeper_dashboard(shop_id):
    """Shopkeeper Dashboard - Store management"""
    # Check authentication
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    dashboard_data = mall_system.get_shopkeeper_dashboard(shop_id)
    if not dashboard_data:
        return "Shop not found", 404
    
    return render_template('shopkeeper_dashboard.html', dashboard=dashboard_data)

@app.route('/customer-service')
def customer_service_dashboard():
    """Customer Service Dashboard - Support management"""
    # Check authentication
    if 'user_id' not in session:
        return redirect(url_for('login'))

    dashboard_data = mall_system.get_customer_service_dashboard()
    return render_template('customer_service_dashboard.html', dashboard=dashboard_data)


@app.route('/webar/treasure-hunt', methods=['GET', 'POST'])
def webar_treasure_hunt():
    """WebAR Treasure Hunt interaction"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    if request.method == 'GET':
        return render_template('webar_treasure_hunt.html', user_id=user_id)

    result = mall_system.participate_treasure_hunt(user_id)
    return jsonify(result)

# -----------------------------
# API ENDPOINTS
# -----------------------------

@app.route('/api/submit-receipt', methods=['POST'])
def api_submit_receipt():
    """API endpoint for receipt submission"""
    # Check authentication
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Rate limiting
    if not secure_db.check_rate_limit(request.remote_addr, 'submit_receipt', 10, 60):
        return jsonify({'error': 'Rate limit exceeded'}), 429
    
    data = request.get_json()
    user_id = data.get('user_id')
    amount = data.get('amount', 0)
    store = data.get('store', '')
    
    # Validate input
    if not user_id or not amount:
        return jsonify({'error': 'User ID and amount are required'}), 400
    
    # Validate amount
    validated_amount = input_validator.validate_amount(amount)
    if validated_amount is None:
        return jsonify({'error': 'Invalid amount'}), 400
    
    # Sanitize store name
    sanitized_store = input_validator.sanitize_string(store, 100)
    
    mall_system.process_receipt(user_id, validated_amount, sanitized_store)
    
    user = mall_system.get_user(user_id)
    
    # Log security event
    secure_db.log_security_event(user_id, 'receipt_submitted', f'Amount: {validated_amount}, Store: {sanitized_store}')
    
    return jsonify({
        'success': True,
        'coins': user.coins,
        'rewards': user.rewards[-1] if user.rewards else None
    })

@app.route('/api/generate-mission', methods=['POST'])
def api_generate_mission():
    """API endpoint for mission generation"""
    data = request.get_json()
    user_id = data.get('user_id')
    mission_type = data.get('mission_type', 'daily')
    
    mission = mall_system.generate_user_missions(user_id, mission_type)
    return jsonify({'success': True, 'mission': mission})

@app.route('/api/remove-receipt', methods=['POST'])
def api_remove_receipt():
    """API endpoint for admin receipt removal"""
    data = request.get_json()
    user_id = data.get('user_id')
    receipt_index = data.get('receipt_index')
    reason = data.get('reason', 'Invalid/Fraudulent')
    
    user = mall_system.get_user(user_id)
    if user:
        admin_remove_receipt(user, receipt_index, reason)
        return jsonify({'success': True, 'coins': user.coins})
    
    return jsonify({'success': False, 'error': 'User not found'})

@app.route('/api/create-ticket', methods=['POST'])
def api_create_ticket():
    """API endpoint for creating customer service tickets"""
    data = request.get_json()
    user_id = data.get('user_id')
    issue_type = data.get('issue_type')
    description = data.get('description')
    language = data.get('language', 'en')
    
    ticket_id = mall_system.customer_service.create_ticket(user_id, issue_type, description, language)
    return jsonify({'success': True, 'ticket_id': ticket_id})

@app.route('/api/respond-ticket', methods=['POST'])
def api_respond_ticket():
    """API endpoint for responding to customer service tickets"""
    data = request.get_json()
    ticket_id = data.get('ticket_id')
    response = data.get('response')
    agent_id = data.get('agent_id')
    
    mall_system.customer_service.respond_to_ticket(ticket_id, response, agent_id)
    return jsonify({'success': True})

# -----------------------------
# LANGUAGE SWITCHING
# -----------------------------

@app.route('/switch-language/<language>')
def switch_language(language):
    """Switch user language preference"""
    if 'user_id' in session:
        user = mall_system.get_user(session['user_id'])
        if user:
            user.language = language
    
    session['language'] = language
    return redirect(request.referrer or url_for('index'))

# -----------------------------
# ERROR HANDLERS
# -----------------------------

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db_status = secure_db.check_connection()
        
        # Check mall system
        mall_status = mall_system is not None
        
        # Check performance manager
        perf_status = performance_manager is not None
        
        if db_status and mall_status and perf_status:
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'services': {
                    'database': 'ok',
                    'mall_system': 'ok',
                    'performance_manager': 'ok'
                }
            }), 200
        else:
            return jsonify({
                'status': 'unhealthy',
                'timestamp': datetime.now().isoformat(),
                'services': {
                    'database': 'ok' if db_status else 'error',
                    'mall_system': 'ok' if mall_status else 'error',
                    'performance_manager': 'ok' if perf_status else 'error'
                }
            }), 503
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'error',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 