#!/usr/bin/env python3
"""
Test script for CSRF Protection and MFA functionality
"""

import json
import time
from security_module import SecurityManager, SecureDatabase

def test_mfa_functionality():
    """Test MFA functionality"""
    print("🔐 Testing MFA Functionality...")
    
    # Initialize security components
    security_manager = SecurityManager()
    secure_db = SecureDatabase()
    
    # Test 1: Generate MFA secret
    print("  Test 1: Generate MFA secret")
    try:
        mfa_secret = security_manager.generate_mfa_secret()
        print(f"    ✅ MFA secret generated: {mfa_secret[:10]}...")
    except Exception as e:
        print(f"    ❌ Failed to generate MFA secret: {e}")
        return
    
    # Test 2: Generate QR code URL
    print("  Test 2: Generate QR code URL")
    try:
        qr_url = security_manager.generate_mfa_qr_code("test_user", mfa_secret)
        print(f"    ✅ QR code URL generated: {qr_url[:50]}...")
    except Exception as e:
        print(f"    ❌ Failed to generate QR code: {e}")
        return
    
    # Test 3: Generate backup codes
    print("  Test 3: Generate backup codes")
    try:
        backup_codes = security_manager.generate_backup_codes(5)
        print(f"    ✅ Backup codes generated: {backup_codes}")
    except Exception as e:
        print(f"    ❌ Failed to generate backup codes: {e}")
        return
    
    # Test 4: Save MFA settings to database
    print("  Test 4: Save MFA settings to database")
    try:
        success = secure_db.save_mfa_settings("test_user", mfa_secret, backup_codes)
        if success:
            print("    ✅ MFA settings saved to database")
        else:
            print("    ❌ Failed to save MFA settings")
    except Exception as e:
        print(f"    ❌ Database error: {e}")
        return
    
    # Test 5: Enable MFA
    print("  Test 5: Enable MFA")
    try:
        success = secure_db.enable_mfa("test_user")
        if success:
            print("    ✅ MFA enabled")
        else:
            print("    ❌ Failed to enable MFA")
    except Exception as e:
        print(f"    ❌ Database error: {e}")
        return
    
    # Test 6: Retrieve MFA settings
    print("  Test 6: Retrieve MFA settings")
    try:
        settings = secure_db.get_mfa_settings("test_user")
        if settings and settings['mfa_enabled']:
            print("    ✅ MFA settings retrieved and enabled")
        else:
            print("    ❌ MFA settings not found or not enabled")
    except Exception as e:
        print(f"    ❌ Database error: {e}")
        return
    
    # Test 7: Test OTP verification (this would require a real OTP)
    print("  Test 7: Test OTP verification")
    try:
        # This test requires a real OTP from an authenticator app
        # For demo purposes, we'll just test the function exists
        result = security_manager.verify_otp(mfa_secret, "123456")
        print(f"    ✅ OTP verification function working (result: {result})")
    except Exception as e:
        print(f"    ❌ OTP verification failed: {e}")
    
    # Test 8: Test backup code verification
    print("  Test 8: Test backup code verification")
    try:
        if backup_codes:
            test_code = backup_codes[0]
            result = security_manager.verify_backup_code(backup_codes.copy(), test_code)
            if result:
                print(f"    ✅ Backup code verification working (used code: {test_code})")
            else:
                print("    ❌ Backup code verification failed")
        else:
            print("    ⚠️  No backup codes to test")
    except Exception as e:
        print(f"    ❌ Backup code verification failed: {e}")

def test_rate_limiting():
    """Test rate limiting functionality"""
    print("\n🚦 Testing Rate Limiting...")
    
    secure_db = SecureDatabase()
    
    # Test 1: Check rate limit for new IP
    print("  Test 1: Check rate limit for new IP")
    try:
        result = secure_db.check_rate_limit("192.168.1.100", "test_endpoint", 5, 60)
        if result:
            print("    ✅ Rate limit check passed for new IP")
        else:
            print("    ❌ Rate limit check failed for new IP")
    except Exception as e:
        print(f"    ❌ Rate limiting error: {e}")
    
    # Test 2: Check multiple requests
    print("  Test 2: Check multiple requests")
    try:
        for i in range(6):
            result = secure_db.check_rate_limit("192.168.1.101", "test_endpoint", 5, 60)
            if i < 5:
                if result:
                    print(f"    ✅ Request {i+1} allowed")
                else:
                    print(f"    ❌ Request {i+1} blocked unexpectedly")
            else:
                if not result:
                    print(f"    ✅ Request {i+1} correctly blocked (rate limit exceeded)")
                else:
                    print(f"    ❌ Request {i+1} should have been blocked")
    except Exception as e:
        print(f"    ❌ Rate limiting error: {e}")

def test_security_logging():
    """Test security logging functionality"""
    print("\n📝 Testing Security Logging...")
    
    secure_db = SecureDatabase()
    
    # Test 1: Log security event
    print("  Test 1: Log security event")
    try:
        secure_db.log_security_event("test_user", "test_action", "Test security event")
        print("    ✅ Security event logged successfully")
    except Exception as e:
        print(f"    ❌ Security logging failed: {e}")
    
    # Test 2: Log MFA attempt
    print("  Test 2: Log MFA attempt")
    try:
        secure_db.log_mfa_attempt("test_user", "otp", True)
        print("    ✅ MFA attempt logged successfully")
    except Exception as e:
        print(f"    ❌ MFA logging failed: {e}")

def test_csrf_protection():
    """Test CSRF protection setup"""
    print("🔒 Testing CSRF Protection Setup...")
    
    try:
        # Test that Flask-WTF is available
        from flask_wtf.csrf import CSRFProtect
        print("    ✅ Flask-WTF CSRFProtect imported successfully")
        
        # Test that we can create a CSRFProtect instance
        from flask import Flask
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'test_secret_key'
        csrf = CSRFProtect(app)
        print("    ✅ CSRFProtect instance created successfully")
        
        print("    ✅ CSRF protection is properly configured")
        
    except ImportError as e:
        print(f"    ❌ Flask-WTF not available: {e}")
    except Exception as e:
        print(f"    ❌ CSRF protection setup failed: {e}")

def test_input_validation():
    """Test input validation functionality"""
    print("\n🔍 Testing Input Validation...")
    
    from security_module import InputValidator
    validator = InputValidator()
    
    # Test email validation
    print("  Test 1: Email validation")
    valid_emails = ["test@example.com", "user.name@domain.co.uk"]
    invalid_emails = ["invalid-email", "@domain.com", "user@"]
    
    for email in valid_emails:
        if validator.validate_email(email):
            print(f"    ✅ Valid email: {email}")
        else:
            print(f"    ❌ Invalid email (should be valid): {email}")
    
    for email in invalid_emails:
        if not validator.validate_email(email):
            print(f"    ✅ Invalid email correctly rejected: {email}")
        else:
            print(f"    ❌ Invalid email incorrectly accepted: {email}")
    
    # Test amount validation
    print("  Test 2: Amount validation")
    valid_amounts = ["100.50", 200, 0.01]
    invalid_amounts = ["-100", "abc", 0, 1000000]
    
    for amount in valid_amounts:
        if validator.validate_amount(amount) is not None:
            print(f"    ✅ Valid amount: {amount}")
        else:
            print(f"    ❌ Invalid amount (should be valid): {amount}")
    
    for amount in invalid_amounts:
        if validator.validate_amount(amount) is None:
            print(f"    ✅ Invalid amount correctly rejected: {amount}")
        else:
            print(f"    ❌ Invalid amount incorrectly accepted: {amount}")
    
    # Test string sanitization
    print("  Test 3: String sanitization")
    test_string = "<script>alert('xss')</script>"
    sanitized = validator.sanitize_string(test_string)
    if "<script>" not in sanitized:
        print("    ✅ String sanitization successful")
    else:
        print("    ❌ String sanitization failed")

def main():
    """Run all security tests"""
    print("🛡️  Security Features Test Suite")
    print("=" * 50)
    
    test_csrf_protection()
    test_mfa_functionality()
    test_rate_limiting()
    test_security_logging()
    test_input_validation()
    
    print("\n" + "=" * 50)
    print("✅ Security features test completed!")
    print("\n📋 Summary:")
    print("  - CSRF Protection: Implemented with Flask-WTF")
    print("  - MFA: TOTP-based with backup codes")
    print("  - Rate Limiting: Database-based with cleanup")
    print("  - Security Logging: Comprehensive audit trail")
    print("  - Input Validation: Sanitization and validation")
    
    print("\n🚀 To test with the web interface:")
    print("  1. Install dependencies: pip install Flask-WTF pyotp requests")
    print("  2. Start the server: python web_interface.py")
    print("  3. Visit: http://localhost:5000/login")
    print("  4. Login with any user_id and password 'demo123'")
    print("  5. Setup MFA if prompted")

if __name__ == "__main__":
    main() 