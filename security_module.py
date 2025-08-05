#!/usr/bin/env python3
"""
Security Module for Deerfields Mall Gamification System
Provides comprehensive security features including JWT authentication, 
secure database operations, rate limiting, input validation, and MFA.
"""

import hashlib
import secrets
import jwt
import sqlite3
import logging
import base64
import re
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, List, Optional, Any, Union
from flask import request, jsonify, session, current_app

# Add bcrypt for password hashing
try:
    import bcrypt
except ImportError:
    print("[WARNING] bcrypt not installed. Please add 'bcrypt==4.0.1' to requirements.txt")
    bcrypt = None

# Add PyJWT to requirements if not already present
try:
    import jwt
except ImportError:
    print("[WARNING] PyJWT not installed. Please add 'PyJWT==2.8.0' to requirements.txt")
    jwt = None

# Add pyotp for MFA
try:
    import pyotp
except ImportError:
    print("[WARNING] pyotp not installed. Please add 'pyotp==2.9.0' to requirements.txt")
    pyotp = None

# Custom exception classes for better error handling
class SecurityError(Exception):
    """Base security exception"""
    pass

class AuthenticationError(SecurityError):
    """Authentication related errors"""
    pass

class AuthorizationError(SecurityError):
    """Authorization related errors"""
    pass

class ValidationError(SecurityError):
    """Input validation errors"""
    pass

class RateLimitError(SecurityError):
    """Rate limiting errors"""
    pass

class DatabaseSecurityError(SecurityError):
    """Database security errors"""
    pass

class SecurityManager:
    """Manages JWT token generation and verification with MFA support"""
    
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.admin_users = set()  # Should be loaded from secure storage
        self.setup_logging()
    
    def setup_logging(self):
        """Setup security logging"""
        self.logger = logging.getLogger('SecurityManager')
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def generate_token(self, user_id: str, role: str = "user") -> str:
        """Generate JWT token for authentication"""
        if not jwt:
            raise ImportError("PyJWT is required for token generation")
        
        payload = {
            'user_id': user_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return payload if valid"""
        if not jwt:
            raise ImportError("PyJWT is required for token verification")
        
        if not token:
            raise AuthenticationError("Token is required")
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            self.logger.warning(f"Expired token attempted: {token[:20]}...")
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError as e:
            self.logger.warning(f"Invalid token: {e}")
            raise AuthenticationError("Invalid token")
        except Exception as e:
            self.logger.error(f"Unexpected error verifying token: {e}")
            raise AuthenticationError("Token verification failed")
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt with salt"""
        if not bcrypt:
            raise ImportError("bcrypt is required for password hashing")
        
        if not password:
            raise ValidationError("Password cannot be empty")
        
        # Generate salt and hash password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against bcrypt hash"""
        if not bcrypt:
            raise ImportError("bcrypt is required for password verification")
        
        if not password or not hashed:
            return False
        
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception as e:
            self.logger.error(f"Error verifying password: {e}")
            return False
    
    def generate_mfa_secret(self) -> str:
        """Generate a new MFA secret key"""
        if not pyotp:
            raise ImportError("pyotp is required for MFA functionality")
        
        return pyotp.random_base32()
    
    def generate_mfa_qr_code(self, user_id: str, secret: str, issuer: str = "Deerfields Mall") -> str:
        """Generate QR code URL for MFA setup"""
        if not pyotp:
            raise ImportError("pyotp is required for MFA functionality")
        
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            name=user_id,
            issuer_name=issuer
        )
        return provisioning_uri
    
    def verify_otp(self, secret: str, otp: str, window: int = 1) -> bool:
        """Verify OTP code"""
        if not pyotp:
            raise ImportError("pyotp is required for OTP verification")
        
        if not secret or not otp:
            raise ValidationError("Secret and OTP are required")
        
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(otp, valid_window=window)
        except Exception as e:
            self.logger.error(f"Error verifying OTP: {e}")
            raise AuthenticationError("OTP verification failed")
    
    def generate_backup_codes(self, count: int = 10) -> List[str]:
        """Generate backup codes for MFA"""
        codes = []
        for _ in range(count):
            # Generate 8-character alphanumeric codes
            code = secrets.token_hex(4).upper()
            codes.append(code)
        return codes
    
    def verify_backup_code(self, backup_codes: List[str], provided_code: str) -> bool:
        """Verify a backup code and remove it if valid"""
        if not backup_codes or not provided_code:
            raise ValidationError("Backup codes and provided code are required")
        
        if provided_code.upper() in backup_codes:
            backup_codes.remove(provided_code.upper())
            return True
        return False

def require_auth(role: str = None):
    """Decorator to require authentication with proper error handling"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                token = request.headers.get('Authorization')
                if not token:
                    return jsonify({'error': 'No token provided'}), 401
                
                # Remove 'Bearer ' prefix if present
                if token.startswith('Bearer '):
                    token = token[7:]
                
                security_manager = SecurityManager()
                payload = security_manager.verify_token(token)
                
                if role and payload.get('role') != role:
                    return jsonify({'error': 'Insufficient permissions'}), 403
                
                # Add user info to request context
                request.current_user = payload
                return f(*args, **kwargs)
                
            except AuthenticationError as e:
                return jsonify({'error': str(e)}), 401
            except AuthorizationError as e:
                return jsonify({'error': str(e)}), 403
            except Exception as e:
                return jsonify({'error': 'Authentication failed'}), 500
        
        return decorated_function
    return decorator

class SecureDatabase:
    """Improved database class with security features"""
    
    def __init__(self, db_path: str = 'mall_gamification.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.setup_logging()
        self.create_tables()
    
    def setup_logging(self):
        """Setup database logging"""
        self.logger = logging.getLogger('SecureDatabase')
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def create_tables(self):
        """Create security-related tables"""
        try:
            # Security audit log table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS security_audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    action TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    details TEXT
                )
            ''')
            
            # Rate limiting table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS rate_limits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_address TEXT NOT NULL,
                    endpoint TEXT NOT NULL,
                    request_count INTEGER DEFAULT 1,
                    first_request TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_request TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(ip_address, endpoint)
                )
            ''')
            
            # MFA settings table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS mfa_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,
                    mfa_secret TEXT,
                    mfa_enabled BOOLEAN DEFAULT FALSE,
                    backup_codes TEXT,  -- JSON array of backup codes
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # MFA verification attempts table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS mfa_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    attempt_type TEXT NOT NULL,  -- 'otp' or 'backup'
                    success BOOLEAN NOT NULL,
                    ip_address TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Error creating security tables: {e}")
    
    def execute_safe_query(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute parameterized query safely"""
        if not query or not isinstance(query, str):
            raise DatabaseSecurityError("Invalid query")
        
        # Basic SQL injection prevention
        dangerous_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE', 'INSERT', 'UPDATE']
        query_upper = query.upper()
        if any(keyword in query_upper for keyword in dangerous_keywords):
            # Only allow if it's a parameterized query with proper structure
            if not params or '?' not in query:
                raise DatabaseSecurityError("Potentially dangerous query detected")
        
        try:
            cursor = self.conn.execute(query, params)
            self.conn.commit()
            return cursor
        except sqlite3.Error as e:
            self.conn.rollback()
            self.logger.error(f"Database error: {e}")
            raise DatabaseSecurityError(f"Database operation failed: {e}")
        except Exception as e:
            self.conn.rollback()
            self.logger.error(f"Unexpected database error: {e}")
            raise DatabaseSecurityError(f"Database operation failed: {e}")
    
    def update_user_safe(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Safely update user with parameterized queries"""
        if not updates:
            return False
        
        # Whitelist allowed columns
        allowed_columns = {'coins', 'xp', 'level', 'vip_tier', 'login_streak', 'name', 'email', 'phone'}
        filtered_updates = {k: v for k, v in updates.items() if k in allowed_columns}
        
        if not filtered_updates:
            return False
        
        set_clause = ', '.join([f"{k} = ?" for k in filtered_updates.keys()])
        set_clause += ', updated_at = CURRENT_TIMESTAMP'
        
        query = f"UPDATE users SET {set_clause} WHERE user_id = ?"
        params = tuple(filtered_updates.values()) + (user_id,)
        
        try:
            self.execute_safe_query(query, params)
            return True
        except Exception as e:
            self.logger.error(f"Error updating user {user_id}: {e}")
            return False
    
    def log_security_event(self, user_id: str, action: str, details: str = None):
        """Log security events for audit trail"""
        try:
            query = '''
                INSERT INTO security_audit_log (user_id, action, ip_address, user_agent, details)
                VALUES (?, ?, ?, ?, ?)
            '''
            params = (
                user_id,
                action,
                request.remote_addr if request else None,
                request.headers.get('User-Agent') if request else None,
                details
            )
            self.execute_safe_query(query, params)
        except Exception as e:
            self.logger.error(f"Error logging security event: {e}")
    
    def check_rate_limit(self, ip_address: str, endpoint: str, max_requests: int, window_seconds: int) -> bool:
        """Check if request is within rate limits"""
        if not ip_address or not endpoint:
            raise ValidationError("IP address and endpoint are required")
        
        if max_requests <= 0 or window_seconds <= 0:
            raise ValidationError("Invalid rate limit parameters")
        
        try:
            # Clean old entries
            cleanup_query = '''
                DELETE FROM rate_limits 
                WHERE last_request < datetime('now', '-{} seconds')
            '''.format(window_seconds)
            self.conn.execute(cleanup_query)
            
            # Check current rate
            check_query = '''
                SELECT request_count, first_request 
                FROM rate_limits 
                WHERE ip_address = ? AND endpoint = ?
            '''
            cursor = self.conn.execute(check_query, (ip_address, endpoint))
            result = cursor.fetchone()
            
            if result:
                request_count = result['request_count']
                first_request = datetime.fromisoformat(result['first_request'])
                
                if request_count >= max_requests:
                    return False
                
                # Update request count
                update_query = '''
                    UPDATE rate_limits 
                    SET request_count = request_count + 1, last_request = CURRENT_TIMESTAMP
                    WHERE ip_address = ? AND endpoint = ?
                '''
                self.conn.execute(update_query, (ip_address, endpoint))
            else:
                # First request
                insert_query = '''
                    INSERT INTO rate_limits (ip_address, endpoint, request_count)
                    VALUES (?, ?, 1)
                '''
                self.conn.execute(insert_query, (ip_address, endpoint))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            self.logger.error(f"Error checking rate limit: {e}")
            return True  # Allow request if rate limiting fails
    
    def get_mfa_settings(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get MFA settings for a user"""
        try:
            query = "SELECT * FROM mfa_settings WHERE user_id = ?"
            cursor = self.conn.execute(query, (user_id,))
            result = cursor.fetchone()
            
            if result:
                import json
                backup_codes = json.loads(result['backup_codes']) if result['backup_codes'] else []
                return {
                    'user_id': result['user_id'],
                    'mfa_secret': result['mfa_secret'],
                    'mfa_enabled': bool(result['mfa_enabled']),
                    'backup_codes': backup_codes,
                    'created_at': result['created_at'],
                    'updated_at': result['updated_at']
                }
            return None
        except Exception as e:
            self.logger.error(f"Error getting MFA settings for {user_id}: {e}")
            return None
    
    def save_mfa_settings(self, user_id: str, mfa_secret: str, backup_codes: List[str]) -> bool:
        """Save MFA settings for a user"""
        try:
            import json
            backup_codes_json = json.dumps(backup_codes)
            
            query = '''
                INSERT OR REPLACE INTO mfa_settings 
                (user_id, mfa_secret, mfa_enabled, backup_codes, updated_at)
                VALUES (?, ?, TRUE, ?, CURRENT_TIMESTAMP)
            '''
            self.execute_safe_query(query, (user_id, mfa_secret, backup_codes_json))
            return True
        except Exception as e:
            self.logger.error(f"Error saving MFA settings for {user_id}: {e}")
            return False
    
    def enable_mfa(self, user_id: str) -> bool:
        """Enable MFA for a user"""
        try:
            query = "UPDATE mfa_settings SET mfa_enabled = TRUE, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?"
            self.execute_safe_query(query, (user_id,))
            return True
        except Exception as e:
            self.logger.error(f"Error enabling MFA for {user_id}: {e}")
            return False
    
    def disable_mfa(self, user_id: str) -> bool:
        """Disable MFA for a user"""
        try:
            query = "UPDATE mfa_settings SET mfa_enabled = FALSE, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?"
            self.execute_safe_query(query, (user_id,))
            return True
        except Exception as e:
            self.logger.error(f"Error disabling MFA for {user_id}: {e}")
            return False
    
    def update_backup_codes(self, user_id: str, backup_codes: List[str]) -> bool:
        """Update backup codes for a user"""
        try:
            import json
            backup_codes_json = json.dumps(backup_codes)
            
            query = "UPDATE mfa_settings SET backup_codes = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?"
            self.execute_safe_query(query, (backup_codes_json, user_id))
            return True
        except Exception as e:
            self.logger.error(f"Error updating backup codes for {user_id}: {e}")
            return False
    
    def log_mfa_attempt(self, user_id: str, attempt_type: str, success: bool) -> bool:
        """Log MFA verification attempt"""
        try:
            query = '''
                INSERT INTO mfa_attempts (user_id, attempt_type, success, ip_address)
                VALUES (?, ?, ?, ?)
            '''
            params = (user_id, attempt_type, success, request.remote_addr if request else None)
            self.execute_safe_query(query, params)
            return True
        except Exception as e:
            self.logger.error(f"Error logging MFA attempt: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

class RateLimiter:
    """Rate limiting implementation"""
    
    def __init__(self, database: SecureDatabase = None):
        self.database = database or SecureDatabase()
        self.memory_requests = {}  # Fallback in-memory storage
    
    def limit(self, max_requests: int, window_seconds: int):
        """Rate limiting decorator"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                client_ip = request.remote_addr
                endpoint = request.endpoint
                
                # Try database-based rate limiting first
                if self.database:
                    if not self.database.check_rate_limit(client_ip, endpoint, max_requests, window_seconds):
                        return jsonify({'error': 'Rate limit exceeded'}), 429
                else:
                    # Fallback to memory-based rate limiting
                    if not self._check_memory_rate_limit(client_ip, endpoint, max_requests, window_seconds):
                        return jsonify({'error': 'Rate limit exceeded'}), 429
                
                return f(*args, **kwargs)
            
            return decorated_function
        return decorator
    
    def _check_memory_rate_limit(self, client_ip: str, endpoint: str, max_requests: int, window_seconds: int) -> bool:
        """Memory-based rate limiting fallback"""
        key = f"{client_ip}:{endpoint}"
        now = datetime.now()
        
        if key not in self.memory_requests:
            self.memory_requests[key] = []
        
        # Clean old requests
        self.memory_requests[key] = [
            req_time for req_time in self.memory_requests[key]
            if (now - req_time).seconds < window_seconds
        ]
        
        if len(self.memory_requests[key]) >= max_requests:
            return False
        
        self.memory_requests[key].append(now)
        return True

class InputValidator:
    """Input validation utilities with enhanced XSS prevention"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        if not email or not isinstance(email, str):
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        if not phone or not isinstance(phone, str):
            return False
        
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        return len(digits_only) >= 10 and len(digits_only) <= 15
    
    @staticmethod
    def sanitize_string(text: str, max_length: int = 255) -> str:
        """Sanitize string input with enhanced XSS prevention"""
        if not text or not isinstance(text, str):
            return ""
        
        # Remove potentially dangerous characters and patterns
        sanitized = text.strip()
        
        # HTML entity encoding for XSS prevention
        sanitized = sanitized.replace('<', '&lt;').replace('>', '&gt;')
        sanitized = sanitized.replace('"', '&quot;').replace("'", '&#39;')
        sanitized = sanitized.replace('&', '&amp;')
        
        # Remove dangerous patterns
        dangerous_patterns = [
            r'javascript:', r'vbscript:', r'onload=', r'onerror=', r'onclick=',
            r'<script', r'</script>', r'<iframe', r'</iframe>', r'<object',
            r'<embed', r'<form', r'<input', r'<textarea', r'<select'
        ]
        
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # Remove any remaining HTML tags
        sanitized = re.sub(r'<[^>]*>', '', sanitized)
        
        # Limit length
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized
    
    @staticmethod
    def validate_amount(amount: Union[str, float, int]) -> Optional[float]:
        """Validate and convert amount to float"""
        if amount is None:
            return None
        
        try:
            amount_float = float(amount)
            if amount_float <= 0 or amount_float > 100000:  # Reasonable limits
                return None
            return amount_float
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate username format"""
        if not username or not isinstance(username, str):
            return False
        
        # Username should be 3-20 characters, alphanumeric and underscore only
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        """Validate password strength"""
        if not password or not isinstance(password, str):
            return {'valid': False, 'errors': ['Password is required']}
        
        errors = []
        score = 0
        
        # Length check
        if len(password) < 8:
            errors.append('Password must be at least 8 characters long')
        else:
            score += 1
        
        # Complexity checks
        if re.search(r'[a-z]', password):
            score += 1
        else:
            errors.append('Password must contain at least one lowercase letter')
        
        if re.search(r'[A-Z]', password):
            score += 1
        else:
            errors.append('Password must contain at least one uppercase letter')
        
        if re.search(r'\d', password):
            score += 1
        else:
            errors.append('Password must contain at least one digit')
        
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        else:
            errors.append('Password must contain at least one special character')
        
        # Strength assessment
        if score >= 4:
            strength = 'strong'
        elif score >= 3:
            strength = 'medium'
        else:
            strength = 'weak'
        
        return {
            'valid': len(errors) == 0,
            'score': score,
            'strength': strength,
            'errors': errors
        }
    
    @staticmethod
    def sanitize_sql_input(text: str) -> str:
        """Sanitize input for SQL queries (additional layer of protection)"""
        if not text or not isinstance(text, str):
            return ""
        
        # Remove SQL injection patterns
        dangerous_sql = [
            r'--', r'/\*', r'\*/', r'xp_', r'sp_', r'exec', r'execute',
            r'union', r'select', r'insert', r'update', r'delete', r'drop',
            r'create', r'alter', r'truncate', r'declare', r'cast', r'convert'
        ]
        
        sanitized = text
        for pattern in dangerous_sql:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        return sanitized.strip()

# Global instances
security_manager = SecurityManager()
secure_database = SecureDatabase()
rate_limiter = RateLimiter(secure_database)
input_validator = InputValidator()

# Convenience functions
def get_security_manager() -> SecurityManager:
    """Get global security manager instance"""
    return security_manager

def get_secure_database() -> SecureDatabase:
    """Get global secure database instance"""
    return secure_database

def get_rate_limiter() -> RateLimiter:
    """Get global rate limiter instance"""
    return rate_limiter

def get_input_validator() -> InputValidator:
    """Get global input validator instance"""
    return input_validator

def log_security_event(user_id: str, action: str, details: str = None):
    """Log security event using global database"""
    secure_database.log_security_event(user_id, action, details)

def validate_and_sanitize_input(data: Dict[str, Any], required_fields: List[str] = None) -> Dict[str, Any]:
    """Validate and sanitize input data"""
    if not data or not isinstance(data, dict):
        raise ValidationError("Invalid input data")
    
    sanitized_data = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            sanitized_data[key] = input_validator.sanitize_string(value)
        else:
            sanitized_data[key] = value
    
    # Check required fields
    if required_fields:
        for field in required_fields:
            if field not in sanitized_data or not sanitized_data[field]:
                raise ValidationError(f"Required field '{field}' is missing or empty")
    
    return sanitized_data

def create_secure_session(user_id: str, role: str = "user") -> Dict[str, Any]:
    """Create a secure session for a user"""
    try:
        token = security_manager.generate_token(user_id, role)
        return {
            'user_id': user_id,
            'role': role,
            'token': token,
            'expires_at': (datetime.utcnow() + timedelta(hours=24)).isoformat()
        }
    except Exception as e:
        raise AuthenticationError(f"Failed to create session: {e}")

def verify_secure_session(token: str) -> Dict[str, Any]:
    """Verify a secure session token"""
    try:
        payload = security_manager.verify_token(token)
        return payload
    except Exception as e:
        raise AuthenticationError(f"Session verification failed: {e}")

def rate_limit_decorator(max_requests: int = 100, window_seconds: int = 3600):
    """Decorator for rate limiting endpoints"""
    return rate_limiter.limit(max_requests, window_seconds)

def validate_user_input(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate user registration/login input"""
    errors = []
    
    # Validate email
    if 'email' in user_data:
        if not input_validator.validate_email(user_data['email']):
            errors.append("Invalid email format")
    
    # Validate phone
    if 'phone' in user_data:
        if not input_validator.validate_phone(user_data['phone']):
            errors.append("Invalid phone number format")
    
    # Validate username
    if 'username' in user_data:
        if not input_validator.validate_username(user_data['username']):
            errors.append("Username must be 3-20 characters, alphanumeric and underscore only")
    
    # Validate password strength
    if 'password' in user_data:
        password_check = input_validator.validate_password_strength(user_data['password'])
        if not password_check['valid']:
            errors.extend(password_check['errors'])
    
    if errors:
        raise ValidationError(f"Validation errors: {'; '.join(errors)}")
    
    return user_data

def get_security_stats() -> Dict[str, Any]:
    """Get security statistics"""
    try:
        # Get rate limit stats
        cursor = secure_database.conn.execute("""
            SELECT COUNT(*) as total_limits, 
                   COUNT(CASE WHEN request_count >= 10 THEN 1 END) as high_usage
            FROM rate_limits
        """)
        rate_stats = cursor.fetchone()
        
        # Get MFA stats
        cursor = secure_database.conn.execute("""
            SELECT COUNT(*) as total_mfa,
                   COUNT(CASE WHEN mfa_enabled = 1 THEN 1 END) as enabled_mfa
            FROM mfa_settings
        """)
        mfa_stats = cursor.fetchone()
        
        # Get security audit stats
        cursor = secure_database.conn.execute("""
            SELECT COUNT(*) as total_events,
                   COUNT(CASE WHEN action = 'login' THEN 1 END) as login_events,
                   COUNT(CASE WHEN action = 'failed_login' THEN 1 END) as failed_logins
            FROM security_audit_log
        """)
        audit_stats = cursor.fetchone()
        
        return {
            'rate_limiting': {
                'total_limits': rate_stats['total_limits'] if rate_stats else 0,
                'high_usage_count': rate_stats['high_usage'] if rate_stats else 0
            },
            'mfa': {
                'total_users': mfa_stats['total_mfa'] if mfa_stats else 0,
                'enabled_users': mfa_stats['enabled_mfa'] if mfa_stats else 0
            },
            'audit': {
                'total_events': audit_stats['total_events'] if audit_stats else 0,
                'login_events': audit_stats['login_events'] if audit_stats else 0,
                'failed_logins': audit_stats['failed_logins'] if audit_stats else 0
            }
        }
    except Exception as e:
        return {'error': f'Failed to get security stats: {e}'}

def cleanup_expired_data():
    """Clean up expired security data"""
    try:
        # Clean up old rate limits (older than 24 hours)
        secure_database.conn.execute("""
            DELETE FROM rate_limits 
            WHERE last_request < datetime('now', '-24 hours')
        """)
        
        # Clean up old MFA attempts (older than 30 days)
        secure_database.conn.execute("""
            DELETE FROM mfa_attempts 
            WHERE timestamp < datetime('now', '-30 days')
        """)
        
        # Clean up old audit logs (older than 90 days)
        secure_database.conn.execute("""
            DELETE FROM security_audit_log 
            WHERE timestamp < datetime('now', '-90 days')
        """)
        
        secure_database.conn.commit()
        return True
    except Exception as e:
        secure_database.logger.error(f"Error cleaning up expired data: {e}")
        return False 