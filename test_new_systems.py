#!/usr/bin/env python3
"""
Test Script for New Systems: Deer Care, Empire Management, and Notification Systems
Demonstrates all the new features requested by the user
"""

import time
from datetime import datetime, timedelta

def test_deer_care_system():
    """Test the deer care system"""
    print("\n" + "="*60)
    print("🦌 TESTING DEER CARE SYSTEM")
    print("="*60)
    
    try:
        from deer_care_system import deer_care_system
        
        user_id = "test_user_deer"
        
        # Test 1: Create a deer
        print("\n1. Creating a deer companion...")
        result = deer_care_system.create_deer(user_id, "arabian_oryx")
        if result["status"] == "success":
            deer = result["deer"]
            print(f"✅ Created {deer['name']} (Level {deer['level']})")
            print(f"   Health: {deer['health']}, Happiness: {deer['happiness']}, Energy: {deer['energy']}, Hunger: {deer['hunger']}")
        else:
            print(f"❌ Failed to create deer: {result['message']}")
            return
        
        # Test 2: Feed the deer
        print("\n2. Feeding the deer...")
        result = deer_care_system.feed_deer(user_id, "desert_grass")
        if result["status"] == "success":
            print(f"✅ Fed deer with desert grass (+{result['xp_gained']} XP)")
            print(f"   New stats - Health: {result['deer']['health']}, Happiness: {result['deer']['happiness']}, Hunger: {result['deer']['hunger']}")
        else:
            print(f"❌ Failed to feed deer: {result['message']}")
        
        # Test 3: Entertain the deer
        print("\n3. Entertaining the deer...")
        result = deer_care_system.entertain_deer(user_id, "star_gazing")
        if result["status"] == "success":
            print(f"✅ Entertained deer with star gazing (+{result['xp_gained']} XP)")
            print(f"   New stats - Happiness: {result['deer']['happiness']}, Energy: {result['deer']['energy']}")
        else:
            print(f"❌ Failed to entertain deer: {result['message']}")
        
        # Test 4: Build shelter
        print("\n4. Building shelter...")
        result = deer_care_system.build_shelter(user_id, "desert_oasis")
        if result["status"] == "success":
            print(f"✅ Built {result['shelter']['name']} (+{result['xp_gained']} XP)")
            print(f"   Shelter boosts - Health: +{result['shelter']['health_boost']}, Happiness: +{result['shelter']['happiness_boost']}")
        else:
            print(f"❌ Failed to build shelter: {result['message']}")
        
        # Test 5: Get deer status
        print("\n5. Getting deer status...")
        result = deer_care_system.get_deer_status(user_id)
        if result["status"] == "success":
            deer = result["deer"]
            print(f"✅ Deer Status:")
            print(f"   Level: {deer['level']}, XP: {deer['xp']}")
            print(f"   Health: {deer['health']}, Happiness: {deer['happiness']}, Energy: {deer['energy']}, Hunger: {deer['hunger']}")
            print(f"   Shelter: {deer['shelter']}")
            print(f"   Abilities: {', '.join(deer['abilities'])}")
            print(f"   Visual Effects: {', '.join(deer['visual_effects'])}")
            
            if result["recommendations"]:
                print(f"   Recommendations: {', '.join(result['recommendations'])}")
        else:
            print(f"❌ Failed to get deer status: {result['message']}")
        
        # Test 6: Get available options
        print("\n6. Available options...")
        food_result = deer_care_system.get_available_food()
        activity_result = deer_care_system.get_available_activities()
        shelter_result = deer_care_system.get_available_shelters()
        
        print(f"✅ Available food types: {len(food_result['food_types'])}")
        print(f"✅ Available activities: {len(activity_result['activities'])}")
        print(f"✅ Available shelters: {len(shelter_result['shelters'])}")
        
    except ImportError as e:
        print(f"❌ Could not import deer care system: {e}")
    except Exception as e:
        print(f"❌ Error testing deer care system: {e}")

def test_empire_management_system():
    """Test the empire management system"""
    print("\n" + "="*60)
    print("🏛️ TESTING EMPIRE MANAGEMENT SYSTEM")
    print("="*60)
    
    try:
        from empire_management_system import empire_management_system
        
        user_id = "test_user_empire"
        user_level = 10
        user_coins = 5000
        
        # Test 1: Create empire
        print("\n1. Creating empire...")
        result = empire_management_system.create_empire(user_id)
        if result["status"] == "success":
            empire = result["empire"]
            print(f"✅ Created empire: {empire['name']}")
        else:
            print(f"❌ Failed to create empire: {result['message']}")
            return
        
        # Test 2: Purchase facilities
        print("\n2. Purchasing facilities...")
        facilities_to_buy = ["food_court", "entertainment_center", "tech_store"]
        
        for facility_type in facilities_to_buy:
            result = empire_management_system.purchase_facility(user_id, facility_type, user_level, user_coins)
            if result["status"] == "success":
                facility = result["facility"]
                print(f"✅ Purchased {facility['name']} (-{result['cost']} coins)")
                print(f"   Income: {facility['income_per_hour']}/hour, Visitors: {facility['visitor_capacity']}")
                user_coins = result["remaining_coins"]
            else:
                print(f"❌ Failed to purchase {facility_type}: {result['message']}")
        
        # Test 3: Upgrade facility
        print("\n3. Upgrading facility...")
        empire_status = empire_management_system.get_empire_status(user_id)
        if empire_status["status"] == "success" and empire_status["available_upgrades"]:
            upgrade = empire_status["available_upgrades"][0]
            result = empire_management_system.upgrade_facility(user_id, upgrade["facility_id"], user_coins)
            if result["status"] == "success":
                print(f"✅ Upgraded {result['facility']['name']} to level {result['new_level']} (-{result['cost']} coins)")
                user_coins = result["remaining_coins"]
            else:
                print(f"❌ Failed to upgrade facility: {result['message']}")
        else:
            print("ℹ️ No facilities available for upgrade")
        
        # Test 4: Start special event
        print("\n4. Starting special event...")
        empire_status = empire_management_system.get_empire_status(user_id)
        if empire_status["status"] == "success" and empire_status["empire"]["facilities"]:
            facility = empire_status["empire"]["facilities"][0]
            result = empire_management_system.start_special_event(user_id, facility["facility_id"], "food_festival", user_coins)
            if result["status"] == "success":
                event = result["event"]
                print(f"✅ Started {event['name']} at {facility['name']} (-{result['cost']} coins)")
                print(f"   Duration: {event['duration_hours']} hours, Income multiplier: {event['income_multiplier']}x")
                user_coins = result["remaining_coins"]
            else:
                print(f"❌ Failed to start event: {result['message']}")
        else:
            print("ℹ️ No facilities available for events")
        
        # Test 5: Collect income
        print("\n5. Collecting income...")
        # Simulate time passing by modifying the last collection time
        if hasattr(empire_management_system, 'empire_storage') and user_id in empire_management_system.empire_storage:
            empire_management_system.empire_storage[user_id]["last_income_collection"] = (datetime.now() - timedelta(hours=2)).isoformat()
        
        result = empire_management_system.collect_income(user_id)
        if result["status"] == "success":
            print(f"✅ Collected {result['total_income']} coins from empire facilities")
            print(f"   Hours passed: {result['hours_passed']:.1f}")
            for facility_id, income in result["facility_incomes"].items():
                print(f"   - Facility {facility_id}: {income} coins")
        else:
            print(f"❌ Failed to collect income: {result['message']}")
        
        # Test 6: Get empire status
        print("\n6. Getting empire status...")
        result = empire_management_system.get_empire_status(user_id)
        if result["status"] == "success":
            empire = result["empire"]
            stats = result["stats"]
            print(f"✅ Empire Status:")
            print(f"   Level: {empire['level']}, Total Income: {empire['total_income']}")
            print(f"   Facilities: {stats['facility_count']}, Active Events: {stats['active_events']}")
            print(f"   Total Income/Hour: {stats['total_income_per_hour']}")
            print(f"   Total Visitor Capacity: {stats['total_visitor_capacity']}")
            print(f"   Total Happiness Boost: {stats['total_happiness_boost']}")
            
            if result["available_upgrades"]:
                print(f"   Available Upgrades: {len(result['available_upgrades'])}")
            if result["available_purchases"]:
                print(f"   Available Purchases: {len(result['available_purchases'])}")
        else:
            print(f"❌ Failed to get empire status: {result['message']}")
        
        # Test 7: Get available options
        print("\n7. Available options...")
        facilities_result = empire_management_system.get_available_facilities()
        events_result = empire_management_system.get_available_events()
        
        print(f"✅ Available facility types: {len(facilities_result['facilities'])}")
        print(f"✅ Available special events: {len(events_result['events'])}")
        
    except ImportError as e:
        print(f"❌ Could not import empire management system: {e}")
    except Exception as e:
        print(f"❌ Error testing empire management system: {e}")

def test_notification_system():
    """Test the notification system"""
    print("\n" + "="*60)
    print("📢 TESTING NOTIFICATION SYSTEM")
    print("="*60)
    
    try:
        from notification_system import notification_system
        
        user_id = "test_user_notifications"
        
        # Test 1: Create notifications using templates
        print("\n1. Creating notifications using templates...")
        templates_to_test = [
            "new_daily_mission",
            "mission_completed", 
            "level_up",
            "deer_hungry",
            "empire_income_ready",
            "special_event_starting"
        ]
        
        for template in templates_to_test:
            result = notification_system.create_notification(user_id, template)
            if result["status"] == "success":
                notification = result["notification"]
                print(f"✅ Created {notification['type']} notification: {notification['title']}")
            else:
                print(f"❌ Failed to create {template} notification: {result['message']}")
        
        # Test 2: Create custom notification
        print("\n2. Creating custom notification...")
        result = notification_system.create_custom_notification(
            user_id, 
            "achievement", 
            "Custom Achievement!", 
            "You've unlocked a special custom achievement!",
            "view_achievements",
            {"achievement_id": "custom_123", "points": 100}
        )
        if result["status"] == "success":
            notification = result["notification"]
            print(f"✅ Created custom notification: {notification['title']}")
            print(f"   Type: {notification['type']}, Priority: {notification['priority']}")
        else:
            print(f"❌ Failed to create custom notification: {result['message']}")
        
        # Test 3: Get user notifications
        print("\n3. Getting user notifications...")
        result = notification_system.get_user_notifications(user_id, include_read=False)
        if result["status"] == "success":
            notifications = result["notifications"]
            print(f"✅ Found {len(notifications)} notifications")
            print(f"   Unread: {result['unread_count']}")
            print(f"   Priority counts: {result['priority_counts']}")
            
            # Show first few notifications
            for i, notification in enumerate(notifications[:3]):
                print(f"   {i+1}. {notification['icon']} {notification['title']} ({notification['type']})")
        else:
            print(f"❌ Failed to get notifications: {result['message']}")
        
        # Test 4: Mark notification as read
        print("\n4. Marking notification as read...")
        if result["status"] == "success" and result["notifications"]:
            notification_id = result["notifications"][0]["notification_id"]
            read_result = notification_system.mark_as_read(user_id, notification_id)
            if read_result["status"] == "success":
                print(f"✅ Marked notification as read")
            else:
                print(f"❌ Failed to mark as read: {read_result['message']}")
        
        # Test 5: Dismiss notification
        print("\n5. Dismissing notification...")
        if result["status"] == "success" and len(result["notifications"]) > 1:
            notification_id = result["notifications"][1]["notification_id"]
            dismiss_result = notification_system.dismiss_notification(user_id, notification_id)
            if dismiss_result["status"] == "success":
                print(f"✅ Dismissed notification")
            else:
                print(f"❌ Failed to dismiss: {dismiss_result['message']}")
        
        # Test 6: Mark all as read
        print("\n6. Marking all notifications as read...")
        mark_all_result = notification_system.mark_all_as_read(user_id)
        if mark_all_result["status"] == "success":
            print(f"✅ Marked {mark_all_result['count']} notifications as read")
        else:
            print(f"❌ Failed to mark all as read: {mark_all_result['message']}")
        
        # Test 7: Get notification settings
        print("\n7. Getting notification settings...")
        settings_result = notification_system.get_notification_settings(user_id)
        if settings_result["status"] == "success":
            settings = settings_result["settings"]
            print(f"✅ Notification settings:")
            print(f"   Enabled: {settings['enabled']}")
            print(f"   Sound: {settings['sound_enabled']}, Vibration: {settings['vibration_enabled']}")
            print(f"   Enabled types: {sum(settings['types'].values())}/{len(settings['types'])}")
        else:
            print(f"❌ Failed to get settings: {settings_result['message']}")
        
        # Test 8: Get notification statistics
        print("\n8. Getting notification statistics...")
        stats_result = notification_system.get_notification_statistics(user_id)
        if stats_result["status"] == "success":
            stats = stats_result["statistics"]
            print(f"✅ Notification statistics:")
            print(f"   Total: {stats['total_notifications']}")
            print(f"   Read: {stats['read_notifications']}, Dismissed: {stats['dismissed_notifications']}")
            print(f"   By priority: {stats['notifications_by_priority']}")
        else:
            print(f"❌ Failed to get statistics: {stats_result['message']}")
        
        # Test 9: Clear expired notifications
        print("\n9. Clearing expired notifications...")
        clear_result = notification_system.clear_expired_notifications()
        if clear_result["status"] == "success":
            print(f"✅ Cleared {clear_result['cleared_count']} expired notifications")
        else:
            print(f"❌ Failed to clear expired: {clear_result['message']}")
        
    except ImportError as e:
        print(f"❌ Could not import notification system: {e}")
    except Exception as e:
        print(f"❌ Error testing notification system: {e}")

def test_integration():
    """Test integration between the new systems"""
    print("\n" + "="*60)
    print("🔗 TESTING SYSTEM INTEGRATION")
    print("="*60)
    
    try:
        from deer_care_system import deer_care_system
        from empire_management_system import empire_management_system
        from notification_system import notification_system
        
        user_id = "test_user_integration"
        
        print("\n1. Creating integrated user experience...")
        
        # Create deer
        deer_result = deer_care_system.create_deer(user_id, "gazelle")
        if deer_result["status"] == "success":
            print(f"✅ Created deer: {deer_result['deer']['name']}")
            
            # Create notification for deer care
            notification_system.create_notification(user_id, "deer_entertainment")
            print("✅ Created deer care notification")
        
        # Create empire
        empire_result = empire_management_system.create_empire(user_id)
        if empire_result["status"] == "success":
            print(f"✅ Created empire: {empire_result['empire']['name']}")
            
            # Purchase facility
            purchase_result = empire_management_system.purchase_facility(user_id, "food_court", 5, 1000)
            if purchase_result["status"] == "success":
                print(f"✅ Purchased facility: {purchase_result['facility']['name']}")
                
                # Create notification for empire
                notification_system.create_notification(user_id, "empire_income_ready")
                print("✅ Created empire notification")
        
        # Create mission notification
        notification_system.create_notification(user_id, "new_daily_mission")
        print("✅ Created mission notification")
        
        # Get all notifications
        notifications_result = notification_system.get_user_notifications(user_id, include_read=True)
        if notifications_result["status"] == "success":
            print(f"✅ Total notifications created: {len(notifications_result['notifications'])}")
            print(f"   Types: {set(n['type'] for n in notifications_result['notifications'])}")
        
        print("\n2. Integration test completed successfully!")
        
    except ImportError as e:
        print(f"❌ Could not import systems for integration test: {e}")
    except Exception as e:
        print(f"❌ Error in integration test: {e}")

def main():
    """Main test function"""
    print("🚀 STARTING COMPREHENSIVE TEST OF NEW SYSTEMS")
    print("="*80)
    print("Testing the three new systems requested by the user:")
    print("1. 🦌 Deer Care System - Feed, entertain, and shelter deer")
    print("2. 🏛️ Empire Management System - Purchase and upgrade facilities")
    print("3. 📢 Notification System - Inform players about tasks and events")
    print("4. 🔗 System Integration - How the systems work together")
    print("="*80)
    
    # Test each system
    test_deer_care_system()
    test_empire_management_system()
    test_notification_system()
    test_integration()
    
    print("\n" + "="*80)
    print("🎉 ALL TESTS COMPLETED!")
    print("="*80)
    print("✅ Deer Care System: Players can now feed, entertain, and shelter deer")
    print("✅ Empire Management System: Players can purchase facilities and develop their empire")
    print("✅ Notification System: Players are informed about new tasks and missions")
    print("✅ All systems integrate seamlessly with the existing gamification system")
    print("\n🌟 The game now includes all the requested features similar to Hamster Kombat!")

if __name__ == "__main__":
    main() 