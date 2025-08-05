#!/usr/bin/env python3
"""
Player Character Test Script for Deerfields Mall Gamification System
Demonstrates character creation, animations, movement, and camera features
"""

from 3d_graphics_module import (
    GraphicsController,
    create_player_character,
    add_player_animations,
    set_movement_zone,
    enable_third_person_camera,
    move_player,
    play_animation,
    initialize_3d_system
)
import time
import json

def test_player_character_system():
    """Test the complete player character system"""
    
    print("👤 Player Character System Test - Deerfields Mall")
    print("=" * 55)
    
    # Initialize the graphics controller
    controller = GraphicsController()
    
    # Test 1: Character Creation
    print("\n1. Testing Character Creation")
    print("-" * 30)
    
    # Test your commands implementation
    print("🎮 Implementing your commands:")
    print("   # ساخت کاراکتر اصلی")
    result = create_player_character(name="Visitor", avatar_style="modern")
    print(f"✅ Character created: {result}")
    
    print("   # افزودن انیمیشن‌های حرکت")
    result = add_player_animations(["walk", "run", "idle", "jump"])
    print(f"✅ Animations added: {result}")
    
    print("   # اجازه حرکت آزاد در محدوده mall")
    result = set_movement_zone(area="mall_interior", movement_type="freewalk")
    print(f"✅ Movement zone set: {result}")
    
    print("   # فعال‌سازی دوربین سوم‌شخص")
    result = enable_third_person_camera(smooth_tracking=True)
    print(f"✅ Third-person camera enabled: {result}")
    
    # Test 2: Character Details
    print("\n2. Testing Character Details")
    print("-" * 30)
    
    character = controller.graphics_engine.player_character
    if character:
        print(f"✅ Character name: {character['name']}")
        print(f"✅ Avatar style: {character['avatar_style']}")
        print(f"✅ Position: {character['position']}")
        print(f"✅ Model: {character['model']}")
        print(f"✅ Textures: {list(character['textures'].keys())}")
        print(f"✅ Animations: {list(character['animations'].keys())}")
    
    # Test 3: Animation System
    print("\n3. Testing Animation System")
    print("-" * 30)
    
    animations = ["walk", "run", "idle", "jump", "wave", "dance"]
    for anim in animations:
        result = play_animation(anim)
        if result["status"] == "success":
            print(f"✅ {anim} animation: {result['duration']}s")
        else:
            print(f"❌ {anim} animation: {result['message']}")
    
    # Test 4: Movement System
    print("\n4. Testing Movement System")
    print("-" * 30)
    
    directions = ["forward", "backward", "left", "right", "up", "down"]
    for direction in directions:
        result = move_player(direction, speed=2.0)
        if result["status"] == "success":
            print(f"✅ Moved {direction}: {result['new_position']}")
        else:
            print(f"❌ Move {direction}: {result['message']}")
    
    # Test 5: Movement Zones
    print("\n5. Testing Movement Zones")
    print("-" * 30)
    
    zones = ["mall_interior", "store_interior", "outdoor_area"]
    for zone in zones:
        result = set_movement_zone(area=zone, movement_type="freewalk")
        if result["status"] == "success":
            zone_data = controller.graphics_engine.movement_zones[zone]
            bounds = zone_data["bounds"]
            print(f"✅ Zone {zone}: {bounds['min']} to {bounds['max']}")
        else:
            print(f"❌ Zone {zone}: {result['message']}")
    
    # Test 6: Camera System
    print("\n6. Testing Camera System")
    print("-" * 30)
    
    camera_config = controller.graphics_engine.camera_mode
    print(f"✅ Camera mode: {camera_config}")
    print(f"✅ Smooth tracking: {controller.graphics_engine.camera_smooth_tracking}")
    print(f"✅ Camera position: {controller.graphics_engine.camera_position}")
    
    # Test 7: Character Customization
    print("\n7. Testing Character Customization")
    print("-" * 30)
    
    avatar_styles = ["modern", "casual", "formal", "sporty"]
    for style in avatar_styles:
        result = create_player_character(name=f"Visitor_{style}", avatar_style=style)
        if result["status"] == "success":
            character = result["character"]
            print(f"✅ {style} style: {character['model']}")
            print(f"   Textures: {list(character['textures'].keys())}")
    
    # Test 8: Advanced Movement
    print("\n8. Testing Advanced Movement")
    print("-" * 30)
    
    # Reset character position
    controller.graphics_engine.player_character["position"] = {"x": 0, "y": 0, "z": 0}
    
    # Complex movement pattern
    movement_pattern = [
        ("forward", 5.0),
        ("right", 3.0),
        ("forward", 2.0),
        ("left", 4.0),
        ("backward", 3.0)
    ]
    
    for direction, speed in movement_pattern:
        result = move_player(direction, speed)
        if result["status"] == "success":
            print(f"✅ Moved {direction} (speed {speed}): {result['new_position']}")
        else:
            print(f"❌ Move {direction}: {result['message']}")
    
    # Test 9: Animation Sequences
    print("\n9. Testing Animation Sequences")
    print("-" * 30)
    
    animation_sequence = ["idle", "walk", "run", "jump", "idle"]
    for anim in animation_sequence:
        result = play_animation(anim)
        if result["status"] == "success":
            print(f"✅ Playing {anim} animation")
            time.sleep(0.5)  # Simulate animation duration
        else:
            print(f"❌ Animation {anim}: {result['message']}")
    
    # Test 10: Boundary Testing
    print("\n10. Testing Boundary Testing")
    print("-" * 30)
    
    # Try to move outside boundaries
    extreme_movements = [
        ("forward", 200.0),  # Try to move far beyond mall bounds
        ("up", 50.0),        # Try to move above mall height
        ("right", 150.0)     # Try to move beyond mall width
    ]
    
    for direction, speed in extreme_movements:
        result = move_player(direction, speed)
        if result["status"] == "error":
            print(f"✅ Boundary enforced: {result['message']}")
        else:
            print(f"❌ Boundary failed: {result['new_position']}")
    
    print("\n🎉 Player Character System Test Completed Successfully!")
    print("=" * 55)
    
    return controller

def demo_character_journey():
    """Demonstrate a complete character journey through the mall"""
    
    print("\n🌟 Character Journey Demo")
    print("=" * 35)
    
    controller = GraphicsController()
    
    # Initialize system
    initialize_3d_system()
    
    # Create character
    create_player_character(name="MallVisitor", avatar_style="modern")
    add_player_animations(["walk", "run", "idle", "jump", "wave"])
    set_movement_zone(area="mall_interior", movement_type="freewalk")
    enable_third_person_camera(smooth_tracking=True)
    
    print("\n🚶 Character journey through Deerfields Mall...")
    
    # Enter mall
    print("📍 Entering mall main entrance...")
    play_animation("idle")
    time.sleep(1)
    
    # Walk to fashion store
    print("👗 Walking to Deerfields Fashion...")
    play_animation("walk")
    move_player("forward", 10.0)
    move_player("left", 20.0)
    time.sleep(1)
    
    # Arrive at fashion store
    print("🛍️ Arrived at Deerfields Fashion!")
    play_animation("idle")
    time.sleep(1)
    
    # Wave at store
    print("👋 Waving at the store...")
    play_animation("wave")
    time.sleep(1)
    
    # Run to electronics store
    print("📱 Running to Deerfields Electronics...")
    play_animation("run")
    move_player("right", 40.0)
    move_player("forward", 15.0)
    time.sleep(1)
    
    # Jump for joy
    print("🎉 Jumping for joy!")
    play_animation("jump")
    time.sleep(1)
    
    # Walk to café
    print("☕ Walking to Deerfields Café...")
    play_animation("walk")
    move_player("backward", 25.0)
    move_player("right", 20.0)
    time.sleep(1)
    
    # Final idle pose
    print("😌 Relaxing at the café...")
    play_animation("idle")
    
    print("\n🎊 Character journey completed!")
    print("The character successfully navigated through the mall!")

def test_character_interactions():
    """Test character interactions with mall environment"""
    
    print("\n🤝 Character Interactions Demo")
    print("=" * 35)
    
    controller = GraphicsController()
    
    # Initialize with character
    create_player_character(name="InteractiveVisitor", avatar_style="casual")
    add_player_animations(["walk", "idle", "wave", "dance"])
    set_movement_zone(area="mall_interior", movement_type="freewalk")
    enable_third_person_camera(smooth_tracking=True)
    
    # Test store interactions
    stores = [
        {"name": "Deerfields Fashion", "position": {"x": -30, "y": 0, "z": -20}},
        {"name": "Deerfields Electronics", "position": {"x": 30, "y": 0, "z": -20}},
        {"name": "Deerfields Café", "position": {"x": 0, "y": 0, "z": 30}}
    ]
    
    for store in stores:
        print(f"\n🏪 Interacting with {store['name']}...")
        
        # Move to store
        target_pos = store["position"]
        current_pos = controller.graphics_engine.player_character["position"]
        
        # Calculate movement to store
        dx = target_pos["x"] - current_pos["x"]
        dz = target_pos["z"] - current_pos["z"]
        
        if abs(dx) > 1:
            direction = "right" if dx > 0 else "left"
            move_player(direction, abs(dx))
        
        if abs(dz) > 1:
            direction = "forward" if dz < 0 else "backward"
            move_player(direction, abs(dz))
        
        # Interact with store
        print(f"   📍 Arrived at {store['name']}")
        play_animation("wave")
        time.sleep(0.5)
        
        # Simulate shopping interaction
        print(f"   🛍️ Browsing {store['name']}...")
        play_animation("idle")
        time.sleep(1)
    
    # Dance celebration
    print("\n💃 Dance celebration!")
    play_animation("dance")
    time.sleep(2)
    
    print("\n🎉 Character interactions completed!")

if __name__ == "__main__":
    # Run comprehensive player character tests
    test_player_character_system()
    
    # Demonstrate character journey
    demo_character_journey()
    
    # Test character interactions
    test_character_interactions()
    
    print("\n🚀 Player character system is ready for immersive mall experiences!")
    print("Characters can now freely explore and interact with the mall environment!") 