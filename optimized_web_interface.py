#!/usr/bin/env python3
"""
Optimized Web Interface for Mall Gamification AI Control Panel
Integrates comprehensive security features and performance optimizations including
JWT authentication, rate limiting, input validation, async processing, and caching.
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, g
from mall_gamification_system import MallGamificationSystem, User
from security_module import (
    SecurityManager, require_auth, SecureDatabase, RateLimiter,
    InputValidator, log_security_event, get_security_manager,
    get_secure_database, get_rate_limiter
)
from performance_module import (
    PerformanceManager, AsyncTaskManager, CachedDatabase, 
    PerformanceMonitor, OptimizedGraphicsEngine, record_performance_event,
    get_performance_manager, get_performance_monitor, get_optimized_graphics
)
import time
import asyncio
import logging
from datetime import datetime
from i18n import translator, get_locale

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Initialize systems
mall_system = MallGamificationSystem()
security_manager = get_security_manager()
secure_database = get_secure_database()
rate_limiter = get_rate_limiter()
input_validator = InputValidator()

# Initialize performance systems
performance_manager = get_performance_manager()
performance_monitor = get_performance_monitor()
optimized_graphics = get_optimized_graphics()
async_task_manager = AsyncTaskManager()
cached_database = CachedDatabase()

@app.before_request
def set_language():
    g.lang = get_locale()


@app.context_processor
def inject_translations():
    lang = getattr(g, 'lang', translator.default_locale)
    return {'t': lambda key: translator.gettext(key, lang)}

# -----------------------------
# MAIN ROUTES
# -----------------------------

@app.route('/')
@rate_limiter.limit(max_requests=30, window_seconds=60)
def index():
    """Main landing page with language selection"""
    start_time = time.time()
    
    # Record performance
    response_time = time.time() - start_time
    record_performance_event('main_page', response_time)
    
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
@rate_limiter.limit(max_requests=5, window_seconds=300)
def login():
    """Login endpoint with performance monitoring"""
    start_time = time.time()
    lang = getattr(g, 'lang', translator.default_locale)
    
    if request.method == 'POST':
        data = request.get_json()
        
        # Input validation
        email = input_validator.validate_email(data.get('email', ''))
        password = data.get('password', '')
        
        if not email:
            return jsonify({'error': translator.gettext('invalid_email_format', lang)}), 400
        
        # Authenticate user
        user = mall_system.authenticate_user(email, password)
        
        if user:
            # Generate JWT token
            token = security_manager.generate_token(user.user_id, user.role)
            
            # Record performance
            response_time = time.time() - start_time
            record_performance_event('login_success', response_time)
            
            return jsonify({
                'status': 'success',
                'token': token,
                'user_id': user.user_id,
                'role': user.role
            })
        else:
            # Record failed login
            response_time = time.time() - start_time
            record_performance_event('login_failed', response_time)
            log_security_event('login_failed', {'email': email, 'ip': request.remote_addr})
            
            return jsonify({'error': translator.gettext('invalid_credentials', lang)}), 401
    
    return render_template('login.html')

@app.route('/admin/login', methods=['GET', 'POST'])
@rate_limiter.limit(max_requests=3, window_seconds=300)
def admin_login():
    """Admin login endpoint with enhanced security"""
    start_time = time.time()
    lang = getattr(g, 'lang', translator.default_locale)
    
    if request.method == 'POST':
        data = request.get_json()
        
        # Input validation
        email = input_validator.validate_email(data.get('email', ''))
        password = data.get('password', '')
        
        if not email:
            return jsonify({'error': translator.gettext('invalid_email_format', lang)}), 400
        
        # Authenticate admin
        user = mall_system.authenticate_user(email, password)
        
        if user and user.role == 'admin':
            # Generate admin JWT token
            token = security_manager.generate_token(user.user_id, 'admin')
            
            # Record performance
            response_time = time.time() - start_time
            record_performance_event('admin_login_success', response_time)
            
            return jsonify({
                'status': 'success',
                'token': token,
                'user_id': user.user_id,
                'role': 'admin'
            })
        else:
            # Record failed admin login
            response_time = time.time() - start_time
            record_performance_event('admin_login_failed', response_time)
            log_security_event('admin_login_failed', {'email': email, 'ip': request.remote_addr})
            
            return jsonify({'error': translator.gettext('invalid_admin_credentials', lang)}), 401
    
    return render_template('admin_login.html')

@app.route('/player/<user_id>')
@require_auth()
@rate_limiter.limit(max_requests=20, window_seconds=60)
def player_dashboard(user_id):
    """Player dashboard with caching"""
    start_time = time.time()
    lang = getattr(g, 'lang', translator.default_locale)
    
    # Get user data with caching
    user_data = cached_database.get_user(user_id)
    
    if not user_data:
        return jsonify({'error': translator.gettext('user_not_found', lang)}), 404
    
    # Get player stats
    player_stats = mall_system.get_player_stats(user_id)
    
    # Record performance
    response_time = time.time() - start_time
    record_performance_event('player_dashboard', response_time)
    
    return render_template('player_dashboard.html', 
                         user=user_data, 
                         stats=player_stats)

@app.route('/admin')
@require_auth(role='admin')
@rate_limiter.limit(max_requests=10, window_seconds=60)
def admin_dashboard():
    """Admin dashboard with performance monitoring"""
    start_time = time.time()
    
    # Get admin dashboard data
    dashboard_data = mall_system.get_admin_dashboard()
    
    # Get performance metrics
    performance_report = performance_monitor.get_performance_report()
    
    # Record performance
    response_time = time.time() - start_time
    record_performance_event('admin_dashboard', response_time)
    
    return render_template('admin_dashboard.html', 
                         dashboard=dashboard_data,
                         performance=performance_report)

@app.route('/shopkeeper/<shop_id>')
@require_auth(role='shopkeeper')
@rate_limiter.limit(max_requests=15, window_seconds=60)
def shopkeeper_dashboard(shop_id):
    """Shopkeeper dashboard"""
    start_time = time.time()
    lang = getattr(g, 'lang', translator.default_locale)
    
    # Validate shop_id
    if not input_validator.validate_string(shop_id, max_length=50):
        return jsonify({'error': translator.gettext('invalid_shop_id', lang)}), 400
    
    # Get shop data
    shop_data = mall_system.get_shop_data(shop_id)
    
    # Record performance
    response_time = time.time() - start_time
    record_performance_event('shopkeeper_dashboard', response_time)
    
    return render_template('shopkeeper_dashboard.html', shop=shop_data)

@app.route('/customer-service')
@require_auth(role='customer_service')
@rate_limiter.limit(max_requests=20, window_seconds=60)
def customer_service_dashboard():
    """Customer service dashboard"""
    start_time = time.time()
    
    # Get customer service data
    service_data = mall_system.get_customer_service_data()
    
    # Record performance
    response_time = time.time() - start_time
    record_performance_event('customer_service_dashboard', response_time)
    
    return render_template('customer_service_dashboard.html', data=service_data)

@app.route('/api/submit-receipt', methods=['POST'])
@require_auth()
@rate_limiter.limit(max_requests=10, window_seconds=60)
async def submit_receipt():
    """Receipt submission with async processing and security"""
    start_time = time.time()
    lang = getattr(g, 'lang', translator.default_locale)
    
    user_id = request.current_user['user_id']
    data = request.get_json()
    
    # Input validation
    try:
        amount = float(data.get('amount', 0))
        store = input_validator.sanitize_string(data.get('store', ''), max_length=100)
        
        if amount <= 0 or amount > 10000:  # Reasonable limits
            return jsonify({'error': translator.gettext('invalid_amount', lang)}), 400

        if not store:
            return jsonify({'error': translator.gettext('invalid_store_name', lang)}), 400
            
    except (ValueError, TypeError):
        return jsonify({'error': translator.gettext('invalid_input_data', lang)}), 400
    
    # Async processing
    try:
        result = await async_task_manager.process_receipt_async(user_id, amount, store)
        
        # Update user data in batch if successful
        if result['status'] == 'success':
            user_updates = [(user_id, {'coins': result['coins_earned']})]
            cached_database.batch_update_users(user_updates)
        
        # Trigger graphics effect
        optimized_graphics.trigger_effect('coin_earned', 
                                        coins=result.get('coins_earned', 0),
                                        user_id=user_id)
        
        # Record performance
        response_time = time.time() - start_time
        record_performance_event('receipt_submission_async', response_time)
        
        # Log security event
        log_security_event('receipt_submitted', {
            'user_id': user_id,
            'amount': amount,
            'store': store,
            'result': result['status']
        })
        
        return jsonify({
            **result,
            'performance': {
                'response_time': response_time,
                'processed_async': True
            }
        })
        
    except Exception as e:
        logger.error(f"Receipt processing error: {e}")
        return jsonify({'error': translator.gettext('processing_failed', lang)}), 500

@app.route('/api/optimized-submit-receipt', methods=['POST'])
@require_auth()
@rate_limiter.limit(max_requests=10, window_seconds=60)
async def optimized_submit_receipt():
    """Optimized receipt submission with async processing"""
    start_time = time.time()
    lang = getattr(g, 'lang', translator.default_locale)
    
    user_id = request.current_user['user_id']
    data = request.get_json()
    
    # Input validation
    try:
        amount = float(data.get('amount', 0))
        store = input_validator.validate_string(data.get('store', ''), max_length=100)
        
        if amount <= 0 or amount > 10000:  # Reasonable limits
            return jsonify({'error': translator.gettext('invalid_amount', lang)}), 400

        if not store:
            return jsonify({'error': translator.gettext('invalid_store_name', lang)}), 400
            
    except (ValueError, TypeError):
        return jsonify({'error': translator.gettext('invalid_input_data', lang)}), 400
    
    # Async processing
    try:
        result = await async_task_manager.process_receipt_async(user_id, amount, store)
        
        # Update user data in batch if successful
        if result['status'] == 'success':
            user_updates = [(user_id, {'coins': result['coins_earned']})]
            cached_database.batch_update_users(user_updates)
        
        # Trigger graphics effect
        optimized_graphics.trigger_effect('coin_earned', 
                                        coins=result.get('coins_earned', 0),
                                        user_id=user_id)
        
        # Record performance
        response_time = time.time() - start_time
        record_performance_event('receipt_submission_async', response_time)
        
        # Log security event
        log_security_event('receipt_submitted', {
            'user_id': user_id,
            'amount': amount,
            'store': store,
            'result': result['status']
        })
        
        return jsonify({
            **result,
            'performance': {
                'response_time': response_time,
                'processed_async': True
            }
        })
        
    except Exception as e:
        logger.error(f"Receipt processing error: {e}")
        return jsonify({'error': translator.gettext('processing_failed', lang)}), 500

@app.route('/api/generate-mission', methods=['POST'])
@require_auth()
@rate_limiter.limit(max_requests=5, window_seconds=60)
def generate_mission():
    """Generate mission with performance monitoring"""
    start_time = time.time()
    lang = getattr(g, 'lang', translator.default_locale)
    
    user_id = request.current_user['user_id']
    data = request.get_json()
    
    # Input validation
    mission_type = input_validator.validate_string(data.get('type', ''), max_length=50)
    
    if not mission_type:
        return jsonify({'error': translator.gettext('invalid_mission_type', lang)}), 400
    
    # Generate mission
    mission = mall_system.generate_mission(user_id, mission_type)
    
    # Record performance
    response_time = time.time() - start_time
    record_performance_event('mission_generation', response_time)
    
    return jsonify({
        'status': 'success',
        'mission': mission,
        'performance': {
            'response_time': response_time
        }
    })

@app.route('/api/remove-receipt', methods=['DELETE'])
@require_auth()
@rate_limiter.limit(max_requests=5, window_seconds=60)
def remove_receipt():
    """Remove receipt with validation"""
    start_time = time.time()
    lang = getattr(g, 'lang', translator.default_locale)
    
    user_id = request.current_user['user_id']
    data = request.get_json()
    
    # Input validation
    receipt_id = input_validator.validate_string(data.get('receipt_id', ''), max_length=50)

    if not receipt_id:
        return jsonify({'error': translator.gettext('invalid_receipt_id', lang)}), 400
    
    # Remove receipt
    result = mall_system.remove_receipt(user_id, receipt_id)
    
    # Record performance
    response_time = time.time() - start_time
    record_performance_event('receipt_removal', response_time)
    
    return jsonify({
        'status': 'success' if result else 'failed',
        'performance': {
            'response_time': response_time
        }
    })

@app.route('/api/create-ticket', methods=['POST'])
@require_auth()
@rate_limiter.limit(max_requests=3, window_seconds=60)
def create_ticket():
    """Create support ticket with validation"""
    start_time = time.time()
    lang = getattr(g, 'lang', translator.default_locale)
    
    user_id = request.current_user['user_id']
    data = request.get_json()
    
    # Input validation
    subject = input_validator.validate_string(data.get('subject', ''), max_length=200)
    message = input_validator.validate_string(data.get('message', ''), max_length=1000)
    
    if not subject or not message:
        return jsonify({'error': translator.gettext('invalid_ticket_data', lang)}), 400
    
    # Create ticket
    ticket = mall_system.create_support_ticket(user_id, subject, message)
    
    # Record performance
    response_time = time.time() - start_time
    record_performance_event('ticket_creation', response_time)
    
    return jsonify({
        'status': 'success',
        'ticket_id': ticket['id'],
        'performance': {
            'response_time': response_time
        }
    })

@app.route('/api/respond-ticket', methods=['POST'])
@require_auth(role='customer_service')
@rate_limiter.limit(max_requests=10, window_seconds=60)
def respond_ticket():
    """Respond to support ticket"""
    start_time = time.time()
    lang = getattr(g, 'lang', translator.default_locale)
    
    agent_id = request.current_user['user_id']
    data = request.get_json()
    
    # Input validation
    ticket_id = input_validator.validate_string(data.get('ticket_id', ''), max_length=50)
    response = input_validator.validate_string(data.get('response', ''), max_length=1000)
    
    if not ticket_id or not response:
        return jsonify({'error': translator.gettext('invalid_response_data', lang)}), 400
    
    # Respond to ticket
    result = mall_system.respond_to_ticket(ticket_id, agent_id, response)
    
    # Record performance
    response_time = time.time() - start_time
    record_performance_event('ticket_response', response_time)
    
    return jsonify({
        'status': 'success' if result else 'failed',
        'performance': {
            'response_time': response_time
        }
    })

@app.route('/api/update-user', methods=['PUT'])
@require_auth()
@rate_limiter.limit(max_requests=5, window_seconds=60)
def update_user():
    """Update user data with validation"""
    start_time = time.time()
    lang = getattr(g, 'lang', translator.default_locale)
    
    user_id = request.current_user['user_id']
    data = request.get_json()
    
    # Input validation
    updates = {}
    if 'name' in data:
        updates['name'] = input_validator.validate_string(data['name'], max_length=100)
    if 'email' in data:
        updates['email'] = input_validator.validate_email(data['email'])
    if 'phone' in data:
        updates['phone'] = input_validator.validate_phone(data['phone'])
    
    # Remove None values
    updates = {k: v for k, v in updates.items() if v is not None}
    
    if not updates:
        return jsonify({'error': translator.gettext('no_valid_updates', lang)}), 400
    
    # Update user
    result = secure_database.update_user_safe(user_id, updates)
    
    # Record performance
    response_time = time.time() - start_time
    record_performance_event('user_update', response_time)
    
    return jsonify({
        'status': 'success' if result else 'failed',
        'performance': {
            'response_time': response_time
        }
    })

@app.route('/api/get-user-data', methods=['GET'])
@require_auth()
@rate_limiter.limit(max_requests=20, window_seconds=60)
def get_user_data():
    """Get user data with caching"""
    start_time = time.time()
    lang = getattr(g, 'lang', translator.default_locale)
    
    user_id = request.current_user['user_id']
    
    # Get user data with caching
    user_data = cached_database.get_user(user_id)
    
    if not user_data:
        return jsonify({'error': translator.gettext('user_not_found', lang)}), 404
    
    # Record performance
    response_time = time.time() - start_time
    record_performance_event('user_data_retrieval', response_time)
    
    return jsonify({
        'status': 'success',
        'user': user_data,
        'performance': {
            'response_time': response_time,
            'cached': True
        }
    })

@app.route('/api/performance-metrics', methods=['GET'])
@require_auth(role='admin')
def get_performance_metrics():
    """Get performance metrics for monitoring"""
    metrics = performance_monitor.get_performance_report()
    
    # Get graphics performance
    graphics_metrics = optimized_graphics.render_frame()
    
    return jsonify({
        'system_metrics': metrics,
        'graphics_metrics': graphics_metrics,
        'cache_status': {
            'redis_available': performance_manager.redis_client is not None,
            'active_effects': len(optimized_graphics.effects_manager.active_effects)
        }
    })

@app.route('/logout')
@rate_limiter.limit(max_requests=10, window_seconds=60)
def logout():
    """Logout user and clear session"""
    start_time = time.time()
    lang = getattr(g, 'lang', translator.default_locale)
    
    if hasattr(request, 'current_user'):
        user_id = request.current_user.get('user_id')
        if user_id:
            # Log security event
            log_security_event('logout', {'user_id': user_id, 'ip': request.remote_addr})
    
    # Record performance
    response_time = time.time() - start_time
    record_performance_event('logout', response_time)

    session.clear()
    return jsonify({'status': 'success', 'message': translator.gettext('logged_out', lang)})

@app.route('/switch-language/<language>')
@rate_limiter.limit(max_requests=20, window_seconds=60)
def switch_language(language):
    """Switch user language preference"""
    start_time = time.time()
    lang = getattr(g, 'lang', translator.default_locale)
    
    # Validate language
    valid_languages = ['en', 'ar']
    if language not in valid_languages:
        return jsonify({'error': translator.gettext('invalid_language', lang)}), 400
    
    # Update user language if authenticated
    if hasattr(request, 'current_user'):
        user_id = request.current_user.get('user_id')
        if user_id:
            # Update user language in database
            secure_database.update_user_safe(user_id, {'language': language})
    
    session['lang'] = language
    # Record performance
    response_time = time.time() - start_time
    record_performance_event('language_switch', response_time)

    return jsonify({'status': 'success', 'language': language})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'services': {
            'database': 'connected',
            'security': 'active',
            'performance': 'monitoring',
            'graphics': 'optimized'
        },
        'timestamp': datetime.now().isoformat()
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 error: {request.url}")
    lang = getattr(g, 'lang', translator.default_locale)
    return jsonify({'error': translator.gettext('resource_not_found', lang)}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    # Don't expose internal error details to client
    lang = getattr(g, 'lang', translator.default_locale)
    return jsonify({'error': translator.gettext('internal_error', lang)}), 500

@app.errorhandler(429)
def rate_limit_exceeded(error):
    logger.warning(f"Rate limit exceeded for IP: {request.remote_addr}")
    lang = getattr(g, 'lang', translator.default_locale)
    return jsonify({'error': translator.gettext('too_many_requests', lang)}), 429

@app.errorhandler(401)
def unauthorized(error):
    logger.warning(f"Unauthorized access attempt from IP: {request.remote_addr}")
    lang = getattr(g, 'lang', translator.default_locale)
    return jsonify({'error': translator.gettext('authentication_required', lang)}), 401

@app.errorhandler(403)
def forbidden(error):
    logger.warning(f"Forbidden access attempt from IP: {request.remote_addr}")
    lang = getattr(g, 'lang', translator.default_locale)
    return jsonify({'error': translator.gettext('access_denied', lang)}), 403

if __name__ == '__main__':
    # Log startup
    logger.info("🚀 Starting optimized web interface...")
    logger.info("🔒 Security features: JWT, Rate Limiting, Input Validation")
    logger.info("⚡ Performance features: Caching, Async Processing, Monitoring")
    
    # Initialize performance monitoring
    performance_monitor.log_performance_metrics()
    
    # Log security initialization
    log_security_event('system_startup', {
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'features': ['jwt', 'rate_limiting', 'input_validation', 'async_processing', 'caching']
    })
    
    # Start the Flask app
    logger.info("🌐 Web interface ready on http://0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 