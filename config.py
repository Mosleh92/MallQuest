#!/usr/bin/env python3
"""
Configuration management for Deerfields Mall Gamification System
Supports Development, Production, and Testing environments
"""

import os
import secrets
import json
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import json
from dataclasses import dataclass

# Load environment variables from .env file
load_dotenv()

@dataclass
class TenantSettings:
    name: str
    domain: str
    schema: str
    theme: str = 'default'
    logo: str = ''

class BaseConfig:
    """Base configuration class with common settings"""
    TENANT_CONFIG_FILE = os.getenv('TENANT_CONFIG_FILE', 'tenants.json')
    TENANTS: Dict[str, TenantSettings] = {}
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32))
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', '0')
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///mall_gamification.db')
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'mall_gamification.db')
    TENANT_CONFIG_PATH = os.getenv('TENANT_CONFIG_PATH', 'tenants.json')
    
    # Redis Configuration (Optional)
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    REDIS_ENABLED = os.getenv('REDIS_ENABLED', 'True').lower() == 'true'
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_DB = int(os.getenv('REDIS_DB', '0'))

    # Mission Template Cache Configuration
    MISSION_TEMPLATE_CACHE_BACKEND = os.getenv('MISSION_TEMPLATE_CACHE_BACKEND', 'memory')
    MISSION_TEMPLATE_CACHE_TTL = int(os.getenv('MISSION_TEMPLATE_CACHE_TTL', '300'))
    
    # Security Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_hex(32))
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', '3600'))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', '86400'))
    RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', '100'))
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '3600'))
    MFA_ENABLED = os.getenv('MFA_ENABLED', 'True').lower() == 'true'
    CSRF_ENABLED = os.getenv('CSRF_ENABLED', 'True').lower() == 'true'
    
    # Performance Configuration
    CACHE_TTL = int(os.getenv('CACHE_TTL', '300'))
    MAX_CONNECTIONS = int(os.getenv('MAX_CONNECTIONS', '100'))
    ASYNC_WORKERS = int(os.getenv('ASYNC_WORKERS', '4'))
    MEMORY_LIMIT_MB = int(os.getenv('MEMORY_LIMIT_MB', '512'))
    PERFORMANCE_MONITORING = os.getenv('PERFORMANCE_MONITORING', 'True').lower() == 'true'
    
    # Mall Configuration
    MALL_NAME = os.getenv('MALL_NAME', 'Deerfields Mall')
    MALL_LOCATION = os.getenv('MALL_LOCATION', 'Abu Dhabi, UAE')
    SUPPORT_EMAIL = os.getenv('SUPPORT_EMAIL', 'support@deerfields-mall.com')
    SUPPORT_PHONE = os.getenv('SUPPORT_PHONE', '+971-XX-XXX-XXXX')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    SECURITY_LOG_FILE = os.getenv('SECURITY_LOG_FILE', 'logs/security.log')
    PERFORMANCE_LOG_FILE = os.getenv('PERFORMANCE_LOG_FILE', 'logs/performance.log')
    
    # Development Configuration
    TESTING = os.getenv('TESTING', 'False').lower() == 'true'
    TEST_DATABASE_URL = os.getenv('TEST_DATABASE_URL', 'sqlite:///test_mall_gamification.db')
    MOCK_REDIS = os.getenv('MOCK_REDIS', 'False').lower() == 'true'
    
    # Optional Features
    ENABLE_3D_GRAPHICS = os.getenv('ENABLE_3D_GRAPHICS', 'True').lower() == 'true'
    ENABLE_COMPANION_SYSTEM = os.getenv('ENABLE_COMPANION_SYSTEM', 'True').lower() == 'true'
    ENABLE_EVENT_SYSTEM = os.getenv('ENABLE_EVENT_SYSTEM', 'True').lower() == 'true'
    ENABLE_SOCIAL_FEATURES = os.getenv('ENABLE_SOCIAL_FEATURES', 'True').lower() == 'true'
    ENABLE_VIP_SYSTEM = os.getenv('ENABLE_VIP_SYSTEM', 'True').lower() == 'true'
    
    # API Configuration
    API_VERSION = os.getenv('API_VERSION', 'v1')
    API_RATE_LIMIT = int(os.getenv('API_RATE_LIMIT', '100'))
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', '30'))
    
    # Email Configuration (for notifications)
    SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER = os.getenv('SMTP_USER', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    EMAIL_ENABLED = os.getenv('EMAIL_ENABLED', 'False').lower() == 'true'
    
    # File Upload Configuration
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', '10485760'))  # 10MB
    ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', 'jpg,jpeg,png,pdf').split(',')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    
    # Session Configuration
    SESSION_TYPE = os.getenv('SESSION_TYPE', 'filesystem')
    SESSION_FILE_DIR = os.getenv('SESSION_FILE_DIR', 'flask_session')
    PERMANENT_SESSION_LIFETIME = int(os.getenv('PERMANENT_SESSION_LIFETIME', '3600'))
    
    # Monitoring Configuration
    ENABLE_METRICS = os.getenv('ENABLE_METRICS', 'True').lower() == 'true'
    METRICS_PORT = int(os.getenv('METRICS_PORT', '9090'))
    HEALTH_CHECK_INTERVAL = int(os.getenv('HEALTH_CHECK_INTERVAL', '30'))
    
    @classmethod
    def load_tenants(cls) -> Dict[str, TenantSettings]:
        """Load tenant settings from JSON file"""
        try:
            with open(cls.TENANT_CONFIG_FILE, 'r') as f:
                data = json.load(f)
            cls.TENANTS = {k: TenantSettings(**v) for k, v in data.items()}
        except FileNotFoundError:
            cls.TENANTS = {}
        return cls.TENANTS

    @classmethod
    def get_tenant(cls, host: str) -> Optional[TenantSettings]:
        """Retrieve tenant settings by domain"""
        if not cls.TENANTS:
            cls.load_tenants()
        for tenant in cls.TENANTS.values():
            if tenant.domain == host:
                return tenant
        return None

    @classmethod
    def get_database_config(cls, tenant_domain: Optional[str] = None) -> Dict[str, Any]:
        """Get database configuration as dictionary, optionally per-tenant"""
        config = {
            'url': cls.DATABASE_URL,
            'path': cls.DATABASE_PATH,
            'testing': cls.TESTING,
            'test_url': cls.TEST_DATABASE_URL
        }
        if tenant_domain:
            tenant = cls.get_tenant(tenant_domain)
            if tenant:
                config['schema'] = tenant.schema
        return config

    @classmethod
    def get_redis_config(cls) -> Dict[str, Any]:
        """Get Redis configuration as dictionary"""
        return {
            'url': cls.REDIS_URL,
            'enabled': cls.REDIS_ENABLED,
            'host': cls.REDIS_HOST,
            'port': cls.REDIS_PORT,
            'db': cls.REDIS_DB,
            'mock': cls.MOCK_REDIS
        }
    
    @classmethod
    def get_security_config(cls) -> Dict[str, Any]:
        """Get security configuration as dictionary"""
        return {
            'jwt_secret_key': cls.JWT_SECRET_KEY,
            'jwt_access_token_expires': cls.JWT_ACCESS_TOKEN_EXPIRES,
            'jwt_refresh_token_expires': cls.JWT_REFRESH_TOKEN_EXPIRES,
            'rate_limit_requests': cls.RATE_LIMIT_REQUESTS,
            'rate_limit_window': cls.RATE_LIMIT_WINDOW,
            'mfa_enabled': cls.MFA_ENABLED,
            'csrf_enabled': cls.CSRF_ENABLED
        }
    
    @classmethod
    def get_performance_config(cls) -> Dict[str, Any]:
        """Get performance configuration as dictionary"""
        return {
            'cache_ttl': cls.CACHE_TTL,
            'max_connections': cls.MAX_CONNECTIONS,
            'async_workers': cls.ASYNC_WORKERS,
            'memory_limit_mb': cls.MEMORY_LIMIT_MB,
            'performance_monitoring': cls.PERFORMANCE_MONITORING
        }

    @classmethod
    def get_mission_template_cache_config(cls) -> Dict[str, Any]:
        """Get mission template cache configuration"""
        return {
            'backend': cls.MISSION_TEMPLATE_CACHE_BACKEND,
            'ttl': cls.MISSION_TEMPLATE_CACHE_TTL
        }
    
    @classmethod
    def get_logging_config(cls) -> Dict[str, Any]:
        """Get logging configuration as dictionary"""
        return {
            'level': cls.LOG_LEVEL,
            'log_file': cls.LOG_FILE,
            'security_log_file': cls.SECURITY_LOG_FILE,
            'performance_log_file': cls.PERFORMANCE_LOG_FILE
        }
    
    @classmethod
    def get_feature_flags(cls) -> Dict[str, bool]:
        """Get feature flags as dictionary"""
        return {
            '3d_graphics': cls.ENABLE_3D_GRAPHICS,
            'companion_system': cls.ENABLE_COMPANION_SYSTEM,
            'event_system': cls.ENABLE_EVENT_SYSTEM,
            'social_features': cls.ENABLE_SOCIAL_FEATURES,
            'vip_system': cls.ENABLE_VIP_SYSTEM
        }


class TenantManager:
    """Load and manage tenant-specific configuration."""

    _tenants: Dict[str, Any] = {}

    @classmethod
    def _config_path(cls) -> Path:
        return Path(BaseConfig.TENANT_CONFIG_PATH)

    @classmethod
    def load_tenants(cls) -> Dict[str, Any]:
        """Load tenant configuration from JSON file."""
        if not cls._tenants:
            path = cls._config_path()
            if path.exists():
                cls._tenants = json.loads(path.read_text())
            else:
                cls._tenants = {}
        return cls._tenants

    @classmethod
    def get_tenant(cls, domain: str) -> Optional[Dict[str, Any]]:
        """Return configuration for a specific tenant domain."""
        tenants = cls.load_tenants()
        return tenants.get(domain)

    @classmethod
    def add_tenant(cls, domain: str, schema: str, name: str, theme: str = 'default') -> None:
        """Add or update a tenant configuration and persist it."""
        tenants = cls.load_tenants()
        tenants[domain] = {
            'schema': schema,
            'name': name,
            'theme': theme
        }
        cls.save_tenants()

    @classmethod
    def save_tenants(cls) -> None:
        """Persist tenant configuration to JSON file."""
        path = cls._config_path()
        path.write_text(json.dumps(cls._tenants, indent=2))

class DevelopmentConfig(BaseConfig):
    """Development environment configuration"""
    
    DEBUG = True
    FLASK_DEBUG = '1'
    LOG_LEVEL = 'DEBUG'
    
    # Development-specific settings
    TESTING = False
    MOCK_REDIS = True  # Use mock Redis for development
    
    # More verbose logging
    LOG_FILE = 'logs/dev_app.log'
    SECURITY_LOG_FILE = 'logs/dev_security.log'
    PERFORMANCE_LOG_FILE = 'logs/dev_performance.log'
    
    # Development database
    DATABASE_URL = 'sqlite:///dev_mall_gamification.db'
    DATABASE_PATH = 'dev_mall_gamification.db'
    
    # Enable all features for development
    ENABLE_3D_GRAPHICS = True
    ENABLE_COMPANION_SYSTEM = True
    ENABLE_EVENT_SYSTEM = True
    ENABLE_SOCIAL_FEATURES = True
    ENABLE_VIP_SYSTEM = True
    
    # Development performance settings
    CACHE_TTL = 60  # Shorter cache for development
    MAX_CONNECTIONS = 50
    ASYNC_WORKERS = 2
    MEMORY_LIMIT_MB = 256

class ProductionConfig(BaseConfig):
    """Production environment configuration"""
    
    DEBUG = False
    FLASK_DEBUG = '0'
    LOG_LEVEL = 'WARNING'
    
    # Production security settings
    MFA_ENABLED = True
    CSRF_ENABLED = True
    RATE_LIMIT_REQUESTS = 50  # Stricter rate limiting
    RATE_LIMIT_WINDOW = 3600
    
    # Production database (use PostgreSQL in production)
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/mall_gamification')
    
    # Production Redis settings
    REDIS_ENABLED = True
    REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
    
    # Production performance settings
    CACHE_TTL = 1800  # Longer cache for production
    MAX_CONNECTIONS = 200
    ASYNC_WORKERS = 8
    MEMORY_LIMIT_MB = 1024
    
    # Production logging
    LOG_FILE = '/var/log/mall_gamification/app.log'
    SECURITY_LOG_FILE = '/var/log/mall_gamification/security.log'
    PERFORMANCE_LOG_FILE = '/var/log/mall_gamification/performance.log'
    
    # Email enabled for production
    EMAIL_ENABLED = True
    
    # Strict file upload settings
    MAX_FILE_SIZE = 5242880  # 5MB limit for production
    ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'pdf']

class TestingConfig(BaseConfig):
    """Testing environment configuration"""
    
    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    
    # Test database
    DATABASE_URL = 'sqlite:///test_mall_gamification.db'
    DATABASE_PATH = 'test_mall_gamification.db'
    
    # Mock Redis for testing
    REDIS_ENABLED = False
    MOCK_REDIS = True
    
    # Test-specific settings
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing
    MFA_ENABLED = False  # Disable MFA for testing
    
    # Test logging
    LOG_FILE = 'logs/test_app.log'
    SECURITY_LOG_FILE = 'logs/test_security.log'
    PERFORMANCE_LOG_FILE = 'logs/test_performance.log'
    
    # Minimal performance settings for testing
    CACHE_TTL = 30
    MAX_CONNECTIONS = 10
    ASYNC_WORKERS = 1
    MEMORY_LIMIT_MB = 128
    
    # Disable features that might interfere with testing
    ENABLE_3D_GRAPHICS = False
    ENABLE_COMPANION_SYSTEM = False
    ENABLE_EVENT_SYSTEM = False
    ENABLE_SOCIAL_FEATURES = False
    ENABLE_VIP_SYSTEM = False

class StagingConfig(BaseConfig):
    """Staging environment configuration"""
    
    DEBUG = False
    LOG_LEVEL = 'INFO'
    
    # Staging database
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@staging-db/mall_gamification')
    
    # Staging Redis
    REDIS_URL = os.getenv('REDIS_URL', 'redis://staging-redis:6379/0')
    
    # Staging performance settings
    CACHE_TTL = 900
    MAX_CONNECTIONS = 100
    ASYNC_WORKERS = 4
    MEMORY_LIMIT_MB = 512
    
    # Staging logging
    LOG_FILE = '/var/log/mall_gamification/staging_app.log'
    SECURITY_LOG_FILE = '/var/log/mall_gamification/staging_security.log'
    PERFORMANCE_LOG_FILE = '/var/log/mall_gamification/staging_performance.log'

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'default': DevelopmentConfig
}

def get_config(environment: Optional[str] = None) -> BaseConfig:
    """
    Get configuration for the specified environment
    
    Args:
        environment: Environment name (development, production, testing, staging)
        
    Returns:
        Configuration class instance
    """
    if environment is None:
        environment = os.getenv('FLASK_ENV', 'development')
    
    return config.get(environment, config['default'])

def create_directories():
    """Create necessary directories for the application"""
    directories = [
        'logs',
        'uploads',
        'flask_session',
        'temp'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def validate_config(config_obj: BaseConfig) -> bool:
    """
    Validate configuration settings
    
    Args:
        config_obj: Configuration object to validate
        
    Returns:
        True if configuration is valid, False otherwise
    """
    try:
        # Validate required settings
        if not config_obj.SECRET_KEY or config_obj.SECRET_KEY == 'your-secret-key-here-change-this-in-production':
            print("⚠️ Warning: Using default SECRET_KEY. Change this in production!")
        
        if not config_obj.JWT_SECRET_KEY or config_obj.JWT_SECRET_KEY == 'your-jwt-secret-key-change-this-in-production':
            print("⚠️ Warning: Using default JWT_SECRET_KEY. Change this in production!")
        
        # Validate database URL
        if not config_obj.DATABASE_URL:
            print("❌ Error: DATABASE_URL is required")
            return False
        
        # Validate Redis settings if enabled
        if config_obj.REDIS_ENABLED and not config_obj.REDIS_URL:
            print("❌ Error: REDIS_URL is required when REDIS_ENABLED is True")
            return False
        
        # Validate file paths
        if config_obj.LOG_FILE and not os.path.dirname(config_obj.LOG_FILE) == '':
            Path(os.path.dirname(config_obj.LOG_FILE)).mkdir(parents=True, exist_ok=True)
        
        print("✅ Configuration validation passed")
        return True
        
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

def print_config_summary(config_obj: BaseConfig):
    """Print a summary of the current configuration"""
    print("\n" + "="*50)
    print("🔧 Configuration Summary")
    print("="*50)
    print(f"Environment: {config_obj.FLASK_ENV}")
    print(f"Debug Mode: {config_obj.DEBUG}")
    print(f"Testing Mode: {config_obj.TESTING}")
    print(f"Database: {config_obj.DATABASE_URL}")
    print(f"Redis Enabled: {config_obj.REDIS_ENABLED}")
    print(f"Log Level: {config_obj.LOG_LEVEL}")
    print(f"Cache TTL: {config_obj.CACHE_TTL}s")
    print(f"Rate Limit: {config_obj.RATE_LIMIT_REQUESTS} requests per {config_obj.RATE_LIMIT_WINDOW}s")
    print(f"MFA Enabled: {config_obj.MFA_ENABLED}")
    print(f"CSRF Enabled: {config_obj.CSRF_ENABLED}")
    print("="*50)

# Initialize configuration
current_config = get_config()

# Create necessary directories
create_directories()

# Validate configuration
if __name__ == "__main__":
    print_config_summary(current_config)
    validate_config(current_config) 
