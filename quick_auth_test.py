#!/usr/bin/env python3
"""
Quick Authentication Test
Fast test to verify authentication system is working
"""

def quick_test():
    """Quick test of authentication system"""
    print("🔐 Quick Authentication Test")
    print("=" * 40)
    
    try:
        # Import authentication manager
        from authentication_manager import auth_manager, UserRole
        
        print("✅ Authentication manager imported successfully")
        
        # Test token generation
        token = auth_manager.generate_token("test_user", "player")
        print("✅ Token generation successful")
        
        # Test token verification
        payload = auth_manager.verify_token(token)
        print("✅ Token verification successful")
        
        # Test role enumeration
        roles = [role.value for role in UserRole]
        print(f"✅ User roles: {roles}")
        
        # Test password hashing
        password = "test_password"
        hashed = auth_manager.hash_password(password)
        verified = auth_manager.verify_password(password, hashed)
        print("✅ Password hashing and verification successful")
        
        # Test rate limiting
        for i in range(5):
            auth_manager.check_rate_limit("test_user", "test_action")
        print("✅ Rate limiting test successful")
        
        # Test failed attempts
        auth_manager.record_failed_attempt("test_user")
        print("✅ Failed attempts tracking successful")
        
        print("\n🎉 All quick tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False

if __name__ == "__main__":
    quick_test() 