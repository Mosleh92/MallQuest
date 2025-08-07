#!/usr/bin/env python3
"""
Comprehensive Test Suite for Advanced Authentication Manager
Tests all authentication and authorization features
"""

import time
import json
from datetime import datetime, timedelta
from authentication_manager import (
    AuthenticationManager,
    UserRole,
    AuthenticationError,
    AuthorizationError,
    RateLimitError,
    auth_manager,
    login_user,
    logout_user,
    refresh_user_token,
    get_security_report,
    cleanup_security_data,
    require_super_admin
)

import authentication_manager

def test_token_generation():
    """Test JWT token generation"""
    print("🧪 Testing Token Generation")
    print("=" * 40)
    
    try:
        # Test basic token generation
        token = auth_manager.generate_token("user123", "player")
        print("✅ Basic token generation successful")
        
        # Test token with additional claims
        token_with_claims = auth_manager.generate_token(
            "user456", 
            "admin", 
            additional_claims={
                'ip_address': '192.168.1.100',
                'user_agent': 'Mozilla/5.0'
            }
        )
        print("✅ Token with additional claims successful")
        
        # Test refresh token generation
        refresh_token = auth_manager.generate_refresh_token("user123")
        print("✅ Refresh token generation successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Token generation failed: {e}")
        return False

def test_token_verification():
    """Test JWT token verification"""
    print("\n🧪 Testing Token Verification")
    print("=" * 40)
    
    try:
        # Generate a token
        token = auth_manager.generate_token("user123", "player")
        
        # Verify the token
        payload = auth_manager.verify_token(token)
        print("✅ Token verification successful")
        
        # Check payload contents
        assert payload['user_id'] == "user123"
        assert payload['role'] == "player"
        assert payload['type'] == "access"
        print("✅ Token payload validation successful")
        
        # Test invalid token
        try:
            auth_manager.verify_token("invalid_token")
            print("❌ Invalid token should have failed")
            return False
        except AuthenticationError:
            print("✅ Invalid token correctly rejected")
        
        return True
        
    except Exception as e:
        print(f"❌ Token verification failed: {e}")
        return False

def test_token_refresh():
    """Test token refresh functionality"""
    print("\n🧪 Testing Token Refresh")
    print("=" * 40)
    
    try:
        # Generate refresh token
        refresh_token = auth_manager.generate_refresh_token("user123")
        
        # Refresh access token
        new_access_token = auth_manager.refresh_access_token(refresh_token)
        print("✅ Token refresh successful")
        
        # Verify new token
        payload = auth_manager.verify_token(new_access_token)
        assert payload['user_id'] == "user123"
        print("✅ Refreshed token verification successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Token refresh failed: {e}")
        return False

def test_token_revocation():
    """Test token revocation"""
    print("\n🧪 Testing Token Revocation")
    print("=" * 40)
    
    try:
        # Generate a token
        token = auth_manager.generate_token("user123", "player")
        
        # Verify token works
        payload = auth_manager.verify_token(token)
        print("✅ Original token verification successful")
        
        # Revoke the token
        revoked = auth_manager.revoke_token(token)
        assert revoked == True
        print("✅ Token revocation successful")
        
        # Try to verify revoked token
        try:
            auth_manager.verify_token(token)
            print("❌ Revoked token should have failed")
            return False
        except AuthenticationError:
            print("✅ Revoked token correctly rejected")
        
        return True
        
    except Exception as e:
        print(f"❌ Token revocation failed: {e}")
        return False

def test_rate_limiting():
    """Test rate limiting functionality"""
    print("\n🧪 Testing Rate Limiting")
    print("=" * 40)
    
    try:
        user_id = "test_user_rate_limit"
        
        # Test rate limit within bounds
        for i in range(50):
            if not auth_manager.check_rate_limit(user_id, "test_action"):
                print(f"❌ Rate limit triggered too early at attempt {i+1}")
                return False
        
        print("✅ Rate limiting within bounds successful")
        
        # Test rate limit exceeded
        exceeded = False
        for i in range(60):
            if not auth_manager.check_rate_limit(user_id, "test_action"):
                exceeded = True
                break
        
        if exceeded:
            print("✅ Rate limit exceeded correctly")
        else:
            print("❌ Rate limit should have been exceeded")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Rate limiting failed: {e}")
        return False

def test_failed_attempts():
    """Test failed login attempts tracking"""
    print("\n🧪 Testing Failed Attempts")
    print("=" * 40)
    
    try:
        user_id = "test_user_failed_attempts"
        
        # Test failed attempts tracking
        for i in range(4):
            auth_manager.record_failed_attempt(user_id)
            assert not auth_manager.is_account_locked(user_id)
        
        print("✅ Failed attempts tracking successful")
        
        # Test account lockout
        auth_manager.record_failed_attempt(user_id)
        assert auth_manager.is_account_locked(user_id)
        print("✅ Account lockout successful")
        
        # Test clearing failed attempts
        auth_manager.clear_failed_attempts(user_id)
        assert not auth_manager.is_account_locked(user_id)
        print("✅ Failed attempts clearing successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed attempts testing failed: {e}")
        return False

def test_password_hashing():
    """Test password hashing and verification"""
    print("\n🧪 Testing Password Hashing")
    print("=" * 40)
    
    try:
        password = "my_secure_password_123"
        
        # Hash password
        hashed = auth_manager.hash_password(password)
        print("✅ Password hashing successful")
        
        # Verify correct password
        assert auth_manager.verify_password(password, hashed)
        print("✅ Correct password verification successful")
        
        # Verify incorrect password
        assert not auth_manager.verify_password("wrong_password", hashed)
        print("✅ Incorrect password rejection successful")
        
        # Test different passwords produce different hashes
        hashed2 = auth_manager.hash_password("different_password")
        assert hashed != hashed2
        print("✅ Different passwords produce different hashes")
        
        return True
        
    except Exception as e:
        print(f"❌ Password hashing failed: {e}")
        return False

def test_session_management():
    """Test session management functionality"""
    print("\n🧪 Testing Session Management")
    print("=" * 40)
    
    try:
        user_id = "test_user_sessions"
        
        # Generate multiple tokens for the same user
        token1 = auth_manager.generate_token(user_id, "player")
        token2 = auth_manager.generate_token(user_id, "player")
        token3 = auth_manager.generate_token(user_id, "player")
        
        # Get user sessions
        sessions = auth_manager.get_user_sessions(user_id)
        assert len(sessions) == 3
        print("✅ Session creation and retrieval successful")
        
        # Revoke all sessions
        revoked_count = auth_manager.revoke_user_sessions(user_id)
        assert revoked_count == 3
        print("✅ Session revocation successful")
        
        # Verify sessions are gone
        sessions_after = auth_manager.get_user_sessions(user_id)
        assert len(sessions_after) == 0
        print("✅ Session cleanup verification successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Session management failed: {e}")
        return False

def test_security_stats():
    """Test security statistics and monitoring"""
    print("\n🧪 Testing Security Statistics")
    print("=" * 40)
    
    try:
        # Get initial stats
        initial_stats = auth_manager.get_security_stats()
        print("✅ Initial security stats retrieved")
        
        # Create some activity
        auth_manager.generate_token("stats_user1", "player")
        auth_manager.generate_token("stats_user2", "admin")
        auth_manager.record_failed_attempt("stats_user3")
        auth_manager.record_failed_attempt("stats_user3")
        
        # Get updated stats
        updated_stats = auth_manager.get_security_stats()
        print("✅ Updated security stats retrieved")
        
        # Verify stats changed
        assert updated_stats['active_sessions'] >= 2
        print("✅ Security stats tracking successful")
        
        # Test cleanup
        cleanup_result = cleanup_security_data()
        print("✅ Security data cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Security stats failed: {e}")
        return False

def test_login_logout_flow():
    """Test complete login/logout flow"""
    print("\n🧪 Testing Login/Logout Flow")
    print("=" * 40)
    
    try:
        # Test login
        login_result = login_user(
            user_id="flow_user",
            password="password123",
            role="player",
            ip_address="192.168.1.100",
            user_agent="Test Browser"
        )
        
        assert 'access_token' in login_result
        assert 'refresh_token' in login_result
        print("✅ Login flow successful")
        
        # Test token refresh
        new_token = refresh_user_token(login_result['refresh_token'])
        print("✅ Token refresh flow successful")
        
        # Test logout
        logout_success = logout_user(login_result['access_token'])
        assert logout_success
        print("✅ Logout flow successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Login/logout flow failed: {e}")
        return False


def test_super_admin_role():
    """Test super admin role enforcement"""
    print("\n🧪 Testing Super Admin Role")
    print("=" * 40)

    try:
        token = auth_manager.generate_token("super1", UserRole.SUPER_ADMIN.value)

        def secured_action():
            return "access_granted"

        original_extract = authentication_manager._extract_token_from_request
        authentication_manager._extract_token_from_request = lambda: token
        authentication_manager._set_request_user = lambda user: None

        protected = require_super_admin()(secured_action)
        assert protected() == "access_granted"
        print("✅ Super admin access granted")

        admin_token = auth_manager.generate_token("admin1", UserRole.ADMIN.value)
        authentication_manager._extract_token_from_request = lambda: admin_token

        try:
            protected()
            print("❌ Admin should not access super admin endpoint")
            authentication_manager._extract_token_from_request = original_extract
            return False
        except AuthorizationError:
            print("✅ Non-super admin access correctly denied")

        authentication_manager._extract_token_from_request = original_extract
        return True

    except Exception as e:
        print(f"❌ Super admin role test failed: {e}")
        return False


def test_error_handling():
    """Test error handling and edge cases"""
    print("\n🧪 Testing Error Handling")
    print("=" * 40)
    
    try:
        # Test expired token handling
        try:
            auth_manager.verify_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidGVzdCIsImV4cCI6MTYwOTQ0NzIwMH0.invalid")
            print("❌ Invalid token should have failed")
            return False
        except AuthenticationError:
            print("✅ Invalid token error handling successful")
        
        # Test blacklisted token
        token = auth_manager.generate_token("test_user", "player")
        auth_manager.revoke_token(token)
        
        try:
            auth_manager.verify_token(token)
            print("❌ Blacklisted token should have failed")
            return False
        except AuthenticationError:
            print("✅ Blacklisted token error handling successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling failed: {e}")
        return False

def test_performance():
    """Test performance under load"""
    print("\n🧪 Testing Performance")
    print("=" * 40)
    
    try:
        start_time = time.time()
        
        # Generate 100 tokens
        tokens = []
        for i in range(100):
            token = auth_manager.generate_token(f"perf_user_{i}", "player")
            tokens.append(token)
        
        generation_time = time.time() - start_time
        print(f"✅ Generated 100 tokens in {generation_time:.3f} seconds")
        
        # Verify all tokens
        start_time = time.time()
        for token in tokens:
            auth_manager.verify_token(token)
        
        verification_time = time.time() - start_time
        print(f"✅ Verified 100 tokens in {verification_time:.3f} seconds")
        
        # Performance benchmarks
        if generation_time < 1.0 and verification_time < 1.0:
            print("✅ Performance benchmarks met")
        else:
            print("⚠️ Performance slower than expected")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def main():
    """Run all authentication tests"""
    print("🚀 Advanced Authentication Manager Test Suite")
    print("=" * 60)
    
    tests = [
        ("Token Generation", test_token_generation),
        ("Token Verification", test_token_verification),
        ("Token Refresh", test_token_refresh),
        ("Token Revocation", test_token_revocation),
        ("Rate Limiting", test_rate_limiting),
        ("Failed Attempts", test_failed_attempts),
        ("Password Hashing", test_password_hashing),
        ("Session Management", test_session_management),
        ("Security Stats", test_security_stats),
        ("Login/Logout Flow", test_login_logout_flow),
        ("Error Handling", test_error_handling),
        ("Performance", test_performance)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 30)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Authentication system is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the implementation.")
    
    # Final security report
    print("\n🔒 Final Security Report")
    print("=" * 30)
    final_stats = get_security_report()
    print(json.dumps(final_stats, indent=2, default=str))

if __name__ == "__main__":
    main() 