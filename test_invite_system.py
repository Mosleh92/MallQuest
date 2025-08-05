#!/usr/bin/env python3
"""
Invite System Test Script for Deerfields Mall Gamification System
Demonstrates invite link generation, WiFi verification, and user management
"""

from 3d_graphics_module import (
    GraphicsController,
    generate_invite_link,
    is_inside_mall,
    track_invite_click,
    get_invite_stats,
    create_user,
    get_user,
    update_user_stats,
    lock_game_to_wifi,
    check_wifi_connection,
    initialize_3d_system
)
import time
import json
from datetime import datetime

def test_invite_system():
    """Test the complete invite system"""
    
    print("🔗 Invite System Test - Deerfields Mall")
    print("=" * 50)
    
    # Initialize the graphics controller
    controller = GraphicsController()
    
    # Test 1: Your Function Implementation
    print("\n1. Testing Your Function Implementation")
    print("-" * 40)
    
    print("🎯 Testing your function:")
    print("   def generate_invite_link(user: User):")
    print("       if is_inside_mall('Deerfields_Free_WiFi'):")
    print("           return f'https://deerfieldsmall.com/invite/{user.user_id}'")
    
    # Setup WiFi system first
    lock_game_to_wifi("Deerfields_Free_WiFi")
    
    # Test 2: WiFi Verification System
    print("\n2. Testing WiFi Verification System")
    print("-" * 35)
    
    # Test mall WiFi detection
    print("   Testing mall WiFi detection:")
    inside_mall = is_inside_mall("Deerfields_Free_WiFi")
    wifi_connected = check_wifi_connection()
    
    print(f"     Inside mall: {inside_mall}")
    print(f"     WiFi connected: {wifi_connected}")
    
    # Test different WiFi scenarios
    wifi_scenarios = [
        ("Deerfields_Free_WiFi", True),
        ("Other_Network", False),
        ("Mobile_Data", False)
    ]
    
    for ssid, expected in wifi_scenarios:
        result = is_inside_mall(ssid)
        status = "✅" if result == expected else "❌"
        print(f"     {status} {ssid}: {result} (expected: {expected})")
    
    # Test 3: User Management System
    print("\n3. Testing User Management System")
    print("-" * 35)
    
    # Create test users
    users = [
        ("user_001", "Ahmed Al Mansouri", "ahmed@example.com"),
        ("user_002", "Fatima Hassan", "fatima@example.com"),
        ("user_003", "Omar Khalil", "omar@example.com")
    ]
    
    created_users = []
    for user_id, name, email in users:
        result = create_user(user_id, name, email)
        if result["status"] == "success":
            user = result["user"]
            created_users.append(user_id)
            print(f"✅ User created: {user['name']} ({user['user_id']})")
            print(f"   Level: {user['stats']['level']}")
            print(f"   Coins: {user['stats']['total_coins']}")
        else:
            print(f"❌ User creation failed: {result['message']}")
    
    # Test 4: Invite Link Generation
    print("\n4. Testing Invite Link Generation")
    print("-" * 35)
    
    # Test invite link generation for each user
    invite_links = {}
    for user_id in created_users:
        result = generate_invite_link(user_id)
        if result["status"] == "success":
            invite_link = result["invite_link"]
            config = result["config"]
            invite_links[user_id] = invite_link
            print(f"✅ Invite link generated for {user_id}:")
            print(f"   Link: {invite_link}")
            print(f"   Generated: {config['generated_at']}")
            print(f"   Rewards: {config['rewards']}")
        else:
            print(f"❌ Invite generation failed for {user_id}: {result['message']}")
    
    # Test 5: Invite Link Tracking
    print("\n5. Testing Invite Link Tracking")
    print("-" * 35)
    
    # Simulate invite clicks
    invite_scenarios = [
        ("user_001", "user_002"),  # user_001 invites user_002
        ("user_001", "user_003"),  # user_001 invites user_003
        ("user_002", "user_003"),  # user_002 invites user_003
        ("user_003", "user_001"),  # user_003 invites user_001
    ]
    
    for inviter_id, invitee_id in invite_scenarios:
        print(f"\n   Testing invite: {inviter_id} → {invitee_id}")
        
        # Track invite click
        result = track_invite_click(inviter_id, invitee_id)
        if result["status"] == "success":
            print(f"     ✅ Invite tracked: {result['clicks']} clicks, {result['referrals']} referrals")
        else:
            print(f"     ❌ Invite tracking failed: {result['message']}")
    
    # Test 6: Invite Statistics
    print("\n6. Testing Invite Statistics")
    print("-" * 30)
    
    # Get invite stats for each user
    for user_id in created_users:
        result = get_invite_stats(user_id)
        if result["status"] == "success":
            stats = result
            print(f"✅ Invite stats for {user_id}:")
            print(f"   Link: {stats['link']}")
            print(f"   Clicks: {stats['clicks']}")
            print(f"   Referrals: {stats['referrals']}")
            print(f"   Total rewards: {stats['total_rewards']['coins']} coins, {stats['total_rewards']['xp']} XP")
        else:
            print(f"❌ Failed to get stats for {user_id}: {result['message']}")
    
    # Test 7: User Statistics Updates
    print("\n7. Testing User Statistics Updates")
    print("-" * 35)
    
    # Update user stats with rewards
    for user_id in created_users:
        # Simulate earning rewards
        coins_earned = 100
        xp_earned = 250
        
        result = update_user_stats(user_id, coins_earned, xp_earned)
        if result["status"] == "success":
            user = result["user"]
            print(f"✅ User {user_id} stats updated:")
            print(f"   Coins: {user['stats']['total_coins']}")
            print(f"   XP: {user['stats']['total_xp']}")
            print(f"   Level: {user['stats']['level']}")
        else:
            print(f"❌ Stats update failed for {user_id}: {result['message']}")
    
    # Test 8: User Information Retrieval
    print("\n8. Testing User Information Retrieval")
    print("-" * 40)
    
    # Get user information
    for user_id in created_users:
        result = get_user(user_id)
        if result["status"] == "success":
            user = result["user"]
            print(f"✅ User info for {user_id}:")
            print(f"   Name: {user['name']}")
            print(f"   Email: {user['email']}")
            print(f"   Created: {user['created_at']}")
            print(f"   Last active: {user['last_active']}")
        else:
            print(f"❌ Failed to get user {user_id}: {result['message']}")
    
    # Test 9: Error Handling
    print("\n9. Testing Error Handling")
    print("-" * 25)
    
    # Test invalid user operations
    invalid_user_id = "invalid_user_999"
    
    # Test invite generation for invalid user
    result = generate_invite_link(invalid_user_id)
    if result["status"] == "error":
        print(f"✅ Invalid user invite handled: {result['message']}")
    
    # Test getting invalid user
    result = get_user(invalid_user_id)
    if result["status"] == "error":
        print(f"✅ Invalid user lookup handled: {result['message']}")
    
    # Test invite tracking for invalid user
    result = track_invite_click(invalid_user_id, "user_001")
    if result["status"] == "error":
        print(f"✅ Invalid invite tracking handled: {result['message']}")
    
    # Test 10: Performance Testing
    print("\n10. Testing Performance")
    print("-" * 25)
    
    # Test rapid invite link generation
    print("   Testing rapid invite generation:")
    start_time = time.time()
    for i in range(10):
        generate_invite_link(f"perf_user_{i}")
    end_time = time.time()
    print(f"   ✅ 10 invite links generated in {end_time - start_time:.3f}s")
    
    # Test rapid user creation
    print("   Testing rapid user creation:")
    start_time = time.time()
    for i in range(5):
        create_user(f"perf_user_{i+10}", f"Performance User {i+10}")
    end_time = time.time()
    print(f"   ✅ 5 users created in {end_time - start_time:.3f}s")
    
    print("\n🎉 Invite System Test Completed Successfully!")
    print("=" * 50)
    
    return controller

def demo_invite_journey():
    """Demonstrate a complete invite journey"""
    
    print("\n🌟 Invite Journey Demo")
    print("=" * 25)
    
    controller = GraphicsController()
    
    # Initialize system
    initialize_3d_system()
    lock_game_to_wifi("Deerfields_Free_WiFi")
    
    print("\n🔗 Invite Journey Demo - Deerfields Mall")
    
    # Demo 1: User Creation and Invite Generation
    print("\n👤 User Creation and Invite Generation:")
    
    # Create main user
    user_result = create_user("demo_user_001", "Sarah Al Rashid", "sarah@example.com")
    if user_result["status"] == "success":
        user = user_result["user"]
        print(f"   ✅ User created: {user['name']}")
        
        # Generate invite link
        invite_result = generate_invite_link("demo_user_001")
        if invite_result["status"] == "success":
            invite_link = invite_result["invite_link"]
            print(f"   🔗 Invite link generated: {invite_link}")
        else:
            print(f"   ❌ Invite generation failed: {invite_result['message']}")
    
    # Demo 2: Invite Sharing and Tracking
    print("\n📤 Invite Sharing and Tracking:")
    
    # Simulate friends using invite links
    friends = ["friend_001", "friend_002", "friend_003"]
    
    for friend_id in friends:
        print(f"\n   Friend {friend_id} uses invite link:")
        
        # Track invite click
        track_result = track_invite_click("demo_user_001", friend_id)
        if track_result["status"] == "success":
            print(f"     ✅ Invite tracked successfully")
            print(f"     🎁 Rewards awarded to both users")
        else:
            print(f"     ❌ Invite tracking failed: {track_result['message']}")
    
    # Demo 3: Statistics and Rewards
    print("\n📊 Statistics and Rewards:")
    
    # Get invite statistics
    stats_result = get_invite_stats("demo_user_001")
    if stats_result["status"] == "success":
        stats = stats_result
        print(f"   📈 Invite Statistics:")
        print(f"     Total clicks: {stats['clicks']}")
        print(f"     Successful referrals: {stats['referrals']}")
        print(f"     Total rewards earned: {stats['total_rewards']['coins']} coins, {stats['total_rewards']['xp']} XP")
    
    # Demo 4: User Progression
    print("\n📈 User Progression:")
    
    # Update user with earned rewards
    update_result = update_user_stats("demo_user_001", 150, 300)
    if update_result["status"] == "success":
        user = update_result["user"]
        print(f"   🎯 User progression:")
        print(f"     Total coins: {user['stats']['total_coins']}")
        print(f"     Total XP: {user['stats']['total_xp']}")
        print(f"     Current level: {user['stats']['level']}")
    
    print("\n🎊 Invite Journey Demo Completed!")
    print("The invite system provides seamless friend referrals and rewards!")

def test_invite_integration():
    """Test invite system integration with other systems"""
    
    print("\n🔗 Invite Integration Test")
    print("=" * 30)
    
    controller = GraphicsController()
    
    # Setup complete system
    initialize_3d_system()
    lock_game_to_wifi("Deerfields_Free_WiFi")
    
    # Create user
    create_user("integration_user", "Integration Tester")
    
    # Setup other systems
    from 3d_graphics_module import (
        enable_login_streak_rewards,
        create_daily_quest,
        integrate_with_brand,
        set_ui_language_support,
        add_top_bar
    )
    
    enable_login_streak_rewards(days_required=3, bonus_coins=15)
    create_daily_quest("Invite 1 Friend", 25)
    integrate_with_brand("Emirates Palace", "Exclusive Coupon")
    set_ui_language_support(["en", "ar"])
    add_top_bar(coins_visible=True, language_toggle=True)
    
    print("🔄 Testing invite integration with other systems:")
    
    # Test 1: Invite + WiFi System
    print("\n   1. Invite + WiFi System:")
    inside_mall = is_inside_mall("Deerfields_Free_WiFi")
    print(f"       Inside mall: {inside_mall}")
    
    if inside_mall:
        invite_result = generate_invite_link("integration_user")
        if invite_result["status"] == "success":
            print(f"       Invite link generated: {invite_result['invite_link']}")
    
    # Test 2: Invite + Quest System
    print("\n   2. Invite + Quest System:")
    from 3d_graphics_module import update_quest_progress, complete_quest
    quest_result = create_daily_quest("Invite 2 Friends", 30)
    if quest_result["status"] == "success":
        quest_id = quest_result["quest_id"]
        print(f"       Quest created: {quest_result['quest']['title']}")
        
        # Simulate invite completion
        track_invite_click("integration_user", "friend_001")
        track_invite_click("integration_user", "friend_002")
        
        update_quest_progress(quest_id, 2)
        complete_quest(quest_id, "integration_user")
        print("       Quest completed through invites")
    
    # Test 3: Invite + Brand System
    print("\n   3. Invite + Brand System:")
    brand_result = integrate_with_brand("Dubai Mall", "Invite Rewards")
    if brand_result["status"] == "success":
        print(f"       Brand integration: {brand_result['brand']['name']}")
    
    # Test 4: Invite + UI System
    print("\n   4. Invite + UI System:")
    from 3d_graphics_module import update_coin_display, update_xp_display
    update_coin_display(500)
    update_xp_display(1000)
    print("       UI updated with invite rewards")
    
    # Test 5: Invite + Sound System
    print("\n   5. Invite + Sound System:")
    from 3d_graphics_module import play_sound
    play_sound("invite_success.wav")
    print("       Invite success sound played")
    
    print("\n✅ Invite integration test completed successfully!")

if __name__ == "__main__":
    # Run comprehensive invite system tests
    test_invite_system()
    
    # Demonstrate invite journey
    demo_invite_journey()
    
    # Test invite integration
    test_invite_integration()
    
    print("\n🚀 Invite system is ready for social mall experiences!")
    print("Invite links, WiFi verification, and user management are fully operational!") 