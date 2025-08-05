#!/usr/bin/env python3
"""
Enhanced Gamification Features for Deerfields Mall
Adds advanced features to make the game more engaging and interactive
"""

import random
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from mall_gamification_system import MallGamificationSystem, User

class EnhancedGamificationFeatures:
    """Enhanced features to make the gamification system more engaging"""
    
    def __init__(self, mall_system: MallGamificationSystem):
        self.mall_system = mall_system
        self.minigames = {}
        self.achievements = {}
        self.badges = {}
        self.challenges = {}
        self.rewards_vault = {}
        self.social_features = {}
        self.leaderboards = {}
        self.events = {}
        self.initialize_enhanced_features()
    
    def initialize_enhanced_features(self):
        """Initialize all enhanced features"""
        self._setup_minigames()
        self._setup_achievements()
        self._setup_badges()
        self._setup_challenges()
        self._setup_rewards_vault()
        self._setup_social_features()
        self._setup_leaderboards()
        self._setup_events()
    
    def _setup_minigames(self):
        """Setup interactive minigames"""
        self.minigames = {
            "coin_collector": {
                "name": "Coin Collector",
                "description": "Collect falling coins in the mall",
                "reward": 50,
                "cooldown": 3600,  # 1 hour
                "difficulty": "easy",
                "location": "mall_center"
            },
            "treasure_hunt": {
                "name": "Treasure Hunt",
                "description": "Find hidden treasures in stores",
                "reward": 100,
                "cooldown": 7200,  # 2 hours
                "difficulty": "medium",
                "location": "various_stores"
            },
            "speed_shopping": {
                "name": "Speed Shopping",
                "description": "Complete shopping tasks quickly",
                "reward": 75,
                "cooldown": 1800,  # 30 minutes
                "difficulty": "hard",
                "location": "fashion_stores"
            },
            "memory_game": {
                "name": "Mall Memory",
                "description": "Remember store locations and items",
                "reward": 60,
                "cooldown": 2700,  # 45 minutes
                "difficulty": "medium",
                "location": "electronics_stores"
            }
        }
    
    def _setup_achievements(self):
        """Setup achievement system"""
        self.achievements = {
            "first_purchase": {
                "name": "First Purchase",
                "description": "Make your first purchase",
                "reward": 25,
                "icon": "🛍️",
                "category": "shopping"
            },
            "streak_master": {
                "name": "Streak Master",
                "description": "Maintain a 7-day login streak",
                "reward": 100,
                "icon": "🔥",
                "category": "engagement"
            },
            "big_spender": {
                "name": "Big Spender",
                "description": "Spend 1000 AED in one day",
                "reward": 200,
                "icon": "💰",
                "category": "shopping"
            },
            "explorer": {
                "name": "Mall Explorer",
                "description": "Visit 10 different stores",
                "reward": 150,
                "icon": "🗺️",
                "category": "exploration"
            },
            "social_butterfly": {
                "name": "Social Butterfly",
                "description": "Add 5 friends",
                "reward": 75,
                "icon": "🦋",
                "category": "social"
            },
            "mission_complete": {
                "name": "Mission Complete",
                "description": "Complete 10 missions",
                "reward": 300,
                "icon": "✅",
                "category": "missions"
            },
            "vip_status": {
                "name": "VIP Status",
                "description": "Reach Gold VIP tier",
                "reward": 500,
                "icon": "👑",
                "category": "vip"
            },
            "seasonal_champion": {
                "name": "Seasonal Champion",
                "description": "Participate in all seasonal events",
                "reward": 400,
                "icon": "🏆",
                "category": "events"
            }
        }
    
    def _setup_badges(self):
        """Setup badge system"""
        self.badges = {
            "newcomer": {
                "name": "Newcomer",
                "description": "Welcome to Deerfields Mall!",
                "icon": "🌟",
                "unlock_condition": "first_login"
            },
            "regular": {
                "name": "Regular Visitor",
                "description": "Visit the mall 5 times",
                "icon": "👥",
                "unlock_condition": "visit_count_5"
            },
            "shopper": {
                "name": "Smart Shopper",
                "description": "Make 10 purchases",
                "icon": "🛒",
                "unlock_condition": "purchase_count_10"
            },
            "collector": {
                "name": "Coin Collector",
                "description": "Earn 1000 coins",
                "icon": "🪙",
                "unlock_condition": "coins_1000"
            },
            "explorer": {
                "name": "Mall Explorer",
                "description": "Visit all store categories",
                "icon": "🗺️",
                "unlock_condition": "all_categories"
            },
            "social": {
                "name": "Social Star",
                "description": "Have 10 friends",
                "icon": "⭐",
                "unlock_condition": "friends_10"
            },
            "vip": {
                "name": "VIP Member",
                "description": "Reach Silver VIP tier",
                "icon": "💎",
                "unlock_condition": "silver_vip"
            },
            "champion": {
                "name": "Mall Champion",
                "description": "Complete all achievements",
                "icon": "🏆",
                "unlock_condition": "all_achievements"
            }
        }
    
    def _setup_challenges(self):
        """Setup challenge system"""
        self.challenges = {
            "daily_challenge": {
                "name": "Daily Challenge",
                "description": "Complete daily tasks for bonus rewards",
                "duration": "1_day",
                "reward": 100,
                "tasks": [
                    "Submit 3 receipts",
                    "Visit 5 stores",
                    "Earn 50 coins"
                ]
            },
            "weekly_challenge": {
                "name": "Weekly Challenge",
                "description": "Complete weekly goals for big rewards",
                "duration": "7_days",
                "reward": 500,
                "tasks": [
                    "Submit 15 receipts",
                    "Visit 20 stores",
                    "Earn 300 coins",
                    "Complete 5 missions"
                ]
            },
            "monthly_challenge": {
                "name": "Monthly Challenge",
                "description": "Achieve monthly milestones",
                "duration": "30_days",
                "reward": 2000,
                "tasks": [
                    "Submit 50 receipts",
                    "Visit 50 stores",
                    "Earn 1000 coins",
                    "Complete 20 missions",
                    "Reach level 10"
                ]
            }
        }
    
    def _setup_rewards_vault(self):
        """Setup rewards vault system"""
        self.rewards_vault = {
            "daily_rewards": {
                "day_1": {"coins": 10, "xp": 20},
                "day_2": {"coins": 15, "xp": 25},
                "day_3": {"coins": 20, "xp": 30},
                "day_4": {"coins": 25, "xp": 35},
                "day_5": {"coins": 30, "xp": 40},
                "day_6": {"coins": 35, "xp": 45},
                "day_7": {"coins": 100, "xp": 100, "bonus": "special_item"}
            },
            "level_rewards": {
                "level_5": {"coins": 200, "badge": "regular"},
                "level_10": {"coins": 500, "badge": "shopper"},
                "level_15": {"coins": 1000, "badge": "collector"},
                "level_20": {"coins": 2000, "badge": "explorer"},
                "level_25": {"coins": 3000, "badge": "social"},
                "level_30": {"coins": 5000, "badge": "vip"},
                "level_50": {"coins": 10000, "badge": "champion"}
            },
            "vip_rewards": {
                "bronze": {"discount": 0.05, "bonus_coins": 1.1},
                "silver": {"discount": 0.10, "bonus_coins": 1.2},
                "gold": {"discount": 0.15, "bonus_coins": 1.3},
                "platinum": {"discount": 0.20, "bonus_coins": 1.5}
            }
        }
    
    def _setup_social_features(self):
        """Setup social features"""
        self.social_features = {
            "friend_system": {
                "max_friends": 50,
                "friend_bonus": 0.05,  # 5% bonus when shopping with friends
                "gift_system": True,
                "friend_challenges": True
            },
            "team_system": {
                "max_team_size": 10,
                "team_bonus": 0.10,  # 10% bonus for team activities
                "team_challenges": True,
                "team_leaderboards": True
            },
            "chat_system": {
                "enabled": True,
                "moderation": True,
                "emoji_support": True,
                "voice_messages": False
            }
        }
    
    def _setup_leaderboards(self):
        """Setup leaderboards"""
        self.leaderboards = {
            "coins": {
                "name": "Coin Leaderboard",
                "description": "Top coin earners",
                "update_frequency": "daily",
                "rewards": {
                    "1st": {"coins": 1000, "badge": "coin_king"},
                    "2nd": {"coins": 500, "badge": "coin_prince"},
                    "3rd": {"coins": 250, "badge": "coin_noble"}
                }
            },
            "xp": {
                "name": "XP Leaderboard",
                "description": "Top experience earners",
                "update_frequency": "daily",
                "rewards": {
                    "1st": {"xp": 1000, "badge": "xp_master"},
                    "2nd": {"xp": 500, "badge": "xp_expert"},
                    "3rd": {"xp": 250, "badge": "xp_learner"}
                }
            },
            "streak": {
                "name": "Streak Leaderboard",
                "description": "Longest login streaks",
                "update_frequency": "weekly",
                "rewards": {
                    "1st": {"coins": 500, "badge": "streak_legend"},
                    "2nd": {"coins": 250, "badge": "streak_champion"},
                    "3rd": {"coins": 100, "badge": "streak_warrior"}
                }
            },
            "spending": {
                "name": "Spending Leaderboard",
                "description": "Top spenders",
                "update_frequency": "monthly",
                "rewards": {
                    "1st": {"vip_points": 1000, "badge": "big_spender"},
                    "2nd": {"vip_points": 500, "badge": "generous_shopper"},
                    "3rd": {"vip_points": 250, "badge": "loyal_customer"}
                }
            }
        }
    
    def _setup_events(self):
        """Setup special events"""
        self.events = {
            "ramadan": {
                "name": "Ramadan Special",
                "description": "Special rewards during Ramadan",
                "duration": "30_days",
                "bonus_multiplier": 2.0,
                "special_rewards": ["Iftar Vouchers", "Ramadan Coins", "Charity Points"],
                "activities": ["daily_prayer", "charity_donation", "family_shopping"]
            },
            "national_day": {
                "name": "UAE National Day",
                "description": "Celebrate UAE National Day",
                "duration": "3_days",
                "bonus_multiplier": 1.5,
                "special_rewards": ["UAE Flag Items", "National Pride Coins", "Heritage Badges"],
                "activities": ["flag_collection", "heritage_quiz", "patriotic_shopping"]
            },
            "summer_sale": {
                "name": "Summer Sale",
                "description": "Biggest sale of the year",
                "duration": "14_days",
                "bonus_multiplier": 1.3,
                "special_rewards": ["Summer Coins", "Beach Items", "Travel Vouchers"],
                "activities": ["beach_theme", "travel_planning", "summer_shopping"]
            },
            "back_to_school": {
                "name": "Back to School",
                "description": "Prepare for the new school year",
                "duration": "21_days",
                "bonus_multiplier": 1.2,
                "special_rewards": ["School Supplies", "Education Coins", "Study Badges"],
                "activities": ["school_shopping", "education_quiz", "study_preparation"]
            }
        }
    
    def start_minigame(self, user_id: str, game_name: str) -> Dict[str, Any]:
        """Start a minigame for a user"""
        try:
            if game_name not in self.minigames:
                return {"status": "error", "message": "Minigame not found"}
            
            game = self.minigames[game_name]
            user = self.mall_system.get_user(user_id)
            
            if not user:
                return {"status": "error", "message": "User not found"}
            
            # Check cooldown
            last_played = getattr(user, f'last_played_{game_name}', None)
            if last_played and time.time() - last_played < game['cooldown']:
                remaining = game['cooldown'] - (time.time() - last_played)
                return {"status": "error", "message": f"Game on cooldown. Try again in {int(remaining/60)} minutes"}
            
            # Start game
            game_result = self._play_minigame(game_name, user)
            
            # Update user stats
            setattr(user, f'last_played_{game_name}', time.time())
            
            return {
                "status": "success",
                "game": game_name,
                "result": game_result,
                "reward": game['reward'],
                "message": f"Completed {game['name']}!"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error starting minigame: {str(e)}"}
    
    def _play_minigame(self, game_name: str, user: User) -> Dict[str, Any]:
        """Simulate playing a minigame"""
        if game_name == "coin_collector":
            return self._play_coin_collector(user)
        elif game_name == "treasure_hunt":
            return self._play_treasure_hunt(user)
        elif game_name == "speed_shopping":
            return self._play_speed_shopping(user)
        elif game_name == "memory_game":
            return self._play_memory_game(user)
        else:
            return {"score": 0, "completed": False}
    
    def _play_coin_collector(self, user: User) -> Dict[str, Any]:
        """Play coin collector minigame"""
        # Simulate coin collection
        coins_collected = random.randint(10, 50)
        score = coins_collected * 10
        
        # Add coins to user
        user.coins += coins_collected
        
        return {
            "score": score,
            "coins_collected": coins_collected,
            "completed": True,
            "performance": "excellent" if score > 300 else "good" if score > 200 else "average"
        }
    
    def _play_treasure_hunt(self, user: User) -> Dict[str, Any]:
        """Play treasure hunt minigame"""
        # Simulate treasure hunting
        treasures_found = random.randint(3, 8)
        score = treasures_found * 25
        
        # Add XP to user
        user.add_xp(treasures_found * 10)
        
        return {
            "score": score,
            "treasures_found": treasures_found,
            "completed": True,
            "performance": "excellent" if treasures_found > 6 else "good" if treasures_found > 4 else "average"
        }
    
    def _play_speed_shopping(self, user: User) -> Dict[str, Any]:
        """Play speed shopping minigame"""
        # Simulate speed shopping
        tasks_completed = random.randint(2, 5)
        time_taken = random.randint(30, 120)  # seconds
        score = (tasks_completed * 100) - time_taken
        
        # Add coins to user
        user.coins += tasks_completed * 15
        
        return {
            "score": max(0, score),
            "tasks_completed": tasks_completed,
            "time_taken": time_taken,
            "completed": True,
            "performance": "excellent" if score > 300 else "good" if score > 200 else "average"
        }
    
    def _play_memory_game(self, user: User) -> Dict[str, Any]:
        """Play memory game minigame"""
        # Simulate memory game
        correct_matches = random.randint(5, 12)
        total_attempts = random.randint(8, 15)
        score = (correct_matches * 20) - (total_attempts - correct_matches) * 5
        
        # Add XP to user
        user.add_xp(correct_matches * 5)
        
        return {
            "score": max(0, score),
            "correct_matches": correct_matches,
            "total_attempts": total_attempts,
            "completed": True,
            "performance": "excellent" if correct_matches > 10 else "good" if correct_matches > 7 else "average"
        }
    
    def check_achievements(self, user_id: str) -> List[Dict[str, Any]]:
        """Check and award achievements for a user"""
        try:
            user = self.mall_system.get_user(user_id)
            if not user:
                return []
            
            earned_achievements = []
            
            # Check each achievement
            for achievement_id, achievement in self.achievements.items():
                if self._check_achievement_condition(user, achievement_id):
                    if achievement_id not in getattr(user, 'earned_achievements', []):
                        # Award achievement
                        user.coins += achievement['reward']
                        user.add_xp(achievement['reward'] // 2)
                        
                        if not hasattr(user, 'earned_achievements'):
                            user.earned_achievements = []
                        user.earned_achievements.append(achievement_id)
                        
                        earned_achievements.append({
                            "id": achievement_id,
                            "name": achievement['name'],
                            "description": achievement['description'],
                            "reward": achievement['reward'],
                            "icon": achievement['icon']
                        })
            
            return earned_achievements
            
        except Exception as e:
            print(f"Error checking achievements: {e}")
            return []
    
    def _check_achievement_condition(self, user: User, achievement_id: str) -> bool:
        """Check if user meets achievement condition"""
        if achievement_id == "first_purchase":
            return len(user.purchase_history) >= 1
        elif achievement_id == "streak_master":
            return user.login_streak >= 7
        elif achievement_id == "big_spender":
            return user.total_spent >= 1000
        elif achievement_id == "explorer":
            return len(set(p.get('category', '') for p in user.purchase_history)) >= 10
        elif achievement_id == "social_butterfly":
            return len(getattr(user, 'friends', [])) >= 5
        elif achievement_id == "mission_complete":
            return len(getattr(user, 'completed_missions', [])) >= 10
        elif achievement_id == "vip_status":
            return user.vip_tier == "Gold"
        elif achievement_id == "seasonal_champion":
            return len(getattr(user, 'participated_events', [])) >= 4
        
        return False
    
    def get_user_progress(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user progress"""
        try:
            user = self.mall_system.get_user(user_id)
            if not user:
                return {"status": "error", "message": "User not found"}
            
            # Calculate progress for various systems
            progress = {
                "level": {
                    "current": user.level,
                    "xp": user.xp,
                    "xp_needed": user.level * 100,
                    "progress_percent": (user.xp / (user.level * 100)) * 100
                },
                "vip": {
                    "current_tier": user.vip_tier,
                    "vip_points": user.vip_points,
                    "next_tier": self._get_next_vip_tier(user.vip_tier),
                    "points_needed": self._get_vip_points_needed(user.vip_tier)
                },
                "achievements": {
                    "earned": len(getattr(user, 'earned_achievements', [])),
                    "total": len(self.achievements),
                    "progress_percent": (len(getattr(user, 'earned_achievements', [])) / len(self.achievements)) * 100
                },
                "badges": {
                    "earned": len(getattr(user, 'earned_badges', [])),
                    "total": len(self.badges),
                    "progress_percent": (len(getattr(user, 'earned_badges', [])) / len(self.badges)) * 100
                },
                "streak": {
                    "current": user.login_streak,
                    "max": user.max_streak,
                    "next_reward": self._get_next_streak_reward(user.login_streak)
                },
                "shopping": {
                    "total_spent": user.total_spent,
                    "total_purchases": user.total_purchases,
                    "average_spend": user.total_spent / max(user.total_purchases, 1)
                }
            }
            
            return {
                "status": "success",
                "progress": progress
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error getting user progress: {str(e)}"}
    
    def _get_next_vip_tier(self, current_tier: str) -> str:
        """Get next VIP tier"""
        tiers = ["Bronze", "Silver", "Gold", "Platinum"]
        try:
            current_index = tiers.index(current_tier)
            if current_index < len(tiers) - 1:
                return tiers[current_index + 1]
        except ValueError:
            pass
        return "Max"
    
    def _get_vip_points_needed(self, current_tier: str) -> int:
        """Get VIP points needed for next tier"""
        points_needed = {
            "Bronze": 1000,
            "Silver": 2500,
            "Gold": 5000,
            "Platinum": 10000
        }
        return points_needed.get(current_tier, 0)
    
    def _get_next_streak_reward(self, current_streak: int) -> Dict[str, Any]:
        """Get next streak reward"""
        rewards = {
            3: {"coins": 50, "xp": 100},
            7: {"coins": 100, "xp": 200},
            14: {"coins": 200, "xp": 400},
            30: {"coins": 500, "xp": 1000}
        }
        
        for days, reward in rewards.items():
            if current_streak < days:
                return {"days_needed": days - current_streak, "reward": reward}
        
        return {"days_needed": 0, "reward": {"coins": 100, "xp": 200}}

# Create enhanced features instance
def create_enhanced_features(mall_system: MallGamificationSystem) -> EnhancedGamificationFeatures:
    """Create enhanced gamification features"""
    return EnhancedGamificationFeatures(mall_system) 