# Security Documentation for Deerfields Mall Gamification System

## Overview

This document describes the comprehensive security features implemented in the mall gamification system, including JWT authentication, rate limiting, input validation, and secure database operations.

## Table of Contents

1. [Security Components](#security-components)
2. [Installation and Setup](#installation-and-setup)
3. [Authentication System](#authentication-system)
4. [Rate Limiting](#rate-limiting)
5. [Input Validation](#input-validation)
6. [Secure Database Operations](#secure-database-operations)
7. [API Security](#api-security)
8. [Best Practices](#best-practices)
9. [Testing](#testing)
10. [Troubleshooting](#troubleshooting)

## Security Components

### Core Security Modules

- **`security_module.py`**: Main security module containing all security features
- **`secure_web_interface.py`**: Secure version of the web interface with integrated security
- **`test_security_features.py`**: Comprehensive test suite for security features

### Key Classes and Functions

#### SecurityManager
- JWT token generation and verification
- Password hashing and verification
- Security logging

#### SecureDatabase
- Parameterized query execution
- Column whitelisting for safe updates
- Security audit logging
- Rate limiting storage

#### RateLimiter
- Database-based rate limiting
- Memory-based fallback
- Configurable limits per endpoint

#### InputValidator
- Email validation
- Phone number validation
- String sanitization
- Amount validation

## Installation and Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

The requirements.txt file includes:
```
Flask==2.3.3
Werkzeug==2.3.7
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
blinker==1.6.3
PyJWT==2.8.0
```

### 2. Initialize Security Components

```python
from security_module import (
    SecurityManager, SecureDatabase, RateLimiter, 
    InputValidator, get_security_manager, get_secure_database
)

# Get global instances
security_manager = get_security_manager()
secure_database = get_secure_database()
rate_limiter = get_rate_limiter()
input_validator = InputValidator()
```

### 3. Run Security Tests

```bash
python test_security_features.py
```

## Authentication System

### JWT Token Management

#### Generating Tokens

```python
from security_module import SecurityManager

security_manager = SecurityManager()

# Generate token for user
token = security_manager.generate_token("user123", role="user")

# Generate token for admin
admin_token = security_manager.generate_token("admin", role="admin")
```

#### Verifying Tokens

```python
# Verify token
payload = security_manager.verify_token(token)
if payload:
    user_id = payload['user_id']
    role = payload['role']
    print(f"Authenticated user: {user_id} with role: {role}")
else:
    print("Invalid or expired token")
```

### Authentication Decorators

#### Basic Authentication

```python
from security_module import require_auth

@app.route('/protected-endpoint')
@require_auth()
def protected_endpoint():
    user_id = request.current_user['user_id']
    return jsonify({'message': f'Hello {user_id}'})
```

#### Role-Based Authentication

```python
@app.route('/admin-only')
@require_auth(role='admin')
def admin_endpoint():
    admin_id = request.current_user['user_id']
    return jsonify({'message': f'Admin {admin_id} accessed'})
```

### Login Endpoints

#### User Login

```python
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data.get('user_id')
    password = data.get('password')
    
    # Validate credentials (implement your own logic)
    if validate_credentials(user_id, password):
        token = security_manager.generate_token(user_id, role='user')
        return jsonify({'token': token, 'success': True})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
```

#### Admin Login

```python
@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    admin_id = data.get('admin_id')
    password = data.get('password')
    
    if admin_id == 'admin' and password == 'admin123':
        token = security_manager.generate_token(admin_id, role='admin')
        return jsonify({'token': token, 'success': True})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
```

## Rate Limiting

### Configuration

Rate limiting can be configured per endpoint with different limits:

```python
@app.route('/api/submit-receipt', methods=['POST'])
@require_auth()
@rate_limiter.limit(max_requests=10, window_seconds=60)  # 10 requests per minute
def submit_receipt():
    # Endpoint logic
    pass

@app.route('/api/generate-mission', methods=['POST'])
@require_auth()
@rate_limiter.limit(max_requests=5, window_seconds=300)  # 5 requests per 5 minutes
def generate_mission():
    # Endpoint logic
    pass
```

### Rate Limit Responses

When rate limits are exceeded, the system returns:

```json
{
    "error": "Rate limit exceeded"
}
```

With HTTP status code 429.

### Custom Rate Limiting

```python
from security_module import RateLimiter, SecureDatabase

# Create custom rate limiter
secure_db = SecureDatabase()
custom_limiter = RateLimiter(secure_db)

@app.route('/custom-endpoint')
@custom_limiter.limit(max_requests=20, window_seconds=120)
def custom_endpoint():
    # Endpoint logic
    pass
```

## Input Validation

### Email Validation

```python
from security_module import InputValidator

validator = InputValidator()

# Valid emails
print(validator.validate_email("user@example.com"))  # True
print(validator.validate_email("user.name@domain.co.uk"))  # True

# Invalid emails
print(validator.validate_email("invalid-email"))  # False
print(validator.validate_email("@domain.com"))  # False
```

### Phone Validation

```python
# Valid phone numbers
print(validator.validate_phone("+1234567890"))  # True
print(validator.validate_phone("123-456-7890"))  # True
print(validator.validate_phone("(123) 456-7890"))  # True

# Invalid phone numbers
print(validator.validate_phone("123"))  # False
print(validator.validate_phone("abc-def-ghij"))  # False
```

### String Sanitization

```python
# Sanitize potentially dangerous input
dangerous_input = "<script>alert('xss')</script>"
sanitized = validator.sanitize_string(dangerous_input)
print(sanitized)  # "&lt;script&gt;alert('xss')&lt;/script&gt;"

# Limit length
long_input = "A" * 300
sanitized = validator.sanitize_string(long_input, max_length=100)
print(len(sanitized))  # 100
```

### Amount Validation

```python
# Valid amounts
print(validator.validate_amount("100.50"))  # 100.5
print(validator.validate_amount(200))  # 200.0
print(validator.validate_amount(0.01))  # 0.01

# Invalid amounts
print(validator.validate_amount("-100"))  # None
print(validator.validate_amount("abc"))  # None
print(validator.validate_amount(0))  # None
print(validator.validate_amount(1000000))  # None (exceeds limit)
```

## Secure Database Operations

### Parameterized Queries

```python
from security_module import SecureDatabase

secure_db = SecureDatabase()

# Safe query execution
cursor = secure_db.execute_safe_query(
    "SELECT * FROM users WHERE user_id = ? AND status = ?",
    ("user123", "active")
)
```

### Safe User Updates

```python
# Update user with whitelisted columns only
updates = {
    'name': 'John Doe',
    'coins': 150,
    'xp': 75,
    'malicious_field': 'hack_attempt'  # This will be filtered out
}

success = secure_db.update_user_safe("user123", updates)
if success:
    print("User updated successfully")
else:
    print("Update failed")
```

### Security Event Logging

```python
# Log security events
secure_db.log_security_event(
    user_id="user123",
    action="login_success",
    details="User logged in from 192.168.1.100"
)
```

## API Security

### Secure API Endpoints

All API endpoints in `secure_web_interface.py` include:

1. **Authentication**: JWT token verification
2. **Rate Limiting**: Configurable request limits
3. **Input Validation**: Sanitized and validated inputs
4. **Role-Based Access**: Different permissions for different roles

### Example Secure Endpoint

```python
@app.route('/api/submit-receipt', methods=['POST'])
@require_auth()
@rate_limiter.limit(max_requests=10, window_seconds=60)
def secure_submit_receipt():
    user_id = request.current_user['user_id']
    data = request.get_json()
    
    # Input validation
    try:
        amount = input_validator.validate_amount(data.get('amount', 0))
        store = input_validator.sanitize_string(data.get('store', ''), 100)
        
        if amount is None or amount <= 0 or amount > 10000:
            return jsonify({'error': 'Invalid amount'}), 400
        
        if not store or len(store) > 100:
            return jsonify({'error': 'Invalid store name'}), 400
            
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input data'}), 400
    
    # Process receipt securely
    result = mall_system.process_receipt(user_id, amount, store)
    
    # Log security event
    log_security_event(user_id, 'receipt_submitted', f'Receipt: {store} - {amount}')
    
    return jsonify({'success': True, 'result': result})
```

### API Response Format

All API responses follow a consistent format:

```json
{
    "success": true,
    "data": {...},
    "message": "Operation completed successfully"
}
```

Error responses:

```json
{
    "error": "Error description",
    "code": "ERROR_CODE"
}
```

## Best Practices

### 1. Token Management

- Store tokens securely (not in localStorage for production)
- Implement token refresh mechanism
- Set appropriate expiration times
- Rotate secret keys regularly

### 2. Input Validation

- Always validate and sanitize user input
- Use whitelisting approach for allowed values
- Implement proper error handling
- Log validation failures

### 3. Rate Limiting

- Set appropriate limits based on endpoint usage
- Monitor rate limit violations
- Implement progressive delays for repeated violations
- Use different limits for different user roles

### 4. Database Security

- Always use parameterized queries
- Implement column whitelisting
- Log all database operations
- Regular security audits

### 5. Error Handling

- Don't expose sensitive information in error messages
- Log all security-related errors
- Implement proper HTTP status codes
- Provide user-friendly error messages

## Testing

### Running Security Tests

```bash
python test_security_features.py
```

### Test Coverage

The test suite covers:

1. **Security Module Components**
   - JWT token generation and verification
   - Password hashing
   - Input validation
   - Database operations

2. **Rate Limiting**
   - Memory-based rate limiting
   - Database-based rate limiting
   - Limit enforcement

3. **JWT Authentication**
   - Token generation
   - Token verification
   - Invalid token handling

4. **Secure Database Operations**
   - Parameterized queries
   - Column whitelisting
   - Security event logging

### Manual Testing

#### Test JWT Authentication

```bash
# 1. Login to get token
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"user_id": "testuser", "password": "demo123"}'

# 2. Use token for authenticated request
curl -X GET http://localhost:5000/api/get-user-data \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### Test Rate Limiting

```bash
# Make multiple requests to trigger rate limit
for i in {1..15}; do
  curl -X POST http://localhost:5000/api/submit-receipt \
    -H "Authorization: Bearer YOUR_TOKEN_HERE" \
    -H "Content-Type: application/json" \
    -d '{"amount": 100, "store": "Test Store"}'
done
```

## Troubleshooting

### Common Issues

#### 1. PyJWT Import Error

```
ImportError: No module named 'jwt'
```

**Solution**: Install PyJWT
```bash
pip install PyJWT==2.8.0
```

#### 2. Database Connection Issues

```
sqlite3.OperationalError: database is locked
```

**Solution**: Ensure proper database connection handling
```python
# Use check_same_thread=False for Flask
conn = sqlite3.connect(db_path, check_same_thread=False)
```

#### 3. Rate Limiting Not Working

**Solution**: Check if database tables are created
```python
# Ensure rate_limits table exists
secure_database.create_tables()
```

#### 4. Token Verification Fails

**Solution**: Check secret key consistency
```python
# Use the same secret key for generation and verification
security_manager = SecurityManager(secret_key="your_secret_key")
```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Security module logging
security_logger = logging.getLogger('SecurityManager')
security_logger.setLevel(logging.DEBUG)
```

### Security Monitoring

Monitor security events:

```python
# Check security audit log
cursor = secure_database.execute_safe_query(
    "SELECT * FROM security_audit_log ORDER BY timestamp DESC LIMIT 10"
)
for row in cursor.fetchall():
    print(f"{row['timestamp']}: {row['action']} by {row['user_id']}")
```

## Security Checklist

- [ ] JWT tokens implemented and working
- [ ] Rate limiting configured for all endpoints
- [ ] Input validation applied to all user inputs
- [ ] Database queries use parameterized statements
- [ ] Column whitelisting implemented for updates
- [ ] Security event logging enabled
- [ ] Error handling doesn't expose sensitive information
- [ ] Authentication decorators applied to protected endpoints
- [ ] Role-based access control implemented
- [ ] Security tests passing
- [ ] Dependencies updated and secure
- [ ] Secret keys properly managed
- [ ] HTTPS enabled for production
- [ ] Regular security audits scheduled

## Conclusion

The security features provide a comprehensive security layer for the mall gamification system. Regular testing, monitoring, and updates are essential to maintain security standards.

For additional security measures, consider implementing:

- Two-factor authentication
- IP whitelisting
- Advanced threat detection
- Regular penetration testing
- Security incident response procedures 