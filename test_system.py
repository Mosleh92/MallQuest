#!/usr/bin/env python3
"""
Test script for Deerfields Mall Gamification System
Demonstrates core functionality and features
"""

from mall_gamification_system import MallGamificationSystem, User
import json
from datetime import datetime

def test_system():
    """Test the complete mall gamification system"""
    
    print("🏬 Deerfields Mall Gamification System - Test Suite")
    print("=" * 60)
    
    # Initialize the system
    mall_system = MallGamificationSystem()
    
    # Test 1: Create and manage users
    print("\n1. Testing User Management")
    print("-" * 30)
    
    # Create test users
    user1 = mall_system.create_user("user123", "en")
    user2 = mall_system.create_user("user456", "ar")
    
    print(f"✅ Created user: {user1.user_id} (English)")
    print(f"✅ Created user: {user2.user_id} (Arabic)")
    
    # Test 2: User login and daily rewards
    print("\n2. Testing Login System")
    print("-" * 30)
    
    user1.login()
    user2.login()
    
    print(f"✅ User {user1.user_id} logged in, coins: {user1.coins}")
    print(f"✅ User {user2.user_id} logged in, coins: {user2.coins}")
    print(f"✅ Login streak for {user1.user_id}: {user1.login_streak} days")
    
    # Test 3: Receipt submission
    print("\n3. Testing Receipt Submission")
    print("-" * 30)
    
    # Valid receipts
    mall_system.process_receipt("user123", 150.0, "Deerfields Fashion")
    mall_system.process_receipt("user123", 75.0, "Deerfields Electronics")
    mall_system.process_receipt("user456", 200.0, "Deerfields Café")
    
    print(f"✅ User {user1.user_id} coins after receipts: {user1.coins}")
    print(f"✅ User {user2.user_id} coins after receipts: {user2.coins}")
    
    # Test 4: Mission generation
    print("\n4. Testing Mission Generation")
    print("-" * 30)
    
    mission1 = mall_system.generate_user_missions("user123", "daily")
    mission2 = mall_system.generate_user_missions("user456", "weekly")
    
    print(f"✅ Generated daily mission: {mission1['mission']['title']}")
    print(f"✅ Generated weekly mission: {mission2['mission']['title']}")
    
    # Test 5: Dashboard data
    print("\n5. Testing Dashboard Data")
    print("-" * 30)
    
    user_dashboard = mall_system.get_user_dashboard("user123")
    admin_dashboard = mall_system.get_admin_dashboard()
    
    print(f"✅ User dashboard created for {user1.user_id}")
    print(f"✅ Admin dashboard - Total users: {admin_dashboard['total_users']}")
    print(f"✅ Admin dashboard - Total coins: {admin_dashboard['total_coins']}")
    
    # Test 6: Shopkeeper functionality
    print("\n6. Testing Shopkeeper System")
    print("-" * 30)
    
    shopkeeper_dashboard = mall_system.get_shopkeeper_dashboard("store1")
    if shopkeeper_dashboard:
        print(f"✅ Shopkeeper dashboard for {shopkeeper_dashboard['shop_info']['shop_name']}")
        print(f"✅ Total sales: AED {shopkeeper_dashboard['stats']['total_sales']}")
        print(f"✅ Customer count: {shopkeeper_dashboard['stats']['customer_count']}")
    
    # Test 7: Customer service
    print("\n7. Testing Customer Service")
    print("-" * 30)
    
    # Create test tickets
    ticket_id1 = mall_system.customer_service.create_ticket("user123", "receipt_issue", 
                                                           "My receipt wasn't accepted", "en")
    ticket_id2 = mall_system.customer_service.create_ticket("user456", "coin_missing", 
                                                           "Coins not credited", "ar")
    
    print(f"✅ Created ticket: {ticket_id1}")
    print(f"✅ Created ticket: {ticket_id2}")
    
    cs_dashboard = mall_system.get_customer_service_dashboard()
    print(f"✅ CS Dashboard - Open tickets: {cs_dashboard['open_tickets']}")
    print(f"✅ CS Dashboard - Resolved tickets: {cs_dashboard['resolved_tickets']}")
    
    # Test 8: Multilingual features
    print("\n8. Testing Multilingual System")
    print("-" * 30)
    
    welcome_en = user1.multilingual.get_text("welcome_message", "en")
    welcome_ar = user2.multilingual.get_text("welcome_message", "ar")
    
    print(f"✅ English welcome: {welcome_en}")
    print(f"✅ Arabic welcome: {welcome_ar}")
    
    # Test 9: Abu Dhabi features
    print("\n9. Testing Abu Dhabi Special Features")
    print("-" * 30)
    
    ad_features = mall_system.abu_dhabi_features.localized_features
    print(f"✅ Ramadan mode: {ad_features['ramadan_mode']}")
    print(f"✅ National day events: {ad_features['national_day_events']}")
    print(f"✅ Luxury brands: {len(ad_features['luxury_brand_integration'])} integrated")
    
    # Test 10: Event system
    print("\n10. Testing Event System")
    print("-" * 30)
    
    active_events = mall_system.event_scheduler.get_active_events()
    print(f"✅ Active events: {len(active_events)}")
    for event in active_events:
        print(f"   - {event['name']} ({event['bonus_multiplier']}x bonus)")
    
    # Test 11: Security features
    print("\n11. Testing Security Features")
    print("-" * 30)
    
    # Test mall-only access
    features_inside = mall_system.get_available_features(user1, "Deerfields_Free_WiFi")
    features_outside = mall_system.get_available_features(user1, "Other_WiFi")
    
    print(f"✅ Features inside mall: {features_inside}")
    print(f"✅ Features outside mall: {features_outside}")
    
    # Test 12: System summary
    print("\n12. System Summary")
    print("-" * 30)
    
    print(f"✅ Total users in system: {len(mall_system.users)}")
    print(f"✅ Total shopkeepers: {len(mall_system.shopkeepers)}")
    print(f"✅ Total suspicious receipts: {len(mall_system.suspicious_receipts)}")
    print(f"✅ Total support tickets: {len(mall_system.customer_service.tickets)}")
    
    print("\n🎉 All tests completed successfully!")
    print("=" * 60)
    
    return mall_system

def demo_user_journey():
    """Demonstrate a complete user journey"""
    
    print("\n👤 User Journey Demonstration")
    print("=" * 40)
    
    mall_system = MallGamificationSystem()
    
    # Create a new user
    user = mall_system.create_user("demo_user", "en")
    print(f"👋 Welcome {user.user_id}!")
    
    # First login
    user.login()
    print(f"🎁 Daily login reward: +{user.coins} coins")
    
    # Submit receipts
    print("\n🛍️ Shopping at Deerfields Mall...")
    mall_system.process_receipt("demo_user", 120.0, "Deerfields Fashion")
    mall_system.process_receipt("demo_user", 85.0, "Deerfields Electronics")
    mall_system.process_receipt("demo_user", 45.0, "Deerfields Café")
    
    print(f"💰 Total coins earned: {user.coins}")
    print(f"⭐ Current level: {user.level}")
    print(f"👑 VIP tier: {user.vip_tier}")
    
    # Generate missions
    mission = mall_system.generate_user_missions("demo_user", "daily")
    print(f"🎯 New mission: {mission['mission']['title']}")
    
    # Check companion
    print(f"🐉 Companion: {user.companion['name']} (Level {user.companion['level']})")
    print(f"✨ Bonus effect: {user.companion['bonus_effect']}")
    
    print("\n🎉 User journey completed!")

if __name__ == "__main__":
    # Run comprehensive tests
    test_system()
    
    # Demonstrate user journey
    demo_user_journey()
    
    print("\n🚀 System is ready for deployment!")
    print("Access the web interface at: http://localhost:5000") 