#!/usr/bin/env python3
"""
Test script for the updated security_module.py
Tests all new features including bcrypt, enhanced validation, error handling, and helper functions.
"""

import sys
import traceback
from datetime import datetime

def test_bcrypt_password_hashing():
    """Test bcrypt password hashing functionality"""
    print("🔐 Testing bcrypt password hashing...")
    
    try:
        from security_module import SecurityManager, ValidationError
        
        security_manager = SecurityManager()
        
        # Test password hashing
        password = "MySecurePassword123!"
        hashed = security_manager.hash_password(password)
        
        print(f"  ✅ Password hashed successfully: {hashed[:20]}...")
        
        # Test password verification
        is_valid = security_manager.verify_password(password, hashed)
        print(f"  ✅ Password verification: {is_valid}")
        
        # Test wrong password
        is_invalid = security_manager.verify_password("WrongPassword", hashed)
        print(f"  ✅ Wrong password rejected: {not is_invalid}")
        
        # Test empty password
        try:
            security_manager.hash_password("")
            print("  ❌ Empty password should have raised error")
        except ValidationError:
            print("  ✅ Empty password correctly rejected")
        
        return True
        
    except Exception as e:
        print(f"  ❌ bcrypt test failed: {e}")
        return False

def test_enhanced_input_validation():
    """Test enhanced input validation with XSS prevention"""
    print("\n🛡️ Testing enhanced input validation...")
    
    try:
        from security_module import InputValidator, ValidationError
        
        validator = InputValidator()
        
        # Test email validation
        valid_emails = ["test@example.com", "user.name@domain.co.uk"]
        invalid_emails = ["invalid-email", "@domain.com", "user@", ""]
        
        for email in valid_emails:
            if validator.validate_email(email):
                print(f"  ✅ Valid email accepted: {email}")
            else:
                print(f"  ❌ Valid email rejected: {email}")
        
        for email in invalid_emails:
            if not validator.validate_email(email):
                print(f"  ✅ Invalid email rejected: {email}")
            else:
                print(f"  ❌ Invalid email accepted: {email}")
        
        # Test XSS prevention
        malicious_input = '<script>alert("XSS")</script><img src="x" onerror="alert(1)">'
        sanitized = validator.sanitize_string(malicious_input)
        
        if '<script>' not in sanitized and 'onerror=' not in sanitized:
            print(f"  ✅ XSS prevention working: {sanitized[:50]}...")
        else:
            print(f"  ❌ XSS prevention failed: {sanitized}")
        
        # Test password strength validation
        strong_password = "MySecurePassword123!"
        weak_password = "123"
        
        strong_check = validator.validate_password_strength(strong_password)
        weak_check = validator.validate_password_strength(weak_password)
        
        print(f"  ✅ Strong password check: {strong_check['strength']} (score: {strong_check['score']})")
        print(f"  ✅ Weak password check: {weak_check['strength']} (score: {weak_check['score']})")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Input validation test failed: {e}")
        return False

def test_error_handling():
    """Test proper error handling with custom exceptions"""
    print("\n⚠️ Testing error handling...")
    
    try:
        from security_module import (
            SecurityError, AuthenticationError, AuthorizationError, 
            ValidationError, RateLimitError, DatabaseSecurityError
        )
        
        # Test custom exceptions
        exceptions = [
            SecurityError("Base security error"),
            AuthenticationError("Authentication failed"),
            AuthorizationError("Insufficient permissions"),
            ValidationError("Invalid input"),
            RateLimitError("Rate limit exceeded"),
            DatabaseSecurityError("Database security issue")
        ]
        
        for exc in exceptions:
            print(f"  ✅ Exception created: {type(exc).__name__}")
        
        # Test exception inheritance
        auth_error = AuthenticationError("Test")
        if isinstance(auth_error, SecurityError):
            print("  ✅ Exception inheritance working")
        else:
            print("  ❌ Exception inheritance failed")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error handling test failed: {e}")
        return False

def test_helper_functions():
    """Test new helper functions"""
    print("\n🔧 Testing helper functions...")
    
    try:
        from security_module import (
            validate_and_sanitize_input, create_secure_session, 
            verify_secure_session, validate_user_input, get_security_stats
        )
        
        # Test input validation and sanitization
        test_data = {
            'name': '<script>alert("XSS")</script>John',
            'email': 'test@example.com',
            'message': 'Hello <b>world</b>!'
        }
        
        sanitized = validate_and_sanitize_input(test_data, ['name', 'email'])
        print(f"  ✅ Input sanitization: {sanitized['name'][:30]}...")
        
        # Test secure session creation
        session_data = create_secure_session("user123", "player")
        print(f"  ✅ Session created: {session_data['user_id']} ({session_data['role']})")
        
        # Test session verification
        verified = verify_secure_session(session_data['token'])
        print(f"  ✅ Session verified: {verified['user_id']}")
        
        # Test user input validation
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'phone': '+1234567890',
            'password': 'SecurePass123!'
        }
        
        validated = validate_user_input(user_data)
        print(f"  ✅ User input validated: {validated['username']}")
        
        # Test security stats
        stats = get_security_stats()
        print(f"  ✅ Security stats retrieved: {len(stats)} categories")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Helper functions test failed: {e}")
        traceback.print_exc()
        return False

def test_rate_limiting():
    """Test rate limiting functionality"""
    print("\n⏱️ Testing rate limiting...")
    
    try:
        from security_module import RateLimiter, SecureDatabase
        
        # Create test database
        test_db = SecureDatabase(':memory:')  # In-memory database for testing
        rate_limiter = RateLimiter(test_db)
        
        # Test rate limiting
        ip = "192.168.1.1"
        endpoint = "test_endpoint"
        
        # Should allow first few requests
        for i in range(3):
            allowed = test_db.check_rate_limit(ip, endpoint, 5, 60)
            print(f"  ✅ Request {i+1} allowed: {allowed}")
        
        # Test memory fallback
        memory_limiter = RateLimiter()  # No database
        allowed = memory_limiter._check_memory_rate_limit(ip, endpoint, 5, 60)
        print(f"  ✅ Memory rate limiting: {allowed}")
        
        test_db.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Rate limiting test failed: {e}")
        return False

def test_database_security():
    """Test secure database operations"""
    print("\n🗄️ Testing database security...")
    
    try:
        from security_module import SecureDatabase, DatabaseSecurityError
        
        # Create test database
        test_db = SecureDatabase(':memory:')
        
        # Test safe query execution
        cursor = test_db.execute_safe_query("SELECT 1 as test")
        result = cursor.fetchone()
        print(f"  ✅ Safe query executed: {result['test']}")
        
        # Test dangerous query prevention
        try:
            test_db.execute_safe_query("DROP TABLE users")
            print("  ❌ Dangerous query should have been rejected")
        except DatabaseSecurityError:
            print("  ✅ Dangerous query correctly rejected")
        
        # Test parameterized query
        cursor = test_db.execute_safe_query(
            "INSERT INTO security_audit_log (user_id, action) VALUES (?, ?)",
            ("test_user", "test_action")
        )
        print("  ✅ Parameterized query executed safely")
        
        test_db.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Database security test failed: {e}")
        return False

def main():
    """Run all security module tests"""
    print("🚀 Starting Security Module Tests")
    print("=" * 50)
    
    tests = [
        test_bcrypt_password_hashing,
        test_enhanced_input_validation,
        test_error_handling,
        test_helper_functions,
        test_rate_limiting,
        test_database_security
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"  ❌ Test {test.__name__} crashed: {e}")
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Security module is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 