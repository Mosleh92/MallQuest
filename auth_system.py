import jwt
import bcrypt
import secrets
import redis
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Union
from functools import wraps
from flask import request, jsonify
from dataclasses import dataclass, asdict
import re
import logging
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserRole(Enum):
    """User roles within the MallQuest platform."""
    PLAYER = "player"
    ADMIN = "admin"
    SHOPKEEPER = "shopkeeper"
    CUSTOMER_SERVICE = "customer_service"
    MALL_MANAGER = "mall_manager"
    VIP_GOLD = "vip_gold"
    VIP_PLATINUM = "vip_platinum"


class SessionStatus(Enum):
    """Possible states for an authentication session."""
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    SUSPICIOUS = "suspicious"


@dataclass
class SecurityConfig:
    """Security configuration with enterprise-grade defaults."""
    JWT_SECRET_KEY: str = secrets.token_urlsafe(64)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 15
    PASSWORD_MIN_LENGTH: int = 12
    PASSWORD_REQUIRE_SPECIAL: bool = True
    PASSWORD_REQUIRE_NUMBERS: bool = True
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    SESSION_TIMEOUT_MINUTES: int = 120
    MFA_ENABLED: bool = True
    MALL_WIFI_ONLY: bool = True
    ALLOWED_IP_RANGES: Optional[List[str]] = None


@dataclass
class User:
    """Basic user representation."""
    user_id: str
    email: str
    phone: str
    roles: List[UserRole]
    is_active: bool = True
    is_verified: bool = False
    mfa_enabled: bool = False
    mfa_secret: Optional[str] = None
    last_login: Optional[datetime] = None
    failed_login_attempts: int = 0
    account_locked_until: Optional[datetime] = None
    emirates_id: Optional[str] = None
    vip_status: Optional[str] = None
    mall_access_only: bool = True


class MallQuestAuth:
    """
    Enterprise-grade authentication system for MallQuest.
    Designed for high-security mall environment with UAE compliance.
    """

    def __init__(self, config: SecurityConfig, redis_client: redis.Redis):
        self.config = config
        self.redis = redis_client
        self.active_sessions: Dict[str, Dict] = {}

        # UAE Mall-specific security features
        self.mall_ip_ranges = [
            "192.168.100.0/24",  # Mall WiFi range
            "10.0.50.0/24",      # Staff network
        ]

    # ------------------------------------------------------------------
    # Password management
    # ------------------------------------------------------------------
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt(rounds=14)
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

    def validate_password_strength(self, password: str) -> Dict[str, Union[bool, List[str]]]:
        """Validate that a password meets strength requirements."""
        errors: List[str] = []

        if len(password) < self.config.PASSWORD_MIN_LENGTH:
            errors.append(
                f"Password must be at least {self.config.PASSWORD_MIN_LENGTH} characters"
            )

        if self.config.PASSWORD_REQUIRE_UPPERCASE and not re.search(r"[A-Z]", password):
            errors.append("Password must contain uppercase letters")

        if self.config.PASSWORD_REQUIRE_NUMBERS and not re.search(r"\d", password):
            errors.append("Password must contain numbers")

        if self.config.PASSWORD_REQUIRE_SPECIAL and not re.search(r"[!@#$%^&*(),.?\":{}|<>", password):
            errors.append("Password must contain special characters")

        common_passwords = ["password", "123456", "qwerty", "admin", "mallquest"]
        if password.lower() in common_passwords:
            errors.append("Password too common, choose a unique password")

        return {"is_valid": len(errors) == 0, "errors": errors}

    # ------------------------------------------------------------------
    # Validation utilities
    # ------------------------------------------------------------------
    def validate_emirates_id(self, emirates_id: str) -> bool:
        """Validate UAE Emirates ID format."""
        pattern = r"^\d{3}-\d{4}-\d{7}-\d{1}$"
        return bool(re.match(pattern, emirates_id))

    def check_mall_network_access(self, ip_address: str) -> bool:
        """Verify access is from within the mall network."""
        if not self.config.MALL_WIFI_ONLY:
            return True

        import ipaddress

        client_ip = ipaddress.ip_address(ip_address)
        for network_range in self.mall_ip_ranges:
            if client_ip in ipaddress.ip_network(network_range):
                return True

        logger.warning(f"Access denied from non-mall IP: {ip_address}")
        return False

    # ------------------------------------------------------------------
    # Token management
    # ------------------------------------------------------------------
    def generate_tokens(self, user: User) -> Dict[str, str]:
        """Generate JWT access and refresh tokens for a user."""
        now = datetime.utcnow()

        access_payload = {
            "user_id": user.user_id,
            "email": user.email,
            "roles": [role.value for role in user.roles],
            "iat": now,
            "exp": now + timedelta(minutes=self.config.ACCESS_TOKEN_EXPIRE_MINUTES),
            "type": "access",
            "mall_only": user.mall_access_only,
        }

        refresh_payload = {
            "user_id": user.user_id,
            "iat": now,
            "exp": now + timedelta(days=self.config.REFRESH_TOKEN_EXPIRE_DAYS),
            "type": "refresh",
        }

        access_token = jwt.encode(
            access_payload, self.config.JWT_SECRET_KEY, self.config.JWT_ALGORITHM
        )
        refresh_token = jwt.encode(
            refresh_payload, self.config.JWT_SECRET_KEY, self.config.JWT_ALGORITHM
        )

        session_key = f"session:{user.user_id}:{secrets.token_urlsafe(16)}"
        session_data = {
            "user_id": user.user_id,
            "created_at": now.isoformat(),
            "last_activity": now.isoformat(),
            "status": SessionStatus.ACTIVE.value,
            "ip_address": request.remote_addr if request else None,
            "user_agent": request.headers.get("User-Agent") if request else None,
        }

        self.redis.setex(
            session_key,
            timedelta(minutes=self.config.SESSION_TIMEOUT_MINUTES),
            jwt.encode(session_data, self.config.JWT_SECRET_KEY, self.config.JWT_ALGORITHM),
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "session_id": session_key.split(":")[-1],
            "expires_in": self.config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }

    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(
                token, self.config.JWT_SECRET_KEY, algorithms=[self.config.JWT_ALGORITHM]
            )
            if datetime.utcnow() > datetime.fromtimestamp(payload["exp"]):
                logger.warning(f"Token expired for user {payload.get('user_id')}")
                return None
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError as exc:
            logger.error(f"Invalid token: {exc}")
            return None

    # ------------------------------------------------------------------
    # Authentication workflow
    # ------------------------------------------------------------------
    def authenticate_user(
        self,
        email: str,
        password: str,
        ip_address: str,
        mfa_code: Optional[str] = None,
    ) -> Dict:
        """Authenticate a user with security checks."""

        if not self.check_mall_network_access(ip_address):
            return {
                "success": False,
                "error": "access_denied_location",
                "message": "Access restricted to mall premises only",
            }

        rate_limit_key = f"login_attempts:{ip_address}"
        attempts = self.redis.get(rate_limit_key)
        if attempts and int(attempts) >= self.config.MAX_LOGIN_ATTEMPTS:
            return {
                "success": False,
                "error": "rate_limited",
                "message": f"Too many login attempts. Try again in {self.config.LOCKOUT_DURATION_MINUTES} minutes",
            }

        # Simulated user lookup for demonstration purposes
        user = User(
            user_id="demo_user_123",
            email=email,
            phone="+971501234567",
            roles=[UserRole.PLAYER],
            mfa_enabled=True,
        )

        if user.mfa_enabled and not mfa_code:
            return {
                "success": False,
                "error": "mfa_required",
                "message": "Two-factor authentication code required",
            }

        if user.mfa_enabled and mfa_code:
            if not self.verify_mfa_code(user.mfa_secret, mfa_code):
                self.increment_failed_attempts(ip_address, rate_limit_key)
                return {
                    "success": False,
                    "error": "invalid_mfa",
                    "message": "Invalid authentication code",
                }

        tokens = self.generate_tokens(user)
        self.redis.delete(rate_limit_key)
        logger.info(f"Successful login for user {user.email} from {ip_address}")

        return {
            "success": True,
            "user": asdict(user),
            "tokens": tokens,
            "permissions": self.get_user_permissions(user.roles),
        }

    def increment_failed_attempts(self, ip_address: str, rate_limit_key: str) -> None:
        """Increment failed login attempts with rate limiting."""
        pipe = self.redis.pipeline()
        pipe.incr(rate_limit_key)
        pipe.expire(rate_limit_key, self.config.LOCKOUT_DURATION_MINUTES * 60)
        pipe.execute()
        logger.warning(f"Failed login attempt from {ip_address}")

    def verify_mfa_code(self, secret: Optional[str], code: str) -> bool:
        """Verify a TOTP MFA code."""
        if not secret:
            return False
        import pyotp

        totp = pyotp.TOTP(secret)
        return totp.verify(code, valid_window=1)

    def get_user_permissions(self, roles: List[UserRole]) -> List[str]:
        """Get permissions granted to the specified roles."""
        permission_map = {
            UserRole.PLAYER: [
                "deer_care",
                "empire_manage",
                "submit_receipts",
                "view_rewards",
                "participate_events",
            ],
            UserRole.ADMIN: [
                "system_manage",
                "user_manage",
                "analytics_view",
                "event_manage",
                "receipt_verify",
                "security_monitor",
            ],
            UserRole.SHOPKEEPER: [
                "store_manage",
                "promotion_create",
                "sales_analytics",
                "customer_insights",
            ],
            UserRole.CUSTOMER_SERVICE: [
                "ticket_manage",
                "customer_support",
                "issue_resolve",
            ],
            UserRole.VIP_GOLD: [
                "deer_care",
                "empire_manage",
                "vip_rewards",
                "priority_support",
            ],
            UserRole.VIP_PLATINUM: [
                "deer_care",
                "empire_manage",
                "vip_rewards",
                "priority_support",
                "exclusive_events",
                "concierge_service",
            ],
        }

        permissions = set()
        for role in roles:
            permissions.update(permission_map.get(role, []))
        return list(permissions)

    def require_auth(self, required_permissions: Optional[List[str]] = None):
        """Decorator factory for protecting Flask routes."""

        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                token = request.headers.get("Authorization")
                if not token or not token.startswith("Bearer "):
                    return jsonify({"error": "Missing or invalid authorization header"}), 401

                payload = self.verify_token(token.replace("Bearer ", ""))
                if not payload:
                    return jsonify({"error": "Invalid or expired token"}), 401

                if payload.get("mall_only") and not self.check_mall_network_access(request.remote_addr):
                    return jsonify({"error": "Access restricted to mall premises"}), 403

                if required_permissions:
                    user_roles = [UserRole(role) for role in payload.get("roles", [])]
                    user_permissions = self.get_user_permissions(user_roles)
                    if not any(perm in user_permissions for perm in required_permissions):
                        return jsonify({"error": "Insufficient permissions"}), 403

                request.current_user = payload
                return f(*args, **kwargs)

            return decorated_function

        return decorator

    def logout(self, session_id: str, user_id: str) -> bool:
        """Logout a user and revoke the session."""
        session_key = f"session:{user_id}:{session_id}"
        session_data = self.redis.get(session_key)
        if session_data:
            decoded_session = jwt.decode(
                session_data, self.config.JWT_SECRET_KEY, algorithms=[self.config.JWT_ALGORITHM]
            )
            decoded_session["status"] = SessionStatus.REVOKED.value
            updated_session = jwt.encode(
                decoded_session, self.config.JWT_SECRET_KEY, self.config.JWT_ALGORITHM
            )
            self.redis.setex(session_key, timedelta(minutes=5), updated_session)
            logger.info(f"User {user_id} logged out successfully")
            return True
        return False

    def get_active_sessions(self, user_id: str) -> List[Dict]:
        """Retrieve all active sessions for a user."""
        pattern = f"session:{user_id}:*"
        sessions: List[Dict] = []
        for key in self.redis.scan_iter(match=pattern):
            session_data = self.redis.get(key)
            if not session_data:
                continue
            try:
                decoded = jwt.decode(
                    session_data, self.config.JWT_SECRET_KEY, algorithms=[self.config.JWT_ALGORITHM]
                )
                if decoded.get("status") == SessionStatus.ACTIVE.value:
                    sessions.append(
                        {
                            "session_id": key.decode().split(":")[-1],
                            "created_at": decoded.get("created_at"),
                            "last_activity": decoded.get("last_activity"),
                            "ip_address": decoded.get("ip_address"),
                            "user_agent": decoded.get("user_agent"),
                        }
                    )
            except Exception:
                continue
        return sessions


# ----------------------------------------------------------------------
# Flask integration helpers
# ----------------------------------------------------------------------

def create_auth_routes(app, auth_system: MallQuestAuth):
    """Create authentication routes for a Flask app."""

    @app.route("/api/auth/login", methods=["POST"])
    def login():
        data = request.get_json()
        result = auth_system.authenticate_user(
            email=data.get("email"),
            password=data.get("password"),
            ip_address=request.remote_addr,
            mfa_code=data.get("mfa_code"),
        )
        if result["success"]:
            return jsonify(result), 200
        return jsonify({"error": result["error"], "message": result.get("message")}), 400

    @app.route("/api/auth/logout", methods=["POST"])
    @auth_system.require_auth()
    def logout_route():
        data = request.get_json()
        session_id = data.get("session_id")
        user_id = request.current_user["user_id"]
        success = auth_system.logout(session_id, user_id)
        if success:
            return jsonify({"message": "Logged out successfully"}), 200
        return jsonify({"error": "Logout failed"}), 400

    @app.route("/api/auth/sessions", methods=["GET"])
    @auth_system.require_auth()
    def get_sessions_route():
        user_id = request.current_user["user_id"]
        sessions = auth_system.get_active_sessions(user_id)
        return jsonify({"sessions": sessions}), 200


if __name__ == "__main__":
    redis_client = redis.Redis(host="localhost", port=6379, decode_responses=False)
    config = SecurityConfig(MALL_WIFI_ONLY=True, MFA_ENABLED=True, MAX_LOGIN_ATTEMPTS=3)
    auth = MallQuestAuth(config, redis_client)
    result = auth.authenticate_user(
        email="player@deerfields.ae",
        password="SecurePass123!",
        ip_address="192.168.100.50",
        mfa_code="123456",
    )
    print("Authentication Result:", result)
