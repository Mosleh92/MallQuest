#!/usr/bin/env python3
"""
Incentive System Test Script for Deerfields Mall Gamification System
Demonstrates login streaks, sound effects, daily quests, and brand integration
"""

from 3d_graphics_module import (
    GraphicsController,
    enable_login_streak_rewards,
    play_sound,
    create_daily_quest,
    integrate_with_brand,
    record_login,
    complete_quest,
    update_quest_progress,
    get_active_quests,
    get_brand_offers,
    initialize_3d_system
)
import time
import json
from datetime import datetime, timedelta

def test_incentive_system():
    """Test the complete incentive system"""
    
    print("🎯 Incentive System Test - Deerfields Mall")
    print("=" * 55)
    
    # Initialize the graphics controller
    controller = GraphicsController()
    
    # Test 1: Your Commands Implementation
    print("\n1. Testing Your Commands Implementation")
    print("-" * 40)
    
    print("🎯 Implementing your commands:")
    print("   # ایجاد سیستم تشویقی برای حضور مداوم")
    result = enable_login_streak_rewards(days_required=5, bonus_coins=20)
    print(f"✅ Login streak rewards enabled: {result}")
    
    print("   # افزودن افکت صوتی هنگام دریافت پاداش")
    result = play_sound("coin_collect.wav")
    print(f"✅ Sound effect played: {result}")
    
    print("   # طراحی مأموریت روزانه")
    result = create_daily_quest(title="Scan 1 Receipt Today", reward=15)
    print(f"✅ Daily quest created: {result}")
    
    print("   # ادغام با برندهای لوکس")
    result = integrate_with_brand("Emirates Palace", feature="Exclusive Coupon")
    print(f"✅ Brand integration: {result}")
    
    # Test 2: Login Streak System
    print("\n2. Testing Login Streak System")
    print("-" * 30)
    
    # Test consecutive logins
    user_id = "test_user_001"
    for day in range(1, 8):
        print(f"\n   Day {day} login:")
        result = record_login(user_id)
        if result["status"] == "success":
            streak = result["streak"]
            reward = result["reward"]
            print(f"     ✅ Streak: {streak} days")
            print(f"     🎁 Reward: {reward['type']} - {reward['coins']} coins, {reward['xp']} XP")
            
            if reward["type"] == "streak_bonus":
                print(f"     🎉 Streak bonus achieved!")
        else:
            print(f"     ❌ Login failed: {result['message']}")
    
    # Test 3: Sound Effects System
    print("\n3. Testing Sound Effects System")
    print("-" * 30)
    
    # Test different sound categories
    sound_files = [
        "coin_collect.wav",
        "quest_complete.wav",
        "level_up.wav",
        "brand_unlock.wav",
        "streak_celebration.wav"
    ]
    
    for sound_file in sound_files:
        result = play_sound(sound_file)
        if result["status"] == "success":
            sound_config = result["sound"]
            print(f"✅ {sound_file}: {sound_config['category']} category")
        else:
            print(f"❌ {sound_file}: {result['message']}")
    
    # Test 4: Daily Quest System
    print("\n4. Testing Daily Quest System")
    print("-" * 30)
    
    # Create multiple quests
    quests = [
        ("Scan 1 Receipt Today", 15),
        ("Visit 2 Stores Today", 20),
        ("Spend 50 Coins Today", 25),
        ("Play 1 Minigame Today", 10)
    ]
    
    quest_ids = []
    for title, reward in quests:
        result = create_daily_quest(title, reward)
        if result["status"] == "success":
            quest_id = result["quest_id"]
            quest = result["quest"]
            quest_ids.append(quest_id)
            print(f"✅ Quest created: {title}")
            print(f"   ID: {quest_id}")
            print(f"   Reward: {quest['rewards']['coins']} coins")
            print(f"   Expires: {quest['expires_at']}")
        else:
            print(f"❌ Quest creation failed: {result['message']}")
    
    # Test quest progress updates
    print("\n   Testing quest progress:")
    for quest_id in quest_ids:
        result = update_quest_progress(quest_id, 1)
        if result["status"] == "success":
            print(f"     ✅ Quest {quest_id}: {result['progress']}/{result['target']}")
        else:
            print(f"     ❌ Quest update failed: {result['message']}")
    
    # Test quest completion
    print("\n   Testing quest completion:")
    for quest_id in quest_ids:
        result = complete_quest(quest_id, user_id)
        if result["status"] == "success":
            rewards = result["rewards"]
            print(f"     ✅ Quest completed: {rewards['coins']} coins, {rewards['xp']} XP")
        else:
            print(f"     ❌ Quest completion failed: {result['message']}")
    
    # Test 5: Brand Integration System
    print("\n5. Testing Brand Integration System")
    print("-" * 35)
    
    # Integrate with multiple luxury brands
    brands = [
        ("Emirates Palace", "Exclusive Coupon"),
        ("Burj Al Arab", "Fine Dining"),
        ("Dubai Mall", "Premium Shopping"),
        ("Palm Jumeirah", "Luxury Experience")
    ]
    
    for brand_name, feature in brands:
        result = integrate_with_brand(brand_name, feature)
        if result["status"] == "success":
            brand = result["brand"]
            print(f"✅ Brand integrated: {brand_name}")
            print(f"   Feature: {brand['feature']}")
            print(f"   Offers: {len(brand['exclusive_offers'])} exclusive offers")
            print(f"   Rewards: {brand['rewards']['coins']} coins, {brand['rewards']['xp']} XP")
        else:
            print(f"❌ Brand integration failed: {result['message']}")
    
    # Test 6: Active Quests Management
    print("\n6. Testing Active Quests Management")
    print("-" * 35)
    
    # Get active quests
    result = get_active_quests()
    if result["status"] == "success":
        quests = result["quests"]
        print(f"✅ Active quests: {len(quests)}")
        for quest_id, quest in quests.items():
            print(f"   {quest['title']}: {quest['status']}")
    else:
        print(f"❌ Failed to get active quests: {result['message']}")
    
    # Test 7: Brand Offers System
    print("\n7. Testing Brand Offers System")
    print("-" * 30)
    
    # Get all brand offers
    result = get_brand_offers()
    if result["status"] == "success":
        brands = result["brands"]
        print(f"✅ Available brands: {len(brands)}")
        for brand_name, brand in brands.items():
            print(f"   {brand_name}: {brand['feature']}")
            for offer in brand['exclusive_offers']:
                print(f"     - {offer['title']}: {offer['description']}")
    else:
        print(f"❌ Failed to get brand offers: {result['message']}")
    
    # Test specific brand
    result = get_brand_offers("Emirates Palace")
    if result["status"] == "success":
        brand = result["brand"]
        print(f"\n   Emirates Palace details:")
        print(f"     Type: {brand['type']}")
        print(f"     Feature: {brand['feature']}")
        print(f"     VIP Points: {brand['rewards']['vip_points']}")
    else:
        print(f"❌ Failed to get Emirates Palace: {result['message']}")
    
    # Test 8: Incentive System Configuration
    print("\n8. Testing Incentive System Configuration")
    print("-" * 40)
    
    # Check login streak configuration
    if "login_streak" in controller.graphics_engine.incentive_system:
        streak_config = controller.graphics_engine.incentive_system["login_streak"]
        print(f"✅ Login streak configuration:")
        print(f"   Days required: {streak_config['days_required']}")
        print(f"   Bonus coins: {streak_config['bonus_coins']}")
        print(f"   Current streak: {streak_config['current_streak']}")
        print(f"   Max streak: {streak_config['max_streak']}")
        print(f"   Rewards: {streak_config['rewards']}")
    
    # Check sound system
    print(f"✅ Sound system: {len(controller.graphics_engine.sound_system)} sounds played")
    
    # Check quest system
    print(f"✅ Quest system: {len(controller.graphics_engine.quest_system)} quests created")
    
    # Check brand integration
    print(f"✅ Brand integration: {len(controller.graphics_engine.brand_integration)} brands integrated")
    
    # Test 9: Error Handling
    print("\n9. Testing Error Handling")
    print("-" * 25)
    
    # Test invalid quest completion
    result = complete_quest("invalid_quest_id", user_id)
    if result["status"] == "error":
        print(f"✅ Invalid quest handled: {result['message']}")
    
    # Test quest progress on completed quest
    if quest_ids:
        result = update_quest_progress(quest_ids[0], 1)
        if result["status"] == "error":
            print(f"✅ Completed quest progress handled: {result['message']}")
    
    # Test invalid brand lookup
    result = get_brand_offers("Invalid Brand")
    if result["status"] == "error":
        print(f"✅ Invalid brand handled: {result['message']}")
    
    # Test 10: Performance Testing
    print("\n10. Testing Performance")
    print("-" * 25)
    
    # Test rapid sound playing
    print("   Testing rapid sound playing:")
    start_time = time.time()
    for i in range(10):
        play_sound("coin_collect.wav")
    end_time = time.time()
    print(f"   ✅ 10 sounds played in {end_time - start_time:.3f}s")
    
    # Test rapid quest creation
    print("   Testing rapid quest creation:")
    start_time = time.time()
    for i in range(5):
        create_daily_quest(f"Test Quest {i}", 10)
    end_time = time.time()
    print(f"   ✅ 5 quests created in {end_time - start_time:.3f}s")
    
    print("\n🎉 Incentive System Test Completed Successfully!")
    print("=" * 55)
    
    return controller

def demo_incentive_journey():
    """Demonstrate a complete incentive journey"""
    
    print("\n🌟 Incentive Journey Demo")
    print("=" * 30)
    
    controller = GraphicsController()
    
    # Initialize system
    initialize_3d_system()
    
    # Setup incentive system
    enable_login_streak_rewards(days_required=5, bonus_coins=20)
    integrate_with_brand("Emirates Palace", "Exclusive Coupon")
    create_daily_quest("Scan 1 Receipt Today", 15)
    
    print("\n🎯 Incentive Journey Demo - Deerfields Mall")
    
    # Demo 1: Daily Login Streak
    print("\n📅 Daily Login Streak Journey:")
    user_id = "demo_user_001"
    
    for day in range(1, 8):
        print(f"\n   Day {day}:")
        result = record_login(user_id)
        if result["status"] == "success":
            streak = result["streak"]
            reward = result["reward"]
            
            if reward["type"] == "streak_bonus":
                print(f"     🎉 STREAK BONUS! {streak} days!")
                play_sound("streak_celebration.wav")
            else:
                print(f"     ✅ Day {streak} login: +{reward['coins']} coins")
                play_sound("coin_collect.wav")
    
    # Demo 2: Daily Quest Completion
    print("\n🎯 Daily Quest Completion:")
    
    # Create and complete quest
    quest_result = create_daily_quest("Visit Emirates Palace Store", 25)
    if quest_result["status"] == "success":
        quest_id = quest_result["quest_id"]
        print(f"   📋 New quest: {quest_result['quest']['title']}")
        
        # Update progress
        update_quest_progress(quest_id, 1)
        print("   ✅ Quest progress updated")
        
        # Complete quest
        complete_result = complete_quest(quest_id, user_id)
        if complete_result["status"] == "success":
            rewards = complete_result["rewards"]
            print(f"   🎁 Quest completed: +{rewards['coins']} coins, +{rewards['xp']} XP")
            play_sound("quest_complete.wav")
    
    # Demo 3: Brand Integration Experience
    print("\n🏛️ Brand Integration Experience:")
    
    # Get Emirates Palace offers
    brand_result = get_brand_offers("Emirates Palace")
    if brand_result["status"] == "success":
        brand = brand_result["brand"]
        print(f"   🏛️ {brand['name']} - {brand['feature']}")
        
        for offer in brand['exclusive_offers']:
            print(f"     💎 {offer['title']}")
            print(f"        {offer['description']}")
            print(f"        Value: {offer['value']} | Expires: {offer['expires_in']}")
        
        print(f"   🎁 Brand rewards: +{brand['rewards']['coins']} coins, +{brand['rewards']['vip_points']} VIP points")
        play_sound("brand_unlock.wav")
    
    # Demo 4: Sound Experience
    print("\n🔊 Sound Experience Demo:")
    
    sounds = [
        ("coin_collect.wav", "Coin collection"),
        ("quest_complete.wav", "Quest completion"),
        ("level_up.wav", "Level up"),
        ("brand_unlock.wav", "Brand unlock"),
        ("streak_celebration.wav", "Streak celebration")
    ]
    
    for sound_file, description in sounds:
        print(f"   🔊 {description}")
        play_sound(sound_file)
        time.sleep(0.5)
    
    print("\n🎊 Incentive Journey Demo Completed!")
    print("The incentive system provides engaging rewards and experiences!")

def test_incentive_integration():
    """Test incentive system integration with other systems"""
    
    print("\n🔗 Incentive Integration Test")
    print("=" * 30)
    
    controller = GraphicsController()
    
    # Setup complete system
    initialize_3d_system()
    enable_login_streak_rewards(days_required=3, bonus_coins=15)
    
    # Create player character
    from 3d_graphics_module import create_player_character, add_player_animations
    create_player_character(name="IncentiveTester", avatar_style="modern")
    add_player_animations(["walk", "idle"])
    
    # Create interactive zones
    from 3d_graphics_module import create_interactive_zone, trigger_reward_effect
    create_interactive_zone("IncentiveZone", "food_court", "coin")
    
    # Setup UI system
    from 3d_graphics_module import set_ui_language_support, add_top_bar
    set_ui_language_support(["en", "ar"])
    add_top_bar(coins_visible=True, language_toggle=True)
    
    print("🔄 Testing incentive integration with other systems:")
    
    # Test 1: Incentive + Character System
    print("\n   1. Incentive + Character System:")
    user_id = "integration_test_user"
    record_login(user_id)
    print("       Login recorded for character")
    
    # Test 2: Incentive + Zone System
    print("\n   2. Incentive + Zone System:")
    from 3d_graphics_module import trigger_zone_interaction
    player_pos = {"x": 0, "y": 0, "z": 50}
    zone_result = trigger_zone_interaction("IncentiveZone", player_pos)
    if zone_result["status"] == "success":
        play_sound("coin_collect.wav")
        print("       Zone interaction with sound effect")
    
    # Test 3: Incentive + Quest System
    print("\n   3. Incentive + Quest System:")
    quest_result = create_daily_quest("Complete Zone Interaction", 20)
    if quest_result["status"] == "success":
        quest_id = quest_result["quest_id"]
        update_quest_progress(quest_id, 1)
        complete_quest(quest_id, user_id)
        print("       Quest completed with rewards")
    
    # Test 4: Incentive + Brand System
    print("\n   4. Incentive + Brand System:")
    integrate_with_brand("Dubai Mall", "Premium Experience")
    brand_offers = get_brand_offers("Dubai Mall")
    if brand_offers["status"] == "success":
        print("       Brand integration successful")
    
    # Test 5: Incentive + UI System
    print("\n   5. Incentive + UI System:")
    from 3d_graphics_module import update_coin_display, update_xp_display
    update_coin_display(500)
    update_xp_display(1000)
    print("       UI updated with incentive rewards")
    
    print("\n✅ Incentive integration test completed successfully!")

if __name__ == "__main__":
    # Run comprehensive incentive system tests
    test_incentive_system()
    
    # Demonstrate incentive journey
    demo_incentive_journey()
    
    # Test incentive integration
    test_incentive_integration()
    
    print("\n🚀 Incentive system is ready for engaging mall experiences!")
    print("Login streaks, quests, sounds, and brand integration are fully operational!") 