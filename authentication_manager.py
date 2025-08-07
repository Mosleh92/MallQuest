#!/usr/bin/env python3
"""
Advanced Authentication Manager
Provides comprehensive authentication and authorization for the gamification system
"""

from functools import wraps
import jwt
import hashlib
import secrets
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import logging
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserRole(Enum):
    """User roles enumeration"""
    PLAYER = "player"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
    SHOPKEEPER = "shopkeeper"
    CUSTOMER_SERVICE = "customer_service"
    SYSTEM = "system"

class AuthenticationError(Exception):
    """Custom authentication error"""
    pass

class AuthorizationError(Exception):
    """Custom authorization error"""
    pass

class RateLimitError(Exception):
    """Custom rate limit error"""
    pass

class AuthenticationManager:
    """
    Advanced Authentication Manager
    Handles JWT tokens, role-based access control, rate limiting, and security
    """
    
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or self._generate_secret_key()
        self.token_expiry = timedelta(hours=24)
        self.refresh_token_expiry = timedelta(days=7)
        self.failed_attempts = {}  # Track failed login attempts
        self.rate_limits = {}      # Track rate limiting
        self.blacklisted_tokens = set()  # Track blacklisted tokens
        self.session_store = {}    # Store active sessions
        
        # Security settings
        self.max_failed_attempts = 5
        self.lockout_duration = timedelta(minutes=15)
        self.rate_limit_window = timedelta(minutes=1)
        self.max_requests_per_window = 100
        
        logger.info("AuthenticationManager initialized successfully")
    
    def _generate_secret_key(self) -> str:
        """Generate a secure secret key"""
        return secrets.token_urlsafe(32)
    
    def generate_token(self, user_id: str, role: str, additional_claims: Dict = None) -> str:
        """
        Generate JWT token with user information and role
        
        Args:
            user_id: User identifier
            role: User role (player, admin, shopkeeper, etc.)
            additional_claims: Additional claims to include in token
            
        Returns:
            JWT token string
        """
        try:
            payload = {
                'user_id': user_id,
                'role': role,
                'exp': datetime.utcnow() + self.token_expiry,
                'iat': datetime.utcnow(),
                'jti': secrets.token_urlsafe(16),  # JWT ID for token tracking
                'type': 'access'
            }
            
            if additional_claims:
                payload.update(additional_claims)
            
            token = jwt.encode(payload, self.secret_key, algorithm='HS256')
            
            # Store session information
            self.session_store[payload['jti']] = {
                'user_id': user_id,
                'role': role,
                'created_at': datetime.utcnow(),
                'expires_at': payload['exp'],
                'ip_address': additional_claims.get('ip_address'),
                'user_agent': additional_claims.get('user_agent')
            }
            
            logger.info(f"Token generated for user {user_id} with role {role}")
            return token
            
        except Exception as e:
            logger.error(f"Error generating token: {e}")
            raise AuthenticationError("Failed to generate token")
    
    def generate_refresh_token(self, user_id: str) -> str:
        """Generate refresh token for token renewal"""
        try:
            payload = {
                'user_id': user_id,
                'exp': datetime.utcnow() + self.refresh_token_expiry,
                'iat': datetime.utcnow(),
                'jti': secrets.token_urlsafe(16),
                'type': 'refresh'
            }
            
            token = jwt.encode(payload, self.secret_key, algorithm='HS256')
            logger.info(f"Refresh token generated for user {user_id}")
            return token
            
        except Exception as e:
            logger.error(f"Error generating refresh token: {e}")
            raise AuthenticationError("Failed to generate refresh token")
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify JWT token and return payload
        
        Args:
            token: JWT token to verify
            
        Returns:
            Token payload if valid
            
        Raises:
            AuthenticationError: If token is invalid or expired
        """
        try:
            # Check if token is blacklisted
            if token in self.blacklisted_tokens:
                raise AuthenticationError("Token is blacklisted")
            
            # Decode and verify token
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            
            # Check if token is expired
            if datetime.utcnow() > datetime.fromtimestamp(payload['exp']):
                raise AuthenticationError("Token expired")
            
            # Verify token type
            if payload.get('type') != 'access':
                raise AuthenticationError("Invalid token type")
            
            # Check if session exists
            jti = payload.get('jti')
            if jti not in self.session_store:
                raise AuthenticationError("Session not found")
            
            logger.info(f"Token verified for user {payload['user_id']}")
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            raise AuthenticationError("Token expired")
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            raise AuthenticationError("Invalid token")
        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            raise AuthenticationError("Token verification failed")
    
    def refresh_access_token(self, refresh_token: str) -> str:
        """Refresh access token using refresh token"""
        try:
            # Verify refresh token
            payload = jwt.decode(refresh_token, self.secret_key, algorithms=['HS256'])
            
            if payload.get('type') != 'refresh':
                raise AuthenticationError("Invalid refresh token")
            
            # Generate new access token
            new_token = self.generate_token(
                payload['user_id'], 
                payload.get('role', 'player')
            )
            
            logger.info(f"Access token refreshed for user {payload['user_id']}")
            return new_token
            
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            raise AuthenticationError("Failed to refresh token")
    
    def revoke_token(self, token: str) -> bool:
        """Revoke/blacklist a token"""
        try:
            # Decode token to get JWT ID
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            jti = payload.get('jti')
            
            # Add to blacklist
            self.blacklisted_tokens.add(token)
            
            # Remove from session store
            if jti in self.session_store:
                del self.session_store[jti]
            
            logger.info(f"Token revoked for user {payload.get('user_id')}")
            return True
            
        except Exception as e:
            logger.error(f"Error revoking token: {e}")
            return False
    
    def check_rate_limit(self, user_id: str, action: str = "general") -> bool:
        """Check if user has exceeded rate limits"""
        current_time = datetime.utcnow()
        key = f"{user_id}:{action}"
        
        if key not in self.rate_limits:
            self.rate_limits[key] = []
        
        # Remove old entries outside the window
        window_start = current_time - self.rate_limit_window
        self.rate_limits[key] = [
            timestamp for timestamp in self.rate_limits[key]
            if timestamp > window_start
        ]
        
        # Check if limit exceeded
        if len(self.rate_limits[key]) >= self.max_requests_per_window:
            logger.warning(f"Rate limit exceeded for user {user_id}")
            return False
        
        # Add current request
        self.rate_limits[key].append(current_time)
        return True
    
    def record_failed_attempt(self, user_id: str) -> bool:
        """Record failed login attempt and check if account should be locked"""
        current_time = datetime.utcnow()
        
        if user_id not in self.failed_attempts:
            self.failed_attempts[user_id] = []
        
        # Remove old attempts outside lockout window
        lockout_start = current_time - self.lockout_duration
        self.failed_attempts[user_id] = [
            timestamp for timestamp in self.failed_attempts[user_id]
            if timestamp > lockout_start
        ]
        
        # Add current failed attempt
        self.failed_attempts[user_id].append(current_time)
        
        # Check if account should be locked
        if len(self.failed_attempts[user_id]) >= self.max_failed_attempts:
            logger.warning(f"Account locked for user {user_id} due to failed attempts")
            return False
        
        return True
    
    def is_account_locked(self, user_id: str) -> bool:
        """Check if user account is locked due to failed attempts"""
        if user_id not in self.failed_attempts:
            return False
        
        current_time = datetime.utcnow()
        lockout_start = current_time - self.lockout_duration
        
        # Count recent failed attempts
        recent_attempts = [
            timestamp for timestamp in self.failed_attempts[user_id]
            if timestamp > lockout_start
        ]
        
        return len(recent_attempts) >= self.max_failed_attempts
    
    def clear_failed_attempts(self, user_id: str) -> None:
        """Clear failed attempts for successful login"""
        if user_id in self.failed_attempts:
            del self.failed_attempts[user_id]
            logger.info(f"Failed attempts cleared for user {user_id}")
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256 with salt"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256()
        hash_obj.update((password + salt).encode('utf-8'))
        return f"{salt}${hash_obj.hexdigest()}"
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        try:
            salt, hash_value = hashed_password.split('$')
            hash_obj = hashlib.sha256()
            hash_obj.update((password + salt).encode('utf-8'))
            return hash_obj.hexdigest() == hash_value
        except Exception:
            return False
    
    def get_user_sessions(self, user_id: str) -> List[Dict]:
        """Get all active sessions for a user"""
        sessions = []
        for jti, session_data in self.session_store.items():
            if session_data['user_id'] == user_id:
                sessions.append({
                    'jti': jti,
                    'created_at': session_data['created_at'],
                    'expires_at': session_data['expires_at'],
                    'ip_address': session_data.get('ip_address'),
                    'user_agent': session_data.get('user_agent')
                })
        return sessions
    
    def revoke_user_sessions(self, user_id: str) -> int:
        """Revoke all sessions for a user"""
        revoked_count = 0
        sessions_to_remove = []
        
        for jti, session_data in self.session_store.items():
            if session_data['user_id'] == user_id:
                sessions_to_remove.append(jti)
                revoked_count += 1
        
        for jti in sessions_to_remove:
            del self.session_store[jti]
        
        logger.info(f"Revoked {revoked_count} sessions for user {user_id}")
        return revoked_count
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions and tokens"""
        current_time = datetime.utcnow()
        expired_sessions = []
        
        # Find expired sessions
        for jti, session_data in self.session_store.items():
            if session_data['expires_at'] < current_time:
                expired_sessions.append(jti)
        
        # Remove expired sessions
        for jti in expired_sessions:
            del self.session_store[jti]
        
        logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
        return len(expired_sessions)
    
    def get_security_stats(self) -> Dict[str, Any]:
        """Get security statistics"""
        current_time = datetime.utcnow()
        
        # Count active sessions
        active_sessions = len(self.session_store)
        
        # Count locked accounts
        locked_accounts = sum(
            1 for user_id in self.failed_attempts
            if self.is_account_locked(user_id)
        )
        
        # Count blacklisted tokens
        blacklisted_count = len(self.blacklisted_tokens)
        
        return {
            'active_sessions': active_sessions,
            'locked_accounts': locked_accounts,
            'blacklisted_tokens': blacklisted_count,
            'failed_attempts_tracked': len(self.failed_attempts),
            'rate_limits_tracked': len(self.rate_limits)
        }

# Global authentication manager instance
auth_manager = AuthenticationManager()

def require_auth(role: str = None, rate_limit: bool = True):
    """
    Decorator for requiring authentication and optional role-based authorization
    
    Args:
        role: Required role for access (None for any authenticated user)
        rate_limit: Whether to apply rate limiting
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get token from request (this would be implemented based on your web framework)
            token = _extract_token_from_request()
            
            if not token:
                raise AuthenticationError("No authentication token provided")
            
            # Verify token
            try:
                payload = auth_manager.verify_token(token)
            except AuthenticationError as e:
                raise AuthenticationError(f"Authentication failed: {str(e)}")
            
            # Check rate limiting
            if rate_limit:
                user_id = payload['user_id']
                if not auth_manager.check_rate_limit(user_id, f"api:{f.__name__}"):
                    raise RateLimitError("Rate limit exceeded")
            
            # Check role authorization
            if role and payload.get('role') != role:
                raise AuthorizationError(f"Insufficient permissions. Required role: {role}")
            
            # Add user info to request context
            _set_request_user(payload)
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def require_any_role(*roles: str):
    """Decorator for requiring any of the specified roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = _extract_token_from_request()
            
            if not token:
                raise AuthenticationError("No authentication token provided")
            
            try:
                payload = auth_manager.verify_token(token)
            except AuthenticationError as e:
                raise AuthenticationError(f"Authentication failed: {str(e)}")
            
            user_role = payload.get('role')
            if user_role not in roles:
                raise AuthorizationError(f"Insufficient permissions. Required roles: {', '.join(roles)}")
            
            _set_request_user(payload)
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def require_admin():
    """Decorator for requiring admin role"""
    return require_auth(role=UserRole.ADMIN.value)

def require_super_admin():
    """Decorator for requiring super admin role"""
    return require_auth(role=UserRole.SUPER_ADMIN.value)

def require_player():
    """Decorator for requiring player role"""
    return require_auth(role=UserRole.PLAYER.value)

def require_shopkeeper():
    """Decorator for requiring shopkeeper role"""
    return require_auth(role=UserRole.SHOPKEEPER.value)

def require_customer_service():
    """Decorator for requiring customer service role"""
    return require_auth(role=UserRole.CUSTOMER_SERVICE.value)

# Helper functions (these would be implemented based on your web framework)
def _extract_token_from_request() -> Optional[str]:
    """Extract token from request (implement based on your web framework)"""
    # This is a placeholder - implement based on your web framework
    # For Flask: request.headers.get('Authorization', '').replace('Bearer ', '')
    # For FastAPI: request.headers.get('authorization', '').replace('Bearer ', '')
    return None

def _set_request_user(user_data: Dict[str, Any]) -> None:
    """Set user data in request context (implement based on your web framework)"""
    # This is a placeholder - implement based on your web framework
    # For Flask: g.user = user_data
    # For FastAPI: request.state.user = user_data
    pass

# Example usage functions
def login_user(user_id: str, password: str, role: str, ip_address: str = None, user_agent: str = None) -> Dict[str, str]:
    """Login user and return tokens"""
    try:
        # Check if account is locked
        if auth_manager.is_account_locked(user_id):
            raise AuthenticationError("Account is temporarily locked due to failed attempts")
        
        # Verify password (implement your password verification logic here)
        # if not auth_manager.verify_password(password, stored_hash):
        #     auth_manager.record_failed_attempt(user_id)
        #     raise AuthenticationError("Invalid credentials")
        
        # Clear failed attempts on successful login
        auth_manager.clear_failed_attempts(user_id)
        
        # Generate tokens
        access_token = auth_manager.generate_token(
            user_id, 
            role, 
            additional_claims={
                'ip_address': ip_address,
                'user_agent': user_agent
            }
        )
        refresh_token = auth_manager.generate_refresh_token(user_id)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': int(auth_manager.token_expiry.total_seconds())
        }
        
    except Exception as e:
        logger.error(f"Login failed for user {user_id}: {e}")
        raise

def logout_user(token: str) -> bool:
    """Logout user by revoking token"""
    return auth_manager.revoke_token(token)

def refresh_user_token(refresh_token: str) -> str:
    """Refresh user's access token"""
    return auth_manager.refresh_access_token(refresh_token)

# Security monitoring functions
def get_security_report() -> Dict[str, Any]:
    """Get comprehensive security report"""
    return {
        'stats': auth_manager.get_security_stats(),
        'timestamp': datetime.utcnow().isoformat()
    }

def cleanup_security_data() -> Dict[str, int]:
    """Clean up expired security data"""
    expired_sessions = auth_manager.cleanup_expired_sessions()
    
    return {
        'expired_sessions_cleaned': expired_sessions,
        'timestamp': datetime.utcnow().isoformat()
    } 