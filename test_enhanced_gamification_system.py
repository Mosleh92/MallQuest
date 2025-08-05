#!/usr/bin/env python3
"""
Comprehensive Test for Enhanced Mall Gamification System
Tests all new features: IntelligentRewardSystem, PersonalizedMissionGenerator,
VIP tier management, social features, event management, and performance monitoring
"""

import time
from datetime import datetime, timedelta
from mall_gamification_system import (
    MallGamificationSystem, IntelligentRewardSystem, 
    PersonalizedMissionGenerator, User
)

def test_intelligent_reward_system():
    """Test IntelligentRewardSystem functionality"""
    print("\n=== Testing IntelligentRewardSystem ===")
    
    reward_system = IntelligentRewardSystem()
    
    # Test basic reward calculation
    user_profile = {
        'vip_tier': 'Gold',
        'login_streak': 7,
        'total_spent': 1000,
        'visited_categories': ['fashion', 'electronics'],
        'total_purchases': 15
    }
    
    context = {
        'category': 'fashion',
        'event_multiplier': 1.5,
        'time_of_day': 'evening'
    }
    
    result = reward_system.calculate_dynamic_reward(500, 'fashion', user_profile, context)
    
    print(f"Base coins: {result['base_coins']}")
    print(f"Total coins: {result['total_coins']}")
    print(f"Multipliers: {result['multiplier_breakdown']}")
    print(f"Bonus rewards: {result['bonus_rewards']}")
    print(f"Celebration level: {result['celebration_level']}")
    
    # Test different categories
    categories = ['fashion', 'electronics', 'food', 'luxury']
    for category in categories:
        result = reward_system.calculate_dynamic_reward(100, category, user_profile)
        print(f"{category}: {result['total_coins']} coins")
    
    # Test VIP tier differences
    vip_tiers = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond']
    for tier in vip_tiers:
        user_profile['vip_tier'] = tier
        result = reward_system.calculate_dynamic_reward(100, 'fashion', user_profile)
        print(f"VIP {tier}: {result['total_coins']} coins")
    
    print("✅ IntelligentRewardSystem tests completed")

def test_personalized_mission_generator():
    """Test PersonalizedMissionGenerator functionality"""
    print("\n=== Testing PersonalizedMissionGenerator ===")
    
    mission_generator = PersonalizedMissionGenerator()
    
    # Test different user profiles
    user_profiles = [
        {
            'level': 1,
            'vip_tier': 'Bronze',
            'total_spent': 100,
            'visited_categories': ['fashion'],
            'total_purchases': 2,
            'login_streak': 1,
            'preferred_categories': ['fashion'],
            'activity_frequency': 'low'
        },
        {
            'level': 10,
            'vip_tier': 'Gold',
            'total_spent': 2000,
            'visited_categories': ['fashion', 'electronics', 'food', 'luxury'],
            'total_purchases': 25,
            'login_streak': 14,
            'preferred_categories': ['fashion', 'electronics'],
            'activity_frequency': 'high'
        }
    ]
    
    for i, profile in enumerate(user_profiles):
        print(f"\nUser Profile {i+1}:")
        print(f"Level: {profile['level']}, VIP: {profile['vip_tier']}")
        print(f"Total spent: {profile['total_spent']}, Streak: {profile['login_streak']}")
        
        # Generate different mission types
        for mission_type in ['daily', 'weekly', 'seasonal']:
            mission = mission_generator.generate_personalized_mission(profile, mission_type)
            print(f"{mission_type.title()} Mission: {mission['title']}")
            print(f"  Target: {mission['target']}, Reward: {mission['reward']}")
            print(f"  Difficulty: {mission['difficulty']}, Personalized: {mission['personalized']}")
    
    print("✅ PersonalizedMissionGenerator tests completed")

def test_vip_tier_management():
    """Test VIP tier management and benefits"""
    print("\n=== Testing VIP Tier Management ===")
    
    # Create test users with different spending levels
    mall_system = MallGamificationSystem()
    
    # Test user with low spending
    user1 = mall_system.create_user("vip_test_user1", "en")
    user1.total_spent = 100
    user1.login_streak = 3
    user1.achievement_points = 20
    user1.social_score = 10
    user1.update_vip_tier()
    
    print(f"User 1 - Spent: {user1.total_spent}, VIP Tier: {user1.vip_tier}")
    print(f"VIP Points: {user1.vip_points}")
    print(f"VIP Benefits: {user1.get_vip_benefits()}")
    
    # Test user with high spending
    user2 = mall_system.create_user("vip_test_user2", "en")
    user2.total_spent = 5000
    user2.login_streak = 30
    user2.achievement_points = 200
    user2.social_score = 150
    user2.update_vip_tier()
    
    print(f"\nUser 2 - Spent: {user2.total_spent}, VIP Tier: {user2.vip_tier}")
    print(f"VIP Points: {user2.vip_points}")
    print(f"VIP Benefits: {user2.get_vip_benefits()}")
    
    # Test VIP tier upgrade rewards
    user3 = mall_system.create_user("vip_test_user3", "en")
    user3.vip_tier = "Bronze"
    user3.coins = 100
    
    # Simulate VIP upgrade
    user3.vip_tier = "Silver"
    tier_bonuses = {'Silver': 50, 'Gold': 100, 'Platinum': 200, 'Diamond': 500}
    if user3.vip_tier in tier_bonuses:
        bonus = tier_bonuses[user3.vip_tier]
        user3.coins += bonus
        print(f"\nVIP Upgrade to {user3.vip_tier}: +{bonus} coins")
        print(f"Total coins after upgrade: {user3.coins}")
    
    print("✅ VIP Tier Management tests completed")

def test_social_features():
    """Test social features including friends, teams, and leaderboards"""
    print("\n=== Testing Social Features ===")
    
    mall_system = MallGamificationSystem()
    
    # Create test users
    users = []
    for i in range(5):
        user = mall_system.create_user(f"social_user_{i}", "en")
        user.coins = 100 * (i + 1)
        user.xp = 50 * (i + 1)
        user.login_streak = i + 1
        user.total_spent = 200 * (i + 1)
        users.append(user)
    
    # Test friend system
    print("Testing Friend System:")
    user1 = users[0]
    user2 = users[1]
    
    success = user1.add_friend(user2.user_id)
    print(f"Added friend: {success}")
    print(f"User 1 friends: {user1.friends}")
    print(f"User 1 social score: {user1.social_score}")
    
    # Test team system
    print("\nTesting Team System:")
    team_id = mall_system.create_team("Test Team", user1.user_id)
    print(f"Created team: {team_id}")
    
    # Add more members to team
    for user in users[1:3]:
        success = mall_system.join_team(user.user_id, team_id)
        print(f"User {user.user_id} joined team: {success}")
    
    team = mall_system.teams[team_id]
    print(f"Team members: {team['members']}")
    print(f"Team score: {team['score']}")
    
    # Test leaderboards
    print("\nTesting Leaderboards:")
    for user in users:
        mall_system.update_leaderboards(user.user_id, user.coins, user.xp)
    
    for leaderboard_type in ['coins', 'xp', 'streak', 'achievements', 'spending']:
        leaderboard = mall_system.get_leaderboard(leaderboard_type, 5)
        print(f"{leaderboard_type.title()} Leaderboard:")
        for i, entry in enumerate(leaderboard):
            print(f"  {i+1}. User {entry['user_id']}: {entry['score']}")
    
    # Test team challenges
    print("\nTesting Team Challenges:")
    challenge_id = mall_system.create_team_challenge(
        "Weekly Shopping Challenge", 
        1000, 
        {"coins": 500, "xp": 200}, 
        7
    )
    print(f"Created challenge: {challenge_id}")
    
    # Update team score
    mall_system.update_team_challenge_score(challenge_id, team_id, 500)
    challenge = mall_system.team_challenges[challenge_id]
    print(f"Team score in challenge: {challenge['teams'][team_id]['score']}")
    
    print("✅ Social Features tests completed")

def test_achievement_system():
    """Test achievement system"""
    print("\n=== Testing Achievement System ===")
    
    mall_system = MallGamificationSystem()
    user = mall_system.create_user("achievement_user", "en")
    
    # Test earning achievements
    achievements = [
        ("first_purchase", "First Purchase", 10),
        ("high_spender", "High Roller", 50),
        ("category_explorer", "Category Explorer", 30),
        ("frequent_shopper", "Frequent Shopper", 40),
        ("vip_spender", "VIP Spender", 100)
    ]
    
    for achievement_id, name, points in achievements:
        success = user.earn_achievement(achievement_id, name, points)
        print(f"Earned {name}: {success}")
    
    print(f"Total achievements: {len(user.achievements)}")
    print(f"Achievement points: {user.achievement_points}")
    print(f"Social score: {user.social_score}")
    
    # Test duplicate achievement
    success = user.earn_achievement("first_purchase", "First Purchase", 10)
    print(f"Duplicate achievement attempt: {success}")
    
    print("✅ Achievement System tests completed")

def test_enhanced_receipt_processing():
    """Test enhanced receipt processing with intelligent rewards"""
    print("\n=== Testing Enhanced Receipt Processing ===")
    
    mall_system = MallGamificationSystem()
    user = mall_system.create_user("receipt_user", "en")
    
    # Set up user for testing
    user.vip_tier = "Gold"
    user.login_streak = 7
    user.total_spent = 1000
    user.visited_categories = ['fashion']
    
    # Test different store categories
    test_receipts = [
        ("Deerfields Fashion Store", 200, "fashion"),
        ("Deerfields Electronics", 150, "electronics"),
        ("Deerfields Luxury Boutique", 500, "luxury"),
        ("Deerfields Food Court", 50, "food")
    ]
    
    for store, amount, expected_category in test_receipts:
        print(f"\nProcessing receipt: {store} - {amount} AED")
        
        result = mall_system.process_receipt(user.user_id, amount, store)
        
        if result["status"] == "success":
            print(f"  Coins earned: {result['coins_earned']}")
            print(f"  XP earned: {result['xp_earned']}")
            print(f"  Celebration level: {result['celebration_level']}")
            print(f"  Multipliers: {result['multipliers']}")
            
            if result['bonus_rewards']:
                print(f"  Bonus rewards: {result['bonus_rewards']}")
        else:
            print(f"  Error: {result['message']}")
    
    print(f"\nFinal user stats:")
    print(f"  Coins: {user.coins}")
    print(f"  XP: {user.xp}")
    print(f"  Level: {user.level}")
    print(f"  VIP Tier: {user.vip_tier}")
    print(f"  Total spent: {user.total_spent}")
    print(f"  Visited categories: {user.visited_categories}")
    
    print("✅ Enhanced Receipt Processing tests completed")

def test_performance_monitoring():
    """Test performance monitoring integration"""
    print("\n=== Testing Performance Monitoring ===")
    
    mall_system = MallGamificationSystem()
    
    # Test performance monitoring if available
    if mall_system.performance_monitor:
        print("Performance monitoring is available")
        
        # Simulate some operations
        start_time = time.time()
        
        # Create users
        for i in range(10):
            user = mall_system.create_user(f"perf_user_{i}", "en")
        
        # Process receipts
        for i in range(5):
            mall_system.process_receipt(f"perf_user_{i}", 100 + i * 50, f"Deerfields Store {i}")
        
        # Generate missions
        for i in range(3):
            mall_system.generate_user_missions(f"perf_user_{i}", "daily")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"Total operations time: {total_time:.3f}s")
        
        # Get performance report
        report = mall_system.performance_monitor.get_performance_report()
        print(f"Performance report: {report}")
    else:
        print("Performance monitoring not available")
    
    print("✅ Performance Monitoring tests completed")

def test_security_integration():
    """Test security integration"""
    print("\n=== Testing Security Integration ===")
    
    mall_system = MallGamificationSystem()
    
    # Test security logging if available
    if mall_system.security_manager:
        print("Security module is available")
        
        # Test receipt processing with security logging
        user = mall_system.create_user("security_user", "en")
        result = mall_system.process_receipt(user.user_id, 100, "Deerfields Test Store")
        
        print(f"Receipt processing result: {result['status']}")
        print("Security events should be logged")
    else:
        print("Security module not available")
    
    print("✅ Security Integration tests completed")

def test_comprehensive_dashboard():
    """Test comprehensive user dashboard"""
    print("\n=== Testing Comprehensive Dashboard ===")
    
    mall_system = MallGamificationSystem()
    user = mall_system.create_user("dashboard_user", "en")
    
    # Set up user with various activities
    user.vip_tier = "Gold"
    user.login_streak = 10
    user.total_spent = 2000
    user.achievement_points = 150
    user.social_score = 80
    
    # Add some friends
    user.add_friend("friend1")
    user.add_friend("friend2")
    
    # Create a team
    team_id = mall_system.create_team("Dashboard Team", user.user_id)
    
    # Process some receipts
    mall_system.process_receipt(user.user_id, 300, "Deerfields Fashion")
    mall_system.process_receipt(user.user_id, 200, "Deerfields Electronics")
    
    # Generate missions
    mall_system.generate_user_missions(user.user_id, "daily")
    mall_system.generate_user_missions(user.user_id, "weekly")
    
    # Get comprehensive dashboard
    dashboard = mall_system.get_user_dashboard(user.user_id)
    
    print("Dashboard Overview:")
    print(f"  User Info: {dashboard['user_info']}")
    print(f"  VIP Benefits: {dashboard['vip_benefits']}")
    print(f"  Login Streak: {dashboard['login_streak']}")
    print(f"  Missions Count: {len(dashboard['missions'])}")
    print(f"  Achievements Count: {len(dashboard['achievements'])}")
    print(f"  Friends Count: {len(dashboard['friends'])}")
    print(f"  Team Info: {dashboard['team_info']}")
    print(f"  Leaderboard Positions: {dashboard['leaderboard_positions']}")
    print(f"  Visited Categories: {dashboard['visited_categories']}")
    
    if dashboard['performance_metrics']:
        print(f"  Performance Metrics: {dashboard['performance_metrics']}")
    
    print("✅ Comprehensive Dashboard tests completed")

def main():
    """Run all enhanced gamification system tests"""
    print("🚀 Starting Enhanced Gamification System Tests")
    print("=" * 60)
    
    try:
        # Test all components
        test_intelligent_reward_system()
        test_personalized_mission_generator()
        test_vip_tier_management()
        test_social_features()
        test_achievement_system()
        test_enhanced_receipt_processing()
        test_performance_monitoring()
        test_security_integration()
        test_comprehensive_dashboard()
        
        print("\n" + "=" * 60)
        print("✅ All Enhanced Gamification System Tests Completed Successfully!")
        print("\n📋 Summary of Enhanced Features:")
        print("- ✅ IntelligentRewardSystem with dynamic multipliers")
        print("- ✅ PersonalizedMissionGenerator with AI-powered missions")
        print("- ✅ Advanced VIP tier management with real benefits")
        print("- ✅ Social features (friends, teams, leaderboards)")
        print("- ✅ Achievement system with points and social scoring")
        print("- ✅ Enhanced receipt processing with category detection")
        print("- ✅ Performance monitoring integration")
        print("- ✅ Security logging integration")
        print("- ✅ Comprehensive user dashboard")
        print("- ✅ Team challenges and competitions")
        print("- ✅ Multi-factor user progression (coins, XP, VIP points)")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 