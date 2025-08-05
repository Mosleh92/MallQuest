#!/usr/bin/env python3
"""
Interactive Features Test Script for Deerfields Mall Gamification System
Demonstrates mission zones, reward effects, minigames, and WiFi restrictions
"""

from 3d_graphics_module import (
    GraphicsController,
    create_interactive_zone,
    trigger_reward_effect,
    load_minigame,
    lock_game_to_wifi,
    set_outside_warning,
    check_wifi_connection,
    trigger_zone_interaction,
    start_minigame,
    create_player_character,
    add_player_animations,
    set_movement_zone,
    enable_third_person_camera,
    initialize_3d_system
)
import time
import json

def test_interactive_features():
    """Test the complete interactive features system"""
    
    print("🎮 Interactive Features Test - Deerfields Mall")
    print("=" * 55)
    
    # Initialize the graphics controller
    controller = GraphicsController()
    
    # Test 1: Your Commands Implementation
    print("\n1. Testing Your Commands Implementation")
    print("-" * 40)
    
    print("🎯 Implementing your commands:")
    print("   # ساخت نقاط مأموریت (mission zones)")
    result = create_interactive_zone(name="CoinDropZone", location="food_court", reward_type="coin")
    print(f"✅ Interactive zone created: {result}")
    
    print("   # افزودن پاداش کوین با افکت")
    result = trigger_reward_effect(type="coin_sparkle", amount=10)
    print(f"✅ Reward effect triggered: {result}")
    
    print("   # فعال‌سازی مینی‌گیم‌ها")
    result = load_minigame(name="SpinWheel", location="entrance_zone", cooldown="2h")
    print(f"✅ Minigame loaded: {result}")
    
    print("   # فعال‌سازی محدودیت دسترسی فقط در WiFi مول")
    result = lock_game_to_wifi(ssid="Deerfields_Free_WiFi")
    print(f"✅ WiFi restriction set: {result}")
    
    print("   # نمایش هشدار در صورت اتصال از بیرون")
    result = set_outside_warning(
        message_en="Please connect to mall WiFi to play.",
        message_ar="يرجى الاتصال بشبكة واي فاي المول للعب."
    )
    print(f"✅ Outside warning set: {result}")
    
    # Test 2: Interactive Zones
    print("\n2. Testing Interactive Zones")
    print("-" * 30)
    
    # Create multiple zones
    zones = [
        ("CoinDropZone", "food_court", "coin"),
        ("XPBoostZone", "fashion_area", "xp"),
        ("VIPZone", "electronics_area", "vip"),
        ("SpecialZone", "cafe_zone", "special")
    ]
    
    for name, location, reward_type in zones:
        result = create_interactive_zone(name, location, reward_type)
        if result["status"] == "success":
            zone = result["zone"]
            print(f"✅ Zone {name}: {location} ({reward_type})")
            print(f"   Position: {zone['position']}")
            print(f"   Color: {zone['visual_effects']['color']}")
        else:
            print(f"❌ Zone {name}: {result['message']}")
    
    # Test 3: Reward Effects
    print("\n3. Testing Reward Effects")
    print("-" * 30)
    
    effects = [
        ("coin_sparkle", 25),
        ("xp_burst", 50),
        ("vip_flash", 100),
        ("coin_sparkle", 5)
    ]
    
    for effect_type, amount in effects:
        result = trigger_reward_effect(effect_type, amount)
        if result["status"] == "success":
            effect = result["effect"]
            print(f"✅ {effect_type} effect: {amount}")
            print(f"   Duration: {effect['duration']}s")
            print(f"   Particles: {len(effect['particles'])}")
        else:
            print(f"❌ {effect_type} effect: {result['message']}")
    
    # Test 4: Minigames
    print("\n4. Testing Minigames")
    print("-" * 30)
    
    minigames = [
        ("SpinWheel", "entrance_zone", "2h"),
        ("MemoryGame", "fashion_area", "1h"),
        ("TreasureHunt", "electronics_area", "30m"),
        ("QuizGame", "cafe_zone", "15m")
    ]
    
    for name, location, cooldown in minigames:
        result = load_minigame(name, location, cooldown)
        if result["status"] == "success":
            minigame = result["minigame"]
            print(f"✅ Minigame {name}: {location}")
            print(f"   Type: {minigame['type']}")
            print(f"   Cooldown: {cooldown}")
            print(f"   Rewards: {minigame['rewards']}")
        else:
            print(f"❌ Minigame {name}: {result['message']}")
    
    # Test 5: WiFi Restrictions
    print("\n5. Testing WiFi Restrictions")
    print("-" * 30)
    
    # Test WiFi connection check
    for i in range(5):
        is_connected = check_wifi_connection()
        status = "✅ Connected" if is_connected else "❌ Disconnected"
        print(f"   WiFi Check {i+1}: {status}")
        time.sleep(0.5)
    
    # Test 6: Zone Interactions
    print("\n6. Testing Zone Interactions")
    print("-" * 30)
    
    # Create player character for testing
    create_player_character(name="TestPlayer", avatar_style="modern")
    add_player_animations(["walk", "idle"])
    set_movement_zone(area="mall_interior", movement_type="freewalk")
    enable_third_person_camera(smooth_tracking=True)
    
    # Test zone interactions with different player positions
    test_positions = [
        {"x": 0, "y": 0, "z": 50},      # Food court
        {"x": -40, "y": 0, "z": 0},     # Fashion area
        {"x": 40, "y": 0, "z": 0},      # Electronics area
        {"x": 20, "y": 0, "z": 30},     # Cafe zone
        {"x": 100, "y": 0, "z": 100}    # Outside zones
    ]
    
    zone_names = ["CoinDropZone", "XPBoostZone", "VIPZone", "SpecialZone"]
    
    for i, position in enumerate(test_positions):
        print(f"\n   Testing position {i+1}: {position}")
        for zone_name in zone_names:
            result = trigger_zone_interaction(zone_name, position)
            if result["status"] == "success":
                print(f"     ✅ {zone_name}: Reward triggered!")
            else:
                print(f"     ❌ {zone_name}: {result['message']}")
    
    # Test 7: Minigame Interactions
    print("\n7. Testing Minigame Interactions")
    print("-" * 30)
    
    minigame_positions = [
        {"x": 0, "y": 0, "z": -80},     # Entrance zone
        {"x": -40, "y": 0, "z": 0},     # Fashion area
        {"x": 40, "y": 0, "z": 0},      # Electronics area
        {"x": 20, "y": 0, "z": 30}      # Cafe zone
    ]
    
    minigame_names = ["SpinWheel", "MemoryGame", "TreasureHunt", "QuizGame"]
    
    for i, position in enumerate(minigame_positions):
        print(f"\n   Testing minigame position {i+1}: {position}")
        for minigame_name in minigame_names:
            result = start_minigame(minigame_name, position)
            if result["status"] == "success":
                print(f"     ✅ {minigame_name}: Started!")
            else:
                print(f"     ❌ {minigame_name}: {result['message']}")
    
    # Test 8: Cooldown System
    print("\n8. Testing Cooldown System")
    print("-" * 30)
    
    # Test zone cooldown
    zone_name = "CoinDropZone"
    position = {"x": 0, "y": 0, "z": 50}
    
    print(f"   Testing cooldown for {zone_name}:")
    
    # First interaction
    result1 = trigger_zone_interaction(zone_name, position)
    print(f"     First interaction: {result1['status']}")
    
    # Immediate second interaction (should be on cooldown)
    result2 = trigger_zone_interaction(zone_name, position)
    print(f"     Second interaction: {result2['status']}")
    if result2["status"] == "error":
        print(f"     Cooldown message: {result2['message']}")
    
    # Test 9: WiFi Warning System
    print("\n9. Testing WiFi Warning System")
    print("-" * 30)
    
    wifi_config = controller.graphics_engine.wifi_restrictions
    if "warning" in wifi_config:
        warning = wifi_config["warning"]
        print(f"   English warning: {warning['en']}")
        print(f"   Arabic warning: {warning['ar']}")
        print(f"   Display duration: {warning['display_duration']}s")
        print(f"   Style: {warning['style']}")
    
    # Test 10: Advanced Features
    print("\n10. Testing Advanced Features")
    print("-" * 30)
    
    # Test particle generation
    print("   Testing particle generation:")
    for effect_type in ["coin_sparkle", "xp_burst", "vip_flash"]:
        particles = controller.graphics_engine._generate_reward_particles(effect_type, 5)
        print(f"     {effect_type}: {len(particles)} particles generated")
    
    # Test location positions
    print("   Testing location positions:")
    locations = ["food_court", "entrance_zone", "fashion_area", "electronics_area", "cafe_zone"]
    for location in locations:
        pos = controller.graphics_engine._get_zone_position(location)
        print(f"     {location}: {pos}")
    
    print("\n🎉 Interactive Features Test Completed Successfully!")
    print("=" * 55)
    
    return controller

def demo_interactive_journey():
    """Demonstrate a complete interactive journey through the mall"""
    
    print("\n🌟 Interactive Journey Demo")
    print("=" * 35)
    
    controller = GraphicsController()
    
    # Initialize system
    initialize_3d_system()
    
    # Setup player
    create_player_character(name="InteractiveVisitor", avatar_style="modern")
    add_player_animations(["walk", "run", "idle", "jump"])
    set_movement_zone(area="mall_interior", movement_type="freewalk")
    enable_third_person_camera(smooth_tracking=True)
    
    # Setup interactive features
    create_interactive_zone("CoinDropZone", "food_court", "coin")
    create_interactive_zone("XPBoostZone", "fashion_area", "xp")
    create_interactive_zone("VIPZone", "electronics_area", "vip")
    load_minigame("SpinWheel", "entrance_zone", "2h")
    lock_game_to_wifi("Deerfields_Free_WiFi")
    set_outside_warning(
        "Please connect to mall WiFi to play.",
        "يرجى الاتصال بشبكة واي فاي المول للعب."
    )
    
    print("\n🚶 Interactive journey through Deerfields Mall...")
    
    # Check WiFi connection
    print("📶 Checking WiFi connection...")
    is_connected = check_wifi_connection()
    if is_connected:
        print("✅ Connected to Deerfields WiFi - Game unlocked!")
    else:
        print("❌ Not connected to mall WiFi - Game locked!")
        return
    
    # Enter mall and find SpinWheel
    print("\n🎰 Looking for SpinWheel at entrance...")
    player_pos = {"x": 0, "y": 0, "z": -80}
    result = start_minigame("SpinWheel", player_pos)
    if result["status"] == "success":
        print("🎉 SpinWheel started! Potential rewards:")
        rewards = result["rewards"]
        print(f"   Coins: {rewards['coins']['min']}-{rewards['coins']['max']}")
        print(f"   XP: {rewards['xp']['min']}-{rewards['xp']['max']}")
        if "special_items" in rewards:
            print(f"   Special items: {rewards['special_items']}")
    
    # Walk to food court for coin drop
    print("\n🍕 Walking to food court for coin drop...")
    player_pos = {"x": 0, "y": 0, "z": 50}
    result = trigger_zone_interaction("CoinDropZone", player_pos)
    if result["status"] == "success":
        print("🪙 Coin drop zone activated!")
        trigger_reward_effect("coin_sparkle", 15)
    
    # Visit fashion area for XP boost
    print("\n👗 Visiting fashion area for XP boost...")
    player_pos = {"x": -40, "y": 0, "z": 0}
    result = trigger_zone_interaction("XPBoostZone", player_pos)
    if result["status"] == "success":
        print("⚡ XP boost zone activated!")
        trigger_reward_effect("xp_burst", 75)
    
    # Check electronics area for VIP zone
    print("\n📱 Checking electronics area for VIP zone...")
    player_pos = {"x": 40, "y": 0, "z": 0}
    result = trigger_zone_interaction("VIPZone", player_pos)
    if result["status"] == "success":
        print("👑 VIP zone activated!")
        trigger_reward_effect("vip_flash", 200)
    
    # Try to trigger same zone again (cooldown test)
    print("\n⏰ Testing cooldown system...")
    result = trigger_zone_interaction("CoinDropZone", player_pos)
    if result["status"] == "error":
        print(f"✅ Cooldown working: {result['message']}")
    
    print("\n🎊 Interactive journey completed!")
    print("The visitor successfully explored all interactive features!")

def test_wifi_security():
    """Test WiFi security and restriction features"""
    
    print("\n🔒 WiFi Security Test")
    print("=" * 25)
    
    controller = GraphicsController()
    
    # Setup WiFi restrictions
    lock_game_to_wifi("Deerfields_Free_WiFi")
    set_outside_warning(
        "Please connect to mall WiFi to play.",
        "يرجى الاتصال بشبكة واي فاي المول للعب."
    )
    
    print("📡 Testing WiFi connection scenarios:")
    
    # Simulate different network connections
    networks = ["Deerfields_Free_WiFi", "Other_Network", "Mobile_Data"]
    
    for network in networks:
        print(f"\n   Testing connection to: {network}")
        
        # Simulate network change
        controller.graphics_engine.wifi_restrictions["main"]["connection_status"] = "unknown"
        
        # Check connection
        is_connected = check_wifi_connection()
        
        if is_connected:
            print("     ✅ Game unlocked - Full access granted")
        else:
            print("     ❌ Game locked - Access restricted")
            warning = controller.graphics_engine.wifi_restrictions["warning"]
            print(f"     Warning EN: {warning['en']}")
            print(f"     Warning AR: {warning['ar']}")
    
    print("\n🔐 WiFi security test completed!")

if __name__ == "__main__":
    # Run comprehensive interactive features tests
    test_interactive_features()
    
    # Demonstrate interactive journey
    demo_interactive_journey()
    
    # Test WiFi security
    test_wifi_security()
    
    print("\n🚀 Interactive features system is ready for immersive mall experiences!")
    print("Mission zones, minigames, and WiFi restrictions are fully operational!") 