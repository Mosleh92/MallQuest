#!/usr/bin/env python3
"""
Authentication Integration with Gamification System
Integrates the advanced authentication manager with the mall gamification system
"""

from authentication_manager import (
    AuthenticationManager, 
    UserRole, 
    auth_manager,
    login_user,
    logout_user,
    require_auth,
    require_admin,
    require_player,
    require_shopkeeper,
    require_customer_service
)
from mall_gamification_system import MallGamificationSystem
import json
from datetime import datetime

class AuthenticatedGamificationSystem:
    """
    Enhanced Gamification System with Advanced Authentication
    Integrates authentication with all gamification features
    """
    
    def __init__(self):
        self.gamification_system = MallGamificationSystem()
        self.auth_manager = auth_manager
        
        # User role mappings
        self.role_mappings = {
            'player': UserRole.PLAYER.value,
            'admin': UserRole.ADMIN.value,
            'shopkeeper': UserRole.SHOPKEEPER.value,
            'customer_service': UserRole.CUSTOMER_SERVICE.value
        }
        
        print("🔐 Authenticated Gamification System initialized")
    
    def register_user(self, user_id: str, password: str, role: str = "player", language: str = "en") -> dict:
        """Register a new user with authentication"""
        try:
            # Check if user already exists
            existing_user = self.gamification_system.get_user(user_id)
            if existing_user:
                return {"status": "error", "message": "User already exists"}
            
            # Create user in gamification system
            user = self.gamification_system.create_user(user_id, language)
            
            # Hash password and store (in real implementation, store in database)
            hashed_password = self.auth_manager.hash_password(password)
            
            # Generate initial token
            token = self.auth_manager.generate_token(user_id, role)
            
            return {
                "status": "success",
                "message": "User registered successfully",
                "user_id": user_id,
                "role": role,
                "access_token": token,
                "user_info": {
                    "coins": user.coins,
                    "level": user.level,
                    "vip_tier": user.vip_tier,
                    "language": user.language
                }
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Registration failed: {str(e)}"}
    
    def authenticate_user(self, user_id: str, password: str, ip_address: str = None, user_agent: str = None) -> dict:
        """Authenticate user and return tokens"""
        try:
            # Check if account is locked
            if self.auth_manager.is_account_locked(user_id):
                return {"status": "error", "message": "Account is temporarily locked due to failed attempts"}
            
            # Get user from gamification system
            user = self.gamification_system.get_user(user_id)
            if not user:
                self.auth_manager.record_failed_attempt(user_id)
                return {"status": "error", "message": "User not found"}
            
            # Verify password (in real implementation, verify against stored hash)
            # For demo purposes, we'll use a simple check
            if password != "demo_password":  # Replace with actual password verification
                self.auth_manager.record_failed_attempt(user_id)
                return {"status": "error", "message": "Invalid credentials"}
            
            # Clear failed attempts on successful login
            self.auth_manager.clear_failed_attempts(user_id)
            
            # Perform login in gamification system
            user.login()
            
            # Generate authentication tokens
            login_result = login_user(
                user_id=user_id,
                password=password,
                role="player",  # Default role, can be enhanced
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            return {
                "status": "success",
                "message": "Authentication successful",
                "access_token": login_result['access_token'],
                "refresh_token": login_result['refresh_token'],
                "user_info": {
                    "user_id": user.user_id,
                    "coins": user.coins,
                    "level": user.level,
                    "vip_tier": user.vip_tier,
                    "language": user.language,
                    "login_streak": user.login_streak
                }
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Authentication failed: {str(e)}"}
    
    def process_receipt_authenticated(self, token: str, amount: float, store: str) -> dict:
        """Process receipt with authentication"""
        try:
            # Verify token
            payload = self.auth_manager.verify_token(token)
            user_id = payload['user_id']
            
            # Check rate limiting
            if not self.auth_manager.check_rate_limit(user_id, "receipt_submission"):
                return {"status": "error", "message": "Rate limit exceeded for receipt submissions"}
            
            # Process receipt
            result = self.gamification_system.process_receipt(user_id, amount, store)
            
            # Get updated user info
            user = self.gamification_system.get_user(user_id)
            
            return {
                "status": "success",
                "message": "Receipt processed successfully",
                "coins_earned": int(amount // 10),
                "user_info": {
                    "user_id": user.user_id,
                    "coins": user.coins,
                    "level": user.level,
                    "vip_tier": user.vip_tier
                }
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Receipt processing failed: {str(e)}"}
    
    def get_user_dashboard_authenticated(self, token: str) -> dict:
        """Get user dashboard with authentication"""
        try:
            # Verify token
            payload = self.auth_manager.verify_token(token)
            user_id = payload['user_id']
            
            # Get dashboard data
            dashboard = self.gamification_system.get_user_dashboard(user_id)
            
            if not dashboard:
                return {"status": "error", "message": "User not found"}
            
            return {
                "status": "success",
                "dashboard": dashboard
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Dashboard retrieval failed: {str(e)}"}
    
    def get_admin_dashboard_authenticated(self, token: str) -> dict:
        """Get admin dashboard with authentication"""
        try:
            # Verify token and check admin role
            payload = self.auth_manager.verify_token(token)
            if payload.get('role') != 'admin':
                return {"status": "error", "message": "Admin access required"}
            
            # Get admin dashboard
            dashboard = self.gamification_system.get_admin_dashboard()
            
            return {
                "status": "success",
                "dashboard": dashboard
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Admin dashboard retrieval failed: {str(e)}"}
    
    def get_shopkeeper_dashboard_authenticated(self, token: str, shop_id: str) -> dict:
        """Get shopkeeper dashboard with authentication"""
        try:
            # Verify token and check shopkeeper role
            payload = self.auth_manager.verify_token(token)
            if payload.get('role') != 'shopkeeper':
                return {"status": "error", "message": "Shopkeeper access required"}
            
            # Get shopkeeper dashboard
            dashboard = self.gamification_system.get_shopkeeper_dashboard(shop_id)
            
            if not dashboard:
                return {"status": "error", "message": "Shop not found"}
            
            return {
                "status": "success",
                "dashboard": dashboard
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Shopkeeper dashboard retrieval failed: {str(e)}"}
    
    def generate_missions_authenticated(self, token: str, mission_type: str = "daily") -> dict:
        """Generate missions with authentication"""
        try:
            # Verify token
            payload = self.auth_manager.verify_token(token)
            user_id = payload['user_id']
            
            # Check rate limiting
            if not self.auth_manager.check_rate_limit(user_id, "mission_generation"):
                return {"status": "error", "message": "Rate limit exceeded for mission generation"}
            
            # Generate missions
            mission = self.gamification_system.generate_user_missions(user_id, mission_type)
            
            return {
                "status": "success",
                "mission": mission
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Mission generation failed: {str(e)}"}
    
    def logout_user_authenticated(self, token: str) -> dict:
        """Logout user with token revocation"""
        try:
            # Revoke token
            success = self.auth_manager.revoke_token(token)
            
            if success:
                return {"status": "success", "message": "Logout successful"}
            else:
                return {"status": "error", "message": "Logout failed"}
                
        except Exception as e:
            return {"status": "error", "message": f"Logout failed: {str(e)}"}
    
    def refresh_token_authenticated(self, refresh_token: str) -> dict:
        """Refresh access token"""
        try:
            # Refresh token
            new_access_token = self.auth_manager.refresh_access_token(refresh_token)
            
            return {
                "status": "success",
                "access_token": new_access_token,
                "token_type": "Bearer"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Token refresh failed: {str(e)}"}
    
    def get_security_report_authenticated(self, token: str) -> dict:
        """Get security report with admin authentication"""
        try:
            # Verify token and check admin role
            payload = self.auth_manager.verify_token(token)
            if payload.get('role') != 'admin':
                return {"status": "error", "message": "Admin access required"}
            
            # Get security report
            security_report = self.auth_manager.get_security_stats()
            
            return {
                "status": "success",
                "security_report": security_report
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Security report retrieval failed: {str(e)}"}
    
    def get_user_sessions_authenticated(self, token: str, target_user_id: str = None) -> dict:
        """Get user sessions with admin authentication"""
        try:
            # Verify token and check admin role
            payload = self.auth_manager.verify_token(token)
            if payload.get('role') != 'admin':
                return {"status": "error", "message": "Admin access required"}
            
            # Get sessions for target user or current user
            user_id = target_user_id or payload['user_id']
            sessions = self.auth_manager.get_user_sessions(user_id)
            
            return {
                "status": "success",
                "user_id": user_id,
                "sessions": sessions
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Session retrieval failed: {str(e)}"}
    
    def revoke_user_sessions_authenticated(self, token: str, target_user_id: str) -> dict:
        """Revoke all sessions for a user with admin authentication"""
        try:
            # Verify token and check admin role
            payload = self.auth_manager.verify_token(token)
            if payload.get('role') != 'admin':
                return {"status": "error", "message": "Admin access required"}
            
            # Revoke sessions
            revoked_count = self.auth_manager.revoke_user_sessions(target_user_id)
            
            return {
                "status": "success",
                "message": f"Revoked {revoked_count} sessions for user {target_user_id}",
                "revoked_count": revoked_count
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Session revocation failed: {str(e)}"}

# Global authenticated system instance
authenticated_system = AuthenticatedGamificationSystem()

# Example usage functions
def demo_authentication_flow():
    """Demonstrate complete authentication flow"""
    print("🚀 Authentication Flow Demo")
    print("=" * 50)
    
    # 1. Register a new user
    print("\n1. Registering new user...")
    register_result = authenticated_system.register_user(
        user_id="demo_user_123",
        password="secure_password",
        role="player",
        language="en"
    )
    print(f"Registration: {register_result['status']}")
    
    if register_result['status'] == 'success':
        access_token = register_result['access_token']
        
        # 2. Process a receipt
        print("\n2. Processing receipt...")
        receipt_result = authenticated_system.process_receipt_authenticated(
            token=access_token,
            amount=150.0,
            store="Deerfields Fashion"
        )
        print(f"Receipt processing: {receipt_result['status']}")
        
        # 3. Get user dashboard
        print("\n3. Getting user dashboard...")
        dashboard_result = authenticated_system.get_user_dashboard_authenticated(access_token)
        print(f"Dashboard retrieval: {dashboard_result['status']}")
        
        # 4. Generate missions
        print("\n4. Generating missions...")
        mission_result = authenticated_system.generate_missions_authenticated(access_token)
        print(f"Mission generation: {mission_result['status']}")
        
        # 5. Logout
        print("\n5. Logging out...")
        logout_result = authenticated_system.logout_user_authenticated(access_token)
        print(f"Logout: {logout_result['status']}")
        
        return True
    else:
        print(f"Registration failed: {register_result['message']}")
        return False

def demo_security_features():
    """Demonstrate security features"""
    print("\n🔒 Security Features Demo")
    print("=" * 50)
    
    # Create admin user for security demo
    admin_register = authenticated_system.register_user(
        user_id="admin_demo",
        password="admin_password",
        role="admin",
        language="en"
    )
    
    if admin_register['status'] == 'success':
        admin_token = admin_register['access_token']
        
        # Get security report
        print("\n1. Getting security report...")
        security_result = authenticated_system.get_security_report_authenticated(admin_token)
        print(f"Security report: {security_result['status']}")
        
        if security_result['status'] == 'success':
            print("Security Statistics:")
            print(json.dumps(security_result['security_report'], indent=2))
        
        # Get user sessions
        print("\n2. Getting user sessions...")
        sessions_result = authenticated_system.get_user_sessions_authenticated(admin_token, "demo_user_123")
        print(f"User sessions: {sessions_result['status']}")
        
        return True
    else:
        print(f"Admin registration failed: {admin_register['message']}")
        return False

if __name__ == "__main__":
    # Run authentication demo
    demo_authentication_flow()
    
    # Run security demo
    demo_security_features()
    
    print("\n🎉 Authentication integration demo completed!") 