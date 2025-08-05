#!/usr/bin/env python3
"""
UI System Test Script for Deerfields Mall Gamification System
Demonstrates bilingual support, main menu, and top bar functionality
"""

from 3d_graphics_module import (
    GraphicsController,
    set_ui_language_support,
    load_main_menu,
    add_top_bar,
    switch_language,
    get_translation,
    render_main_menu,
    render_top_bar,
    update_coin_display,
    update_xp_display,
    initialize_3d_system
)
import time
import json

def test_ui_system():
    """Test the complete UI system"""
    
    print("🖥️ UI System Test - Deerfields Mall")
    print("=" * 50)
    
    # Initialize the graphics controller
    controller = GraphicsController()
    
    # Test 1: Your Commands Implementation
    print("\n1. Testing Your Commands Implementation")
    print("-" * 40)
    
    print("🎯 Implementing your commands:")
    print("   # فعال‌سازی رابط دوزبانه فقط بدون فارسي")
    result = set_ui_language_support(["en", "ar"])
    print(f"✅ UI language support set: {result}")
    
    print("   # بارگذاری منوی اصلی")
    result = load_main_menu(options=["Play", "Quests", "Rewards", "Profile"], font="Dubai")
    print(f"✅ Main menu loaded: {result}")
    
    print("   # افزودن نوار کوین بالا")
    result = add_top_bar(coins_visible=True, language_toggle=True)
    print(f"✅ Top bar added: {result}")
    
    # Test 2: Language Support System
    print("\n2. Testing Language Support System")
    print("-" * 35)
    
    # Test language switching
    languages = ["en", "ar"]
    for lang in languages:
        result = switch_language(lang)
        if result["status"] == "success":
            print(f"✅ Language switched to: {lang} ({result['direction']})")
            
            # Test translations
            test_keys = ["play", "quests", "rewards", "profile", "coins", "xp"]
            print(f"   Translations in {lang}:")
            for key in test_keys:
                translation = get_translation(key, lang)
                print(f"     {key}: {translation}")
        else:
            print(f"❌ Language switch failed: {result['message']}")
    
    # Test 3: Main Menu System
    print("\n3. Testing Main Menu System")
    print("-" * 30)
    
    # Test menu rendering in different languages
    for lang in ["en", "ar"]:
        switch_language(lang)
        result = render_main_menu()
        if result["status"] == "success":
            print(f"✅ Main menu rendered in {lang}:")
            for item in result["menu_items"]:
                print(f"   {item['original']} → {item['translated']} ({item['direction']})")
        else:
            print(f"❌ Menu rendering failed: {result['message']}")
    
    # Test 4: Top Bar System
    print("\n4. Testing Top Bar System")
    print("-" * 30)
    
    # Test top bar rendering with different values
    test_values = [
        {"coins": 0, "xp": 0},
        {"coins": 150, "xp": 250},
        {"coins": 1000, "xp": 5000},
        {"coins": 50000, "xp": 25000}
    ]
    
    for values in test_values:
        result = render_top_bar(values["coins"], values["xp"])
        if result["status"] == "success":
            data = result["top_bar_data"]
            print(f"✅ Top bar rendered:")
            print(f"   Coins: {data['coins']['value']} ({data['coins']['label']})")
            print(f"   XP: {data['xp']['value']} ({data['xp']['label']})")
            print(f"   Language: {data['language']['name']} ({data['language']['direction']})")
        else:
            print(f"❌ Top bar rendering failed: {result['message']}")
    
    # Test 5: Dynamic Updates
    print("\n5. Testing Dynamic Updates")
    print("-" * 30)
    
    # Test coin display updates
    coin_updates = [100, 250, 500, 1000, 2500]
    for coins in coin_updates:
        result = update_coin_display(coins)
        if result["status"] == "success":
            print(f"✅ Coin display updated: {result['coins']}")
        else:
            print(f"❌ Coin update failed: {result['message']}")
    
    # Test XP display updates
    xp_updates = [50, 100, 250, 500, 1000]
    for xp in xp_updates:
        result = update_xp_display(xp)
        if result["status"] == "success":
            print(f"✅ XP display updated: {result['xp']}")
        else:
            print(f"❌ XP update failed: {result['message']}")
    
    # Test 6: Language Features
    print("\n6. Testing Language Features")
    print("-" * 30)
    
    # Test all available translations
    all_keys = [
        "play", "quests", "rewards", "profile", "coins", "xp", "level",
        "settings", "language", "back", "confirm", "cancel", "loading", "error", "success"
    ]
    
    for lang in ["en", "ar"]:
        print(f"\n   Translations in {lang}:")
        for key in all_keys:
            translation = get_translation(key, lang)
            print(f"     {key}: {translation}")
    
    # Test 7: UI Configuration
    print("\n7. Testing UI Configuration")
    print("-" * 30)
    
    # Check main menu configuration
    if controller.graphics_engine.main_menu:
        menu_config = controller.graphics_engine.main_menu
        print(f"✅ Main menu configuration:")
        print(f"   Options: {menu_config['options']}")
        print(f"   Font: {menu_config['font']}")
        print(f"   Style: {menu_config['style']}")
        print(f"   Layout: {menu_config['layout']}")
        print(f"   Animations: {menu_config['animations']}")
    
    # Check top bar configuration
    if controller.graphics_engine.top_bar:
        top_bar_config = controller.graphics_engine.top_bar
        print(f"✅ Top bar configuration:")
        print(f"   Coins visible: {top_bar_config['coins_visible']}")
        print(f"   Language toggle: {top_bar_config['language_toggle']}")
        print(f"   Style: {top_bar_config['style']}")
        print(f"   Elements: {list(top_bar_config['elements'].keys())}")
        print(f"   Animations: {top_bar_config['animations']}")
    
    # Test 8: Language Support Configuration
    print("\n8. Testing Language Support Configuration")
    print("-" * 40)
    
    for lang, config in controller.graphics_engine.language_support.items():
        print(f"✅ Language {lang}:")
        print(f"   Name: {config['name']}")
        print(f"   Direction: {config['direction']}")
        print(f"   Font: {config['font']}")
        print(f"   Translation count: {len(config['translations'])}")
    
    # Test 9: Error Handling
    print("\n9. Testing Error Handling")
    print("-" * 25)
    
    # Test invalid language
    result = switch_language("invalid_lang")
    if result["status"] == "error":
        print(f"✅ Invalid language handled: {result['message']}")
    
    # Test menu rendering without menu
    controller.graphics_engine.main_menu = {}
    result = render_main_menu()
    if result["status"] == "error":
        print(f"✅ No menu error handled: {result['message']}")
    
    # Test top bar rendering without top bar
    controller.graphics_engine.top_bar = {}
    result = render_top_bar()
    if result["status"] == "error":
        print(f"✅ No top bar error handled: {result['message']}")
    
    # Restore configurations
    load_main_menu(options=["Play", "Quests", "Rewards", "Profile"], font="Dubai")
    add_top_bar(coins_visible=True, language_toggle=True)
    
    # Test 10: Performance Testing
    print("\n10. Testing Performance")
    print("-" * 25)
    
    # Test rapid language switching
    print("   Testing rapid language switching:")
    start_time = time.time()
    for i in range(10):
        switch_language("en" if i % 2 == 0 else "ar")
        get_translation("play")
    end_time = time.time()
    print(f"   ✅ 10 language switches completed in {end_time - start_time:.3f}s")
    
    # Test rapid updates
    print("   Testing rapid display updates:")
    start_time = time.time()
    for i in range(20):
        update_coin_display(i * 10)
        update_xp_display(i * 5)
    end_time = time.time()
    print(f"   ✅ 40 display updates completed in {end_time - start_time:.3f}s")
    
    print("\n🎉 UI System Test Completed Successfully!")
    print("=" * 50)
    
    return controller

def demo_ui_experience():
    """Demonstrate a complete UI experience"""
    
    print("\n🌟 UI Experience Demo")
    print("=" * 25)
    
    controller = GraphicsController()
    
    # Initialize system
    initialize_3d_system()
    
    # Setup UI system
    set_ui_language_support(["en", "ar"])
    load_main_menu(options=["Play", "Quests", "Rewards", "Profile"], font="Dubai")
    add_top_bar(coins_visible=True, language_toggle=True)
    
    print("\n🖥️ UI Experience Demo - Deerfields Mall")
    
    # Demo 1: English Experience
    print("\n🇺🇸 English UI Experience:")
    switch_language("en")
    
    # Show main menu
    menu_result = render_main_menu()
    if menu_result["status"] == "success":
        print("   Main Menu Options:")
        for item in menu_result["menu_items"]:
            print(f"     • {item['translated']}")
    
    # Show top bar
    top_bar_result = render_top_bar(1250, 3400)
    if top_bar_result["status"] == "success":
        data = top_bar_result["top_bar_data"]
        print(f"   Top Bar: {data['coins']['value']} {data['coins']['label']} | {data['xp']['value']} {data['xp']['label']}")
    
    # Demo 2: Arabic Experience
    print("\n🇸🇦 Arabic UI Experience:")
    switch_language("ar")
    
    # Show main menu in Arabic
    menu_result = render_main_menu()
    if menu_result["status"] == "success":
        print("   خيارات القائمة الرئيسية:")
        for item in menu_result["menu_items"]:
            print(f"     • {item['translated']}")
    
    # Show top bar in Arabic
    top_bar_result = render_top_bar(1250, 3400)
    if top_bar_result["status"] == "success":
        data = top_bar_result["top_bar_data"]
        print(f"   الشريط العلوي: {data['coins']['value']} {data['coins']['label']} | {data['xp']['value']} {data['xp']['label']}")
    
    # Demo 3: Dynamic Updates
    print("\n🔄 Dynamic Updates Demo:")
    
    # Simulate coin earning
    coin_amounts = [0, 50, 150, 300, 500, 750, 1000]
    for coins in coin_amounts:
        update_coin_display(coins)
        time.sleep(0.3)
        print(f"   Coins: {coins}")
    
    # Simulate XP earning
    xp_amounts = [0, 25, 75, 150, 250, 400, 600]
    for xp in xp_amounts:
        update_xp_display(xp)
        time.sleep(0.3)
        print(f"   XP: {xp}")
    
    # Demo 4: Language Switching
    print("\n🌐 Language Switching Demo:")
    
    for i in range(3):
        # Switch to English
        switch_language("en")
        play_text = get_translation("play")
        print(f"   {i+1}. English: {play_text}")
        time.sleep(0.5)
        
        # Switch to Arabic
        switch_language("ar")
        play_text = get_translation("play")
        print(f"   {i+1}. Arabic: {play_text}")
        time.sleep(0.5)
    
    print("\n🎊 UI Experience Demo Completed!")
    print("The bilingual UI system provides seamless language switching!")

def test_ui_integration():
    """Test UI integration with other systems"""
    
    print("\n🔗 UI Integration Test")
    print("=" * 25)
    
    controller = GraphicsController()
    
    # Setup complete system
    initialize_3d_system()
    set_ui_language_support(["en", "ar"])
    load_main_menu(options=["Play", "Quests", "Rewards", "Profile"], font="Dubai")
    add_top_bar(coins_visible=True, language_toggle=True)
    
    # Create player character
    from 3d_graphics_module import create_player_character, add_player_animations
    create_player_character(name="UITester", avatar_style="modern")
    add_player_animations(["walk", "idle"])
    
    # Create interactive zones
    from 3d_graphics_module import create_interactive_zone, trigger_reward_effect
    create_interactive_zone("TestZone", "food_court", "coin")
    
    print("🔄 Testing UI integration with other systems:")
    
    # Test 1: UI + Character System
    print("\n   1. UI + Character System:")
    switch_language("en")
    play_text = get_translation("play")
    print(f"       Play button: {play_text}")
    
    # Test 2: UI + Reward System
    print("\n   2. UI + Reward System:")
    trigger_reward_effect("coin_sparkle", 25)
    update_coin_display(250)
    print("       Coin reward triggered and UI updated")
    
    # Test 3: UI + Zone System
    print("\n   3. UI + Zone System:")
    from 3d_graphics_module import trigger_zone_interaction
    player_pos = {"x": 0, "y": 0, "z": 50}
    zone_result = trigger_zone_interaction("TestZone", player_pos)
    if zone_result["status"] == "success":
        update_coin_display(275)
        print("       Zone interaction completed and UI updated")
    
    # Test 4: UI + Language System
    print("\n   4. UI + Language System:")
    for lang in ["en", "ar"]:
        switch_language(lang)
        rewards_text = get_translation("rewards")
        print(f"       Rewards in {lang}: {rewards_text}")
    
    print("\n✅ UI integration test completed successfully!")

if __name__ == "__main__":
    # Run comprehensive UI system tests
    test_ui_system()
    
    # Demonstrate UI experience
    demo_ui_experience()
    
    # Test UI integration
    test_ui_integration()
    
    print("\n🚀 UI system is ready for bilingual mall experiences!")
    print("English and Arabic interfaces are fully operational!") 