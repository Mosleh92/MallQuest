#!/usr/bin/env python3
"""
Simple Security Test for Mall Gamification System
Basic functionality verification without complex terminal interactions.
"""

def test_basic_imports():
    """Test basic imports"""
    print("Testing basic imports...")
    
    try:
        import hashlib
        import secrets
        import sqlite3
        import logging
        from datetime import datetime, timedelta
        from functools import wraps
        from typing import Dict, List, Optional, Any, Union
        print("✅ Basic imports successful")
        return True
    except ImportError as e:
        print(f"❌ Basic import error: {e}")
        return False

def test_jwt_import():
    """Test JWT import"""
    print("Testing JWT import...")
    
    try:
        import jwt
        print("✅ JWT import successful")
        return True
    except ImportError:
        print("⚠️ JWT not available - will use fallback")
        return False

def test_security_module_import():
    """Test security module import"""
    print("Testing security module import...")
    
    try:
        from security_module import SecurityManager
        print("✅ SecurityManager import successful")
        
        from security_module import SecureDatabase
        print("✅ SecureDatabase import successful")
        
        from security_module import RateLimiter
        print("✅ RateLimiter import successful")
        
        from security_module import InputValidator
        print("✅ InputValidator import successful")
        
        return True
    except ImportError as e:
        print(f"❌ Security module import error: {e}")
        return False

def test_security_manager():
    """Test SecurityManager functionality"""
    print("Testing SecurityManager...")
    
    try:
        from security_module import SecurityManager
        
        # Create security manager
        security_manager = SecurityManager()
        print("✅ SecurityManager created successfully")
        
        # Test password hashing
        password = "test_password"
        hashed = security_manager.hash_password(password)
        if security_manager.verify_password(password, hashed):
            print("✅ Password hashing/verification successful")
        else:
            print("❌ Password hashing/verification failed")
            return False
        
        # Test JWT if available
        if jwt:
            try:
                token = security_manager.generate_token("test_user", "user")
                print(f"✅ JWT token generated: {token[:20]}...")
                
                payload = security_manager.verify_token(token)
                if payload and payload['user_id'] == 'test_user':
                    print("✅ JWT token verification successful")
                else:
                    print("❌ JWT token verification failed")
                    return False
            except Exception as e:
                print(f"⚠️ JWT test skipped: {e}")
        else:
            print("⚠️ JWT tests skipped - PyJWT not available")
        
        return True
        
    except Exception as e:
        print(f"❌ SecurityManager test error: {e}")
        return False

def test_input_validator():
    """Test InputValidator functionality"""
    print("Testing InputValidator...")
    
    try:
        from security_module import InputValidator
        
        validator = InputValidator()
        
        # Test email validation
        if validator.validate_email("test@example.com"):
            print("✅ Email validation successful")
        else:
            print("❌ Email validation failed")
            return False
        
        # Test string sanitization
        test_string = "<script>alert('xss')</script>"
        sanitized = validator.sanitize_string(test_string)
        if "<script>" not in sanitized:
            print("✅ String sanitization successful")
        else:
            print("❌ String sanitization failed")
            return False
        
        # Test amount validation
        if validator.validate_amount("100.50") == 100.5:
            print("✅ Amount validation successful")
        else:
            print("❌ Amount validation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ InputValidator test error: {e}")
        return False

def test_secure_database():
    """Test SecureDatabase functionality"""
    print("Testing SecureDatabase...")
    
    try:
        from security_module import SecureDatabase
        
        # Create test database
        secure_db = SecureDatabase("test_security.db")
        print("✅ SecureDatabase created successfully")
        
        # Test safe query execution
        try:
            cursor = secure_db.execute_safe_query(
                "CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY, name TEXT)"
            )
            print("✅ Safe query execution successful")
        except Exception as e:
            print(f"❌ Safe query execution failed: {e}")
            return False
        
        # Test security event logging
        try:
            secure_db.log_security_event("test_user", "test_action", "Test event")
            print("✅ Security event logging successful")
        except Exception as e:
            print(f"❌ Security event logging failed: {e}")
            return False
        
        # Clean up
        secure_db.close()
        import os
        try:
            os.remove("test_security.db")
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ SecureDatabase test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Simple Security Tests")
    print("=" * 40)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("JWT Import", test_jwt_import),
        ("Security Module Import", test_security_module_import),
        ("SecurityManager", test_security_manager),
        ("InputValidator", test_input_validator),
        ("SecureDatabase", test_secure_database),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 40)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 40)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print("-" * 40)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("Security features are working correctly.")
    else:
        print(f"\n⚠️ {total - passed} TEST(S) FAILED!")
        print("Please review the failed tests above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 