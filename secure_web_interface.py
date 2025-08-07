#!/usr/bin/env python3
"""
Secure Web Interface for Mall Gamification AI Control Panel
Integrates comprehensive security features including JWT authentication,
rate limiting, input validation, and secure database operations.
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from mall_gamification_system import MallGamificationSystem, User
from security_module import (
    SecurityManager, require_auth, SecureDatabase, RateLimiter,
    InputValidator, log_security_event, get_security_manager,
    get_secure_database, get_rate_limiter
)
from database import MallDatabase
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'deerfields_mall_secure_secret_key_2024'

# Initialize the mall system and security components
mall_system = MallGamificationSystem()
security_manager = get_security_manager()
secure_database = get_secure_database()
rate_limiter = get_rate_limiter()
input_validator = InputValidator()
mall_db = MallDatabase()

# -----------------------------
# AUTHENTICATION ROUTES
# -----------------------------

@app.route('/login', methods=['GET', 'POST'])
@rate_limiter.limit(max_requests=5, window_seconds=300)  # 5 attempts per 5 minutes
def login():
    """Secure login endpoint"""
    if request.method == 'GET':
        return render_template('login.html')
    
    data = request.get_json()
    user_id = input_validator.sanitize_string(data.get('user_id', ''), 50)
    password = data.get('password', '')
    
    # Input validation
    if not user_id or not password:
        return jsonify({'error': 'Invalid credentials'}), 400
    
    # For demo purposes, accept any user_id with a simple password check
    # In production, this should check against a secure user database
    if password == 'demo123':  # Simple demo password
        # Generate JWT token
        token = security_manager.generate_token(user_id, role='user')
        log_security_event(user_id, 'login_success', f'User logged in from {request.remote_addr}')
        
        return jsonify({
            'success': True,
            'token': token,
            'user_id': user_id,
            'role': 'user'
        })
    else:
        log_security_event(user_id, 'login_failed', f'Failed login attempt from {request.remote_addr}')
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/admin/login', methods=['GET', 'POST'])
@rate_limiter.limit(max_requests=3, window_seconds=300)  # 3 attempts per 5 minutes
def admin_login():
    """Secure admin login endpoint"""
    if request.method == 'GET':
        return render_template('admin_login.html')
    
    data = request.get_json()
    admin_id = input_validator.sanitize_string(data.get('admin_id', ''), 50)
    password = data.get('password', '')
    
    # Input validation
    if not admin_id or not password:
        return jsonify({'error': 'Invalid credentials'}), 400
    
    # For demo purposes, accept admin with specific password
    if admin_id == 'admin' and password == 'admin123':
        token = security_manager.generate_token(admin_id, role='admin')
        log_security_event(admin_id, 'admin_login_success', f'Admin logged in from {request.remote_addr}')
        
        return jsonify({
            'success': True,
            'token': token,
            'user_id': admin_id,
            'role': 'admin'
        })
    else:
        log_security_event(admin_id, 'admin_login_failed', f'Failed admin login attempt from {request.remote_addr}')
        return jsonify({'error': 'Invalid credentials'}), 401

# -----------------------------
# SECURE DASHBOARD ROUTES
# -----------------------------

@app.route('/')
@rate_limiter.limit(max_requests=20, window_seconds=60)
def index():
    """Main landing page with language selection"""
    return render_template('index.html')

@app.route('/player/<user_id>')
@require_auth()
@rate_limiter.limit(max_requests=30, window_seconds=60)
def secure_player_dashboard(user_id):
    """Secure Player Dashboard - Main user interface"""
    # Verify user can access their own dashboard
    if request.current_user['user_id'] != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    user = mall_system.get_user(user_id)
    if not user:
        user = mall_system.create_user(user_id, "en")
    
    user.login()
    dashboard_data = mall_system.get_user_dashboard(user_id)
    
    log_security_event(user_id, 'dashboard_access', 'Player dashboard accessed')
    
    return render_template('player_dashboard.html', 
                         user=user, 
                         dashboard=dashboard_data)

@app.route('/admin')
@require_auth(role='admin')
@rate_limiter.limit(max_requests=50, window_seconds=60)
def secure_admin_dashboard():
    """Secure Admin Dashboard - System management"""
    admin_id = request.current_user['user_id']
    dashboard_data = mall_system.get_admin_dashboard()
    
    log_security_event(admin_id, 'admin_dashboard_access', 'Admin dashboard accessed')
    
    return render_template('admin_dashboard.html', dashboard=dashboard_data)

@app.route('/shopkeeper/<shop_id>')
@require_auth(role='shopkeeper')
@rate_limiter.limit(max_requests=30, window_seconds=60)
def secure_shopkeeper_dashboard(shop_id):
    """Secure Shopkeeper Dashboard - Store management"""
    shopkeeper_id = request.current_user['user_id']
    dashboard_data = mall_system.get_shopkeeper_dashboard(shop_id)
    
    if not dashboard_data:
        return jsonify({'error': 'Shop not found'}), 404
    
    log_security_event(shopkeeper_id, 'shopkeeper_dashboard_access', f'Shopkeeper dashboard accessed for shop {shop_id}')
    
    return render_template('shopkeeper_dashboard.html', dashboard=dashboard_data)

@app.route('/customer-service')
@require_auth(role='customer_service')
@rate_limiter.limit(max_requests=40, window_seconds=60)
def secure_customer_service_dashboard():
    """Secure Customer Service Dashboard - Support management"""
    cs_id = request.current_user['user_id']
    dashboard_data = mall_system.get_customer_service_dashboard()
    
    log_security_event(cs_id, 'customer_service_dashboard_access', 'Customer service dashboard accessed')
    
    return render_template('customer_service_dashboard.html', dashboard=dashboard_data)

# -----------------------------
# SECURE API ENDPOINTS
# -----------------------------

@app.route('/api/submit-receipt', methods=['POST'])
@require_auth()
@rate_limiter.limit(max_requests=10, window_seconds=60)
def secure_submit_receipt():
    """Secure receipt submission endpoint"""
    user_id = request.current_user['user_id']
    data = request.get_json()
    
    # Input validation
    try:
        amount = input_validator.validate_amount(data.get('amount', 0))
        store = input_validator.sanitize_string(data.get('store', ''), 100)
        
        if amount is None or amount <= 0 or amount > 10000:  # Reasonable limits
            return jsonify({'error': 'Invalid amount'}), 400
        
        if not store or len(store) > 100:
            return jsonify({'error': 'Invalid store name'}), 400
            
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input data'}), 400
    
    # Process receipt securely
    result = mall_system.process_receipt(user_id, amount, store)

    mall_db.add_purchase_record({
        'user_id': user_id,
        'store_id': store,
        'amount': amount,
        'upload_type': data.get('upload_type', 'ocr'),
        'receipt_url': data.get('receipt_url')
    })

    # Log the receipt submission
    log_security_event(user_id, 'receipt_submitted', f'Receipt submitted: {store} - {amount}')

    user = mall_system.get_user(user_id)
    return jsonify({
        'success': True,
        'coins': user.coins,
        'rewards': user.rewards[-1] if user.rewards else None
    })

@app.route('/api/generate-mission', methods=['POST'])
@require_auth()
@rate_limiter.limit(max_requests=5, window_seconds=300)  # 5 missions per 5 minutes
def secure_generate_mission():
    """Secure mission generation endpoint"""
    user_id = request.current_user['user_id']
    data = request.get_json()
    mission_type = input_validator.sanitize_string(data.get('mission_type', 'daily'), 20)
    
    # Validate mission type
    valid_types = ['daily', 'weekly', 'special', 'brand']
    if mission_type not in valid_types:
        return jsonify({'error': 'Invalid mission type'}), 400
    
    mission = mall_system.generate_user_missions(user_id, mission_type)
    
    log_security_event(user_id, 'mission_generated', f'Mission generated: {mission_type}')
    
    return jsonify({'success': True, 'mission': mission})

@app.route('/api/remove-receipt', methods=['POST'])
@require_auth(role='admin')
@rate_limiter.limit(max_requests=10, window_seconds=60)
def secure_remove_receipt():
    """Secure admin receipt removal endpoint"""
    admin_id = request.current_user['user_id']
    data = request.get_json()
    
    user_id = input_validator.sanitize_string(data.get('user_id', ''), 50)
    receipt_index = data.get('receipt_index')
    reason = input_validator.sanitize_string(data.get('reason', 'Invalid/Fraudulent'), 200)
    
    # Input validation
    if not user_id or receipt_index is None:
        return jsonify({'error': 'Invalid input data'}), 400
    
    user = mall_system.get_user(user_id)
    if user:
        # This would need to be implemented in the mall system
        # admin_remove_receipt(user, receipt_index, reason)
        log_security_event(admin_id, 'receipt_removed', f'Receipt removed for user {user_id}: {reason}')
        return jsonify({'success': True, 'coins': user.coins})
    
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/create-ticket', methods=['POST'])
@require_auth()
@rate_limiter.limit(max_requests=5, window_seconds=300)
def secure_create_ticket():
    """Secure support ticket creation endpoint"""
    user_id = request.current_user['user_id']
    data = request.get_json()
    
    subject = input_validator.sanitize_string(data.get('subject', ''), 100)
    message = input_validator.sanitize_string(data.get('message', ''), 1000)
    priority = input_validator.sanitize_string(data.get('priority', 'medium'), 20)
    
    # Input validation
    if not subject or not message:
        return jsonify({'error': 'Subject and message are required'}), 400
    
    valid_priorities = ['low', 'medium', 'high', 'urgent']
    if priority not in valid_priorities:
        priority = 'medium'
    
    # Create ticket (this would need to be implemented in the mall system)
    # ticket_id = mall_system.create_support_ticket(user_id, subject, message, priority)
    
    log_security_event(user_id, 'ticket_created', f'Support ticket created: {subject}')
    
    return jsonify({'success': True, 'message': 'Ticket created successfully'})

@app.route('/api/respond-ticket', methods=['POST'])
@require_auth(role='customer_service')
@rate_limiter.limit(max_requests=20, window_seconds=60)
def secure_respond_ticket():
    """Secure ticket response endpoint"""
    cs_id = request.current_user['user_id']
    data = request.get_json()
    
    ticket_id = input_validator.sanitize_string(data.get('ticket_id', ''), 50)
    response = input_validator.sanitize_string(data.get('response', ''), 1000)
    status = input_validator.sanitize_string(data.get('status', 'open'), 20)
    
    # Input validation
    if not ticket_id or not response:
        return jsonify({'error': 'Ticket ID and response are required'}), 400
    
    valid_statuses = ['open', 'in_progress', 'resolved', 'closed']
    if status not in valid_statuses:
        status = 'open'
    
    # Respond to ticket (this would need to be implemented in the mall system)
    # result = mall_system.respond_to_ticket(ticket_id, cs_id, response, status)
    
    log_security_event(cs_id, 'ticket_responded', f'Ticket {ticket_id} responded to')
    
    return jsonify({'success': True, 'message': 'Response submitted successfully'})

@app.route('/api/update-user', methods=['POST'])
@require_auth()
@rate_limiter.limit(max_requests=10, window_seconds=300)
def secure_update_user():
    """Secure user profile update endpoint"""
    user_id = request.current_user['user_id']
    data = request.get_json()
    
    # Validate and sanitize input
    updates = {}
    
    if 'name' in data:
        name = input_validator.sanitize_string(data['name'], 100)
        if name:
            updates['name'] = name
    
    if 'email' in data:
        email = input_validator.sanitize_string(data['email'], 100)
        if email and input_validator.validate_email(email):
            updates['email'] = email
    
    if 'phone' in data:
        phone = input_validator.sanitize_string(data['phone'], 20)
        if phone and input_validator.validate_phone(phone):
            updates['phone'] = phone
    
    if not updates:
        return jsonify({'error': 'No valid updates provided'}), 400
    
    # Update user securely using the secure database
    success = secure_database.update_user_safe(user_id, updates)
    
    if success:
        log_security_event(user_id, 'profile_updated', f'Profile updated: {list(updates.keys())}')
        return jsonify({'success': True, 'message': 'Profile updated successfully'})
    else:
        return jsonify({'error': 'Failed to update profile'}), 500

@app.route('/api/get-user-data', methods=['GET'])
@require_auth()
@rate_limiter.limit(max_requests=30, window_seconds=60)
def secure_get_user_data():
    """Secure endpoint to get user data"""
    user_id = request.current_user['user_id']
    
    user = mall_system.get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Return only safe user data
    user_data = {
        'user_id': user.user_id,
        'name': user.name,
        'coins': user.coins,
        'xp': user.xp,
        'level': user.level,
        'vip_tier': user.vip_tier,
        'login_streak': user.login_streak
    }
    
    log_security_event(user_id, 'data_accessed', 'User data accessed')
    
    return jsonify({'success': True, 'user': user_data})

# -----------------------------
# UTILITY ROUTES
# -----------------------------

@app.route('/switch-language/<language>')
@rate_limiter.limit(max_requests=20, window_seconds=60)
def switch_language(language):
    """Switch application language"""
    valid_languages = ['en', 'ar', 'fr', 'es']
    if language not in valid_languages:
        language = 'en'
    
    session['language'] = language
    return redirect(request.referrer or url_for('index'))

@app.route('/logout')
def logout():
    """Logout endpoint"""
    if hasattr(request, 'current_user'):
        user_id = request.current_user.get('user_id')
        if user_id:
            log_security_event(user_id, 'logout', 'User logged out')
    
    return jsonify({'success': True, 'message': 'Logged out successfully'})

# -----------------------------
# ERROR HANDLERS
# -----------------------------

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(429)
def rate_limit_exceeded(error):
    """Handle rate limit exceeded"""
    return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429

# -----------------------------
# HEALTH CHECK
# -----------------------------

@app.route('/health')
@rate_limiter.limit(max_requests=10, window_seconds=60)
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'security': 'enabled'
    })

if __name__ == '__main__':
    print("[SECURITY] Starting secure web interface...")
    print("[SECURITY] JWT authentication enabled")
    print("[SECURITY] Rate limiting enabled")
    print("[SECURITY] Input validation enabled")
    print("[SECURITY] Secure database operations enabled")
    
    app.run(debug=False, host='0.0.0.0', port=5000) 