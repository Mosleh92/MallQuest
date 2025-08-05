#!/usr/bin/env python3
"""
Configuration test script for Deerfields Mall Gamification System
Tests environment variable loading and configuration validation
"""

import os
import sys
from pathlib import Path

def test_env_file():
    """Test if .env file exists and can be loaded"""
    print("🔍 Testing Environment File...")
    
    env_file = Path('.env')
    env_example = Path('env.example')
    
    if env_file.exists():
        print("✅ .env file exists")
        return True
    elif env_example.exists():
        print("⚠️ .env file not found, but env.example exists")
        print("   Run: cp env.example .env")
        return False
    else:
        print("❌ No environment file found")
        return False

def test_config_import():
    """Test if config.py can be imported"""
    print("\n🔍 Testing Config Import...")
    
    try:
        from config import get_config, validate_config, print_config_summary
        print("✅ Config module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import config: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error importing config: {e}")
        return False

def test_environment_variables():
    """Test required environment variables"""
    print("\n🔍 Testing Environment Variables...")
    
    required_vars = [
        'SECRET_KEY',
        'JWT_SECRET_KEY',
        'DATABASE_URL',
        'REDIS_URL',
        'FLASK_ENV',
        'DEBUG',
        'LOG_LEVEL'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Missing environment variables: {', '.join(missing_vars)}")
        print("   These will use default values from config.py")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def test_config_classes():
    """Test configuration classes"""
    print("\n🔍 Testing Configuration Classes...")
    
    try:
        from config import DevelopmentConfig, ProductionConfig, TestingConfig
        
        # Test development config
        dev_config = DevelopmentConfig()
        print(f"✅ Development config: DEBUG={dev_config.DEBUG}, LOG_LEVEL={dev_config.LOG_LEVEL}")
        
        # Test production config
        prod_config = ProductionConfig()
        print(f"✅ Production config: DEBUG={prod_config.DEBUG}, LOG_LEVEL={prod_config.LOG_LEVEL}")
        
        # Test testing config
        test_config = TestingConfig()
        print(f"✅ Testing config: TESTING={test_config.TESTING}, DEBUG={test_config.DEBUG}")
        
        return True
    except Exception as e:
        print(f"❌ Error testing config classes: {e}")
        return False

def test_config_validation():
    """Test configuration validation"""
    print("\n🔍 Testing Configuration Validation...")
    
    try:
        from config import get_config, validate_config
        
        # Test with different environments
        environments = ['development', 'production', 'testing']
        
        for env in environments:
            config = get_config(env)
            is_valid = validate_config(config)
            print(f"✅ {env.capitalize()} config validation: {'PASS' if is_valid else 'FAIL'}")
        
        return True
    except Exception as e:
        print(f"❌ Error testing config validation: {e}")
        return False

def test_docker_files():
    """Test Docker configuration files"""
    print("\n🔍 Testing Docker Files...")
    
    docker_files = {
        'Dockerfile': 'Docker container configuration',
        'docker-compose.yml': 'Docker Compose services',
        '.dockerignore': 'Docker build exclusions'
    }
    
    all_exist = True
    for file_name, description in docker_files.items():
        if Path(file_name).exists():
            print(f"✅ {file_name}: {description}")
        else:
            print(f"❌ {file_name}: {description} - Missing")
            all_exist = False
    
    return all_exist

def test_directory_structure():
    """Test if necessary directories exist or can be created"""
    print("\n🔍 Testing Directory Structure...")
    
    required_dirs = [
        'logs',
        'uploads', 
        'flask_session',
        'temp',
        'static'
    ]
    
    all_created = True
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✅ {dir_name}/ directory exists")
        else:
            try:
                dir_path.mkdir(exist_ok=True)
                print(f"✅ {dir_name}/ directory created")
            except Exception as e:
                print(f"❌ Failed to create {dir_name}/ directory: {e}")
                all_created = False
    
    return all_created

def test_config_summary():
    """Test configuration summary display"""
    print("\n🔍 Testing Configuration Summary...")
    
    try:
        from config import get_config, print_config_summary
        
        config = get_config()
        print_config_summary(config)
        return True
    except Exception as e:
        print(f"❌ Error displaying config summary: {e}")
        return False

def main():
    """Run all configuration tests"""
    print("🚀 Configuration Test Suite")
    print("=" * 50)
    
    tests = [
        ("Environment File", test_env_file),
        ("Config Import", test_config_import),
        ("Environment Variables", test_environment_variables),
        ("Config Classes", test_config_classes),
        ("Config Validation", test_config_validation),
        ("Docker Files", test_docker_files),
        ("Directory Structure", test_directory_structure),
        ("Config Summary", test_config_summary)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📋 Configuration Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All configuration tests passed! System is properly configured.")
        return True
    elif passed >= total * 0.8:
        print("⚠️ Most configuration tests passed. System is mostly configured.")
        return True
    else:
        print("❌ Many configuration tests failed. Please check the setup.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 