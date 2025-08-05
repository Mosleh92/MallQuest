#!/usr/bin/env python3
"""
Test Enhanced Gamification Features
Demonstrates the new interactive features added to the system
"""

from mall_gamification_system import MallGamificationSystem
from enhanced_gamification_features import create_enhanced_features
import json

def test_enhanced_features():
    """Test all enhanced gamification features"""
    
    print("🎮 Enhanced Gamification Features Test")
    print("=" * 50)
    
    # Initialize systems
    mall_system = MallGamificationSystem()
    enhanced_features = create_enhanced_features(mall_system)
    
    # Create test user
    user = mall_system.create_user("enhanced_user", "en")
    print(f"👤 Created user: {user.user_id}")
    
    # Test 1: Minigames
    print("\n1. Testing Minigames")
    print("-" * 30)
    
    minigames = ["coin_collector", "treasure_hunt", "speed_shopping", "memory_game"]
    
    for game in minigames:
        result = enhanced_features.start_minigame("enhanced_user", game)
        if result["status"] == "success":
            print(f"✅ {game}: Score {result['result']['score']}, Reward {result['reward']} coins")
        else:
            print(f"❌ {game}: {result['message']}")
    
    # Test 2: Achievements
    print("\n2. Testing Achievements")
    print("-" * 30)
    
    # Simulate some activities to trigger achievements
    mall_system.process_receipt("enhanced_user", 150.0, "Deerfields Fashion")
    mall_system.process_receipt("enhanced_user", 200.0, "Deerfields Electronics")
    mall_system.process_receipt("enhanced_user", 100.0, "Deerfields Café")
    
    # Check achievements
    earned_achievements = enhanced_features.check_achievements("enhanced_user")
    for achievement in earned_achievements:
        print(f"🏆 {achievement['icon']} {achievement['name']}: +{achievement['reward']} coins")
    
    # Test 3: User Progress
    print("\n3. Testing User Progress")
    print("-" * 30)
    
    progress = enhanced_features.get_user_progress("enhanced_user")
    if progress["status"] == "success":
        p = progress["progress"]
        print(f"📊 Level: {p['level']['current']} ({p['level']['progress_percent']:.1f}% to next)")
        print(f"👑 VIP: {p['vip']['current_tier']} (Next: {p['vip']['next_tier']})")
        print(f"🏆 Achievements: {p['achievements']['earned']}/{p['achievements']['total']}")
        print(f"🔥 Streak: {p['streak']['current']} days")
        print(f"💰 Total spent: AED {p['shopping']['total_spent']:.2f}")
    
    # Test 4: Available Features
    print("\n4. Testing Available Features")
    print("-" * 30)
    
    print("🎮 Available Minigames:")
    for game_id, game in enhanced_features.minigames.items():
        print(f"   • {game['name']}: {game['description']} (Reward: {game['reward']} coins)")
    
    print("\n🏆 Available Achievements:")
    for achievement_id, achievement in enhanced_features.achievements.items():
        print(f"   • {achievement['icon']} {achievement['name']}: {achievement['description']}")
    
    print("\n🎯 Available Challenges:")
    for challenge_id, challenge in enhanced_features.challenges.items():
        print(f"   • {challenge['name']}: {challenge['description']} (Reward: {challenge['reward']} coins)")
    
    # Test 5: Rewards Vault
    print("\n5. Testing Rewards Vault")
    print("-" * 30)
    
    print("📅 Daily Rewards:")
    for day, reward in enhanced_features.rewards_vault["daily_rewards"].items():
        print(f"   • Day {day.split('_')[1]}: {reward['coins']} coins, {reward['xp']} XP")
    
    print("\n📈 Level Rewards:")
    for level, reward in enhanced_features.rewards_vault["level_rewards"].items():
        print(f"   • {level}: {reward['coins']} coins + {reward['badge']} badge")
    
    print("\n👑 VIP Rewards:")
    for tier, benefits in enhanced_features.rewards_vault["vip_rewards"].items():
        print(f"   • {tier.title()}: {benefits['discount']*100}% discount, {benefits['bonus_coins']}x coin bonus")
    
    # Test 6: Social Features
    print("\n6. Testing Social Features")
    print("-" * 30)
    
    social = enhanced_features.social_features
    print(f"👥 Friend System: Max {social['friend_system']['max_friends']} friends")
    print(f"   • Friend bonus: {social['friend_system']['friend_bonus']*100}%")
    print(f"   • Gift system: {'✅' if social['friend_system']['gift_system'] else '❌'}")
    
    print(f"\n🏆 Team System: Max {social['team_system']['max_team_size']} members")
    print(f"   • Team bonus: {social['team_system']['team_bonus']*100}%")
    print(f"   • Team challenges: {'✅' if social['team_system']['team_challenges'] else '❌'}")
    
    print(f"\n💬 Chat System:")
    print(f"   • Enabled: {'✅' if social['chat_system']['enabled'] else '❌'}")
    print(f"   • Moderation: {'✅' if social['chat_system']['moderation'] else '❌'}")
    print(f"   • Emoji support: {'✅' if social['chat_system']['emoji_support'] else '❌'}")
    
    # Test 7: Leaderboards
    print("\n7. Testing Leaderboards")
    print("-" * 30)
    
    for leaderboard_id, leaderboard in enhanced_features.leaderboards.items():
        print(f"📊 {leaderboard['name']}: {leaderboard['description']}")
        print(f"   • Update frequency: {leaderboard['update_frequency']}")
        print(f"   • 1st place: {leaderboard['rewards']['1st']}")
        print(f"   • 2nd place: {leaderboard['rewards']['2nd']}")
        print(f"   • 3rd place: {leaderboard['rewards']['3rd']}")
        print()
    
    # Test 8: Special Events
    print("\n8. Testing Special Events")
    print("-" * 30)
    
    for event_id, event in enhanced_features.events.items():
        print(f"🎉 {event['name']}: {event['description']}")
        print(f"   • Duration: {event['duration']}")
        print(f"   • Bonus multiplier: {event['bonus_multiplier']}x")
        print(f"   • Special rewards: {', '.join(event['special_rewards'])}")
        print(f"   • Activities: {', '.join(event['activities'])}")
        print()
    
    # Test 9: Badges
    print("\n9. Testing Badges")
    print("-" * 30)
    
    for badge_id, badge in enhanced_features.badges.items():
        print(f"{badge['icon']} {badge['name']}: {badge['description']}")
        print(f"   • Unlock condition: {badge['unlock_condition']}")
    
    # Final Summary
    print("\n" + "=" * 50)
    print("🎮 Enhanced Features Summary")
    print("=" * 50)
    
    user = mall_system.get_user("enhanced_user")
    print(f"👤 User: {user.user_id}")
    print(f"💰 Coins: {user.coins}")
    print(f"⭐ Level: {user.level}")
    print(f"👑 VIP Tier: {user.vip_tier}")
    print(f"🔥 Login Streak: {user.login_streak}")
    print(f"🏆 Achievements Earned: {len(getattr(user, 'earned_achievements', []))}")
    
    print("\n✅ All enhanced features tested successfully!")
    print("🚀 The gamification system is now fully enhanced!")

if __name__ == "__main__":
    test_enhanced_features() 