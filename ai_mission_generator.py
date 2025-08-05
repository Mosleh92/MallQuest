#!/usr/bin/env python3
"""
AI Mission Generator for Deerfields Mall Gamification System
Creates personalized missions based on user behavior and mall activities
"""

import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from database import db

class AIMissionGenerator:
    """AI-powered mission generator for personalized user experiences"""
    
    def __init__(self):
        self.mission_templates = self._load_mission_templates()
        self.user_patterns = {}
        self.mall_zones = [
            "Fashion", "Electronics", "Food", "Beauty", "Sports", 
            "Home", "Entertainment", "Kids", "Luxury", "Services"
        ]
        self.mission_types = [
            "receipt_scan", "store_visit", "spending", "social", 
            "exploration", "collection", "challenge", "daily"
        ]
    
    def _load_mission_templates(self) -> Dict[str, List[Dict]]:
        """Load mission templates from configuration"""
        return {
            "receipt_scan": [
                {
                    "title": "🧾 Scan {count} Receipts",
                    "description": "Submit {count} valid receipts from any store",
                    "base_reward_coins": 15,
                    "base_reward_xp": 30,
                    "difficulty_multiplier": 1.2
                },
                {
                    "title": "🏪 {store_type} Shopping Spree",
                    "description": "Scan receipts from {store_type} stores",
                    "base_reward_coins": 20,
                    "base_reward_xp": 40,
                    "difficulty_multiplier": 1.5
                }
            ],
            "store_visit": [
                {
                    "title": "🛍️ Explore {zone} Zone",
                    "description": "Visit {count} different stores in the {zone} zone",
                    "base_reward_coins": 25,
                    "base_reward_xp": 50,
                    "difficulty_multiplier": 1.3
                },
                {
                    "title": "🎯 Brand Hunter",
                    "description": "Visit {brand} store and explore their latest collection",
                    "base_reward_coins": 30,
                    "base_reward_xp": 60,
                    "difficulty_multiplier": 1.4
                }
            ],
            "spending": [
                {
                    "title": "💰 Big Spender",
                    "description": "Spend AED {amount} in {category} stores",
                    "base_reward_coins": 50,
                    "base_reward_xp": 100,
                    "difficulty_multiplier": 1.8
                },
                {
                    "title": "🎁 Gift Shopping",
                    "description": "Purchase gifts worth AED {amount} from any store",
                    "base_reward_coins": 40,
                    "base_reward_xp": 80,
                    "difficulty_multiplier": 1.6
                }
            ],
            "social": [
                {
                    "title": "👥 Social Butterfly",
                    "description": "Invite {count} friends to join the mall experience",
                    "base_reward_coins": 35,
                    "base_reward_xp": 70,
                    "difficulty_multiplier": 1.7
                },
                {
                    "title": "📸 Photo Challenge",
                    "description": "Take photos with {count} different store displays",
                    "base_reward_coins": 20,
                    "base_reward_xp": 40,
                    "difficulty_multiplier": 1.2
                }
            ],
            "exploration": [
                {
                    "title": "🗺️ Mall Explorer",
                    "description": "Visit {count} different mall zones",
                    "base_reward_coins": 30,
                    "base_reward_xp": 60,
                    "difficulty_multiplier": 1.4
                },
                {
                    "title": "🎮 Arcade Adventure",
                    "description": "Play {count} different arcade games",
                    "base_reward_coins": 25,
                    "base_reward_xp": 50,
                    "difficulty_multiplier": 1.3
                }
            ],
            "collection": [
                {
                    "title": "🏆 Collection Master",
                    "description": "Collect {count} different store stamps",
                    "base_reward_coins": 45,
                    "base_reward_xp": 90,
                    "difficulty_multiplier": 1.6
                },
                {
                    "title": "🎨 Color Collector",
                    "description": "Visit stores with {color} themed displays",
                    "base_reward_coins": 20,
                    "base_reward_xp": 40,
                    "difficulty_multiplier": 1.2
                }
            ],
            "challenge": [
                {
                    "title": "⚡ Speed Shopper",
                    "description": "Complete shopping in {time_limit} minutes",
                    "base_reward_coins": 60,
                    "base_reward_xp": 120,
                    "difficulty_multiplier": 2.0
                },
                {
                    "title": "🎯 Precision Shopper",
                    "description": "Spend exactly AED {target_amount} (within AED 10)",
                    "base_reward_coins": 70,
                    "base_reward_xp": 140,
                    "difficulty_multiplier": 2.2
                }
            ],
            "daily": [
                {
                    "title": "🌅 Daily Login",
                    "description": "Log in to the mall app today",
                    "base_reward_coins": 10,
                    "base_reward_xp": 20,
                    "difficulty_multiplier": 1.0
                },
                {
                    "title": "📱 App Explorer",
                    "description": "Use {count} different app features today",
                    "base_reward_coins": 15,
                    "base_reward_xp": 30,
                    "difficulty_multiplier": 1.1
                }
            ]
        }
    
    def analyze_user_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analyze user behavior patterns for mission personalization"""
        try:
            # Get user data
            user = db.get_user(user_id)
            if not user:
                return {}
            
            # Get user activities
            activities = db.get_user_activities(user_id, limit=50)
            receipts = db.get_user_receipts(user_id, limit=20)
            missions = db.get_user_missions(user_id, status='completed')
            
            patterns = {
                "favorite_zones": self._analyze_favorite_zones(activities, receipts),
                "spending_patterns": self._analyze_spending_patterns(receipts),
                "activity_frequency": self._analyze_activity_frequency(activities),
                "mission_preferences": self._analyze_mission_preferences(missions),
                "social_engagement": self._analyze_social_engagement(activities),
                "exploration_level": self._analyze_exploration_level(activities),
                "skill_level": self._calculate_skill_level(user, activities, missions)
            }
            
            self.user_patterns[user_id] = patterns
            return patterns
            
        except Exception as e:
            print(f"Error analyzing user patterns: {e}")
            return {}
    
    def _analyze_favorite_zones(self, activities: List[Dict], receipts: List[Dict]) -> List[str]:
        """Analyze user's favorite mall zones"""
        zone_visits = {}
        
        for activity in activities:
            if activity.get('activity_type') == 'zone_visit':
                zone = activity.get('metadata', {}).get('zone')
                if zone:
                    zone_visits[zone] = zone_visits.get(zone, 0) + 1
        
        for receipt in receipts:
            store_name = receipt.get('store_name', '')
            for zone in self.mall_zones:
                if zone.lower() in store_name.lower():
                    zone_visits[zone] = zone_visits.get(zone, 0) + 1
        
        # Return top 3 favorite zones
        sorted_zones = sorted(zone_visits.items(), key=lambda x: x[1], reverse=True)
        return [zone for zone, _ in sorted_zones[:3]]
    
    def _analyze_spending_patterns(self, receipts: List[Dict]) -> Dict[str, Any]:
        """Analyze user's spending patterns"""
        total_spent = sum(receipt.get('amount', 0) for receipt in receipts)
        avg_spend = total_spent / len(receipts) if receipts else 0
        
        category_spending = {}
        for receipt in receipts:
            store_name = receipt.get('store_name', '')
            amount = receipt.get('amount', 0)
            
            for zone in self.mall_zones:
                if zone.lower() in store_name.lower():
                    category_spending[zone] = category_spending.get(zone, 0) + amount
        
        return {
            "total_spent": total_spent,
            "average_spend": avg_spend,
            "favorite_categories": sorted(category_spending.items(), key=lambda x: x[1], reverse=True)[:3],
            "spending_frequency": len(receipts)
        }
    
    def _analyze_activity_frequency(self, activities: List[Dict]) -> Dict[str, Any]:
        """Analyze user's activity frequency"""
        activity_counts = {}
        for activity in activities:
            activity_type = activity.get('activity_type')
            activity_counts[activity_type] = activity_counts.get(activity_type, 0) + 1
        
        return {
            "total_activities": len(activities),
            "activity_distribution": activity_counts,
            "most_active_type": max(activity_counts.items(), key=lambda x: x[1])[0] if activity_counts else None
        }
    
    def _analyze_mission_preferences(self, missions: List[Dict]) -> Dict[str, Any]:
        """Analyze user's mission completion preferences"""
        mission_type_counts = {}
        total_rewards = 0
        
        for mission in missions:
            mission_type = mission.get('mission_type')
            mission_type_counts[mission_type] = mission_type_counts.get(mission_type, 0) + 1
            total_rewards += mission.get('reward_coins', 0)
        
        return {
            "completed_missions": len(missions),
            "favorite_mission_types": sorted(mission_type_counts.items(), key=lambda x: x[1], reverse=True)[:3],
            "total_rewards_earned": total_rewards
        }
    
    def _analyze_social_engagement(self, activities: List[Dict]) -> Dict[str, Any]:
        """Analyze user's social engagement"""
        social_activities = [a for a in activities if a.get('activity_type') in ['invite_sent', 'photo_shared', 'review_posted']]
        
        return {
            "social_activity_count": len(social_activities),
            "invites_sent": len([a for a in social_activities if a.get('activity_type') == 'invite_sent']),
            "photos_shared": len([a for a in social_activities if a.get('activity_type') == 'photo_shared']),
            "reviews_posted": len([a for a in social_activities if a.get('activity_type') == 'review_posted'])
        }
    
    def _analyze_exploration_level(self, activities: List[Dict]) -> Dict[str, Any]:
        """Analyze user's mall exploration level"""
        zones_visited = set()
        stores_visited = set()
        
        for activity in activities:
            if activity.get('activity_type') == 'zone_visit':
                zone = activity.get('metadata', {}).get('zone')
                if zone:
                    zones_visited.add(zone)
            
            if activity.get('activity_type') == 'store_visit':
                store = activity.get('metadata', {}).get('store')
                if store:
                    stores_visited.add(store)
        
        return {
            "zones_explored": len(zones_visited),
            "stores_visited": len(stores_visited),
            "exploration_percentage": (len(zones_visited) / len(self.mall_zones)) * 100
        }
    
    def _calculate_skill_level(self, user: Dict, activities: List[Dict], missions: List[Dict]) -> Dict[str, Any]:
        """Calculate user's skill level based on various factors"""
        level = user.get('level', 1)
        total_xp = user.get('xp', 0)
        completed_missions = len(missions)
        total_activities = len(activities)
        
        # Calculate skill score (0-100)
        skill_score = min(100, (
            (level * 10) +  # Level contribution
            (total_xp / 1000) +  # XP contribution
            (completed_missions * 2) +  # Mission completion contribution
            (total_activities / 10)  # Activity contribution
        ))
        
        if skill_score < 20:
            skill_level = "Beginner"
        elif skill_score < 40:
            skill_level = "Novice"
        elif skill_score < 60:
            skill_level = "Intermediate"
        elif skill_score < 80:
            skill_level = "Advanced"
        else:
            skill_level = "Expert"
        
        return {
            "skill_score": skill_score,
            "skill_level": skill_level,
            "level": level,
            "total_xp": total_xp,
            "completed_missions": completed_missions
        }
    
    def generate_daily_missions(self, user_id: str, count: int = 3) -> List[Dict[str, Any]]:
        """Generate personalized daily missions for a user"""
        try:
            # Analyze user patterns
            patterns = self.analyze_user_patterns(user_id)
            
            # Get user data
            user = db.get_user(user_id)
            if not user:
                return []
            
            missions = []
            used_types = set()
            
            for i in range(count):
                # Select mission type based on user preferences and skill level
                mission_type = self._select_mission_type(patterns, used_types)
                used_types.add(mission_type)
                
                # Generate mission based on type and user patterns
                mission = self._generate_mission_by_type(mission_type, patterns, user)
                
                if mission:
                    missions.append(mission)
            
            return missions
            
        except Exception as e:
            print(f"Error generating daily missions: {e}")
            return []
    
    def _select_mission_type(self, patterns: Dict[str, Any], used_types: set) -> str:
        """Select appropriate mission type based on user patterns"""
        available_types = [t for t in self.mission_types if t not in used_types]
        
        if not available_types:
            return random.choice(self.mission_types)
        
        # Weight selection based on user preferences
        weights = []
        for mission_type in available_types:
            weight = 1.0  # Base weight
            
            # Boost weight for user's favorite mission types
            favorite_types = patterns.get('mission_preferences', {}).get('favorite_mission_types', [])
            for favorite_type, _ in favorite_types:
                if mission_type == favorite_type:
                    weight *= 1.5
            
            # Boost weight for social missions if user is socially active
            if mission_type == 'social' and patterns.get('social_engagement', {}).get('social_activity_count', 0) > 5:
                weight *= 1.3
            
            # Boost weight for exploration missions if user is explorer
            if mission_type == 'exploration' and patterns.get('exploration_level', {}).get('exploration_percentage', 0) < 50:
                weight *= 1.4
            
            weights.append(weight)
        
        # Normalize weights
        total_weight = sum(weights)
        if total_weight > 0:
            weights = [w / total_weight for w in weights]
        
        return random.choices(available_types, weights=weights)[0]
    
    def _generate_mission_by_type(self, mission_type: str, patterns: Dict[str, Any], user: Dict) -> Optional[Dict[str, Any]]:
        """Generate a specific mission based on type and user patterns"""
        try:
            templates = self.mission_templates.get(mission_type, [])
            if not templates:
                return None
            
            # Select template
            template = random.choice(templates)
            
            # Generate mission parameters
            params = self._generate_mission_parameters(mission_type, patterns, user)
            
            # Create mission
            mission = {
                "mission_id": f"mission_{int(datetime.now().timestamp())}_{random.randint(1000, 9999)}",
                "user_id": user['user_id'],
                "title": template['title'].format(**params),
                "description": template['description'].format(**params),
                "mission_type": mission_type,
                "target_value": params.get('target_value', 1),
                "reward_coins": int(template['base_reward_coins'] * template['difficulty_multiplier']),
                "reward_xp": int(template['base_reward_xp'] * template['difficulty_multiplier']),
                "expires_at": (datetime.now() + timedelta(days=1)).isoformat(),
                "metadata": params
            }
            
            return mission
            
        except Exception as e:
            print(f"Error generating mission by type: {e}")
            return None
    
    def _generate_mission_parameters(self, mission_type: str, patterns: Dict[str, Any], user: Dict) -> Dict[str, Any]:
        """Generate parameters for mission based on type and user patterns"""
        skill_level = patterns.get('skill_level', {})
        skill_score = skill_level.get('skill_score', 50)
        
        params = {}
        
        if mission_type == "receipt_scan":
            # Adjust count based on skill level
            base_count = 1 if skill_score < 30 else 2 if skill_score < 60 else 3
            params['count'] = base_count + random.randint(0, 2)
            params['target_value'] = params['count']
            
            # Add store type if user has preferences
            favorite_zones = patterns.get('favorite_zones', [])
            if favorite_zones and random.random() < 0.7:
                params['store_type'] = random.choice(favorite_zones)
        
        elif mission_type == "store_visit":
            # Select zone based on user preferences
            favorite_zones = patterns.get('favorite_zones', [])
            if favorite_zones and random.random() < 0.6:
                zone = random.choice(favorite_zones)
            else:
                zone = random.choice(self.mall_zones)
            
            params['zone'] = zone
            params['count'] = 1 if skill_score < 40 else 2 if skill_score < 70 else 3
            params['target_value'] = params['count']
        
        elif mission_type == "spending":
            # Adjust amount based on user's spending patterns
            spending_patterns = patterns.get('spending_patterns', {})
            avg_spend = spending_patterns.get('average_spend', 100)
            
            # Generate realistic spending target
            base_amount = max(50, avg_spend * 0.5)
            params['amount'] = int(base_amount + random.randint(0, 100))
            params['target_value'] = params['amount']
            
            # Add category if user has preferences
            favorite_categories = spending_patterns.get('favorite_categories', [])
            if favorite_categories and random.random() < 0.7:
                params['category'] = favorite_categories[0][0]
        
        elif mission_type == "social":
            params['count'] = 1 if skill_score < 30 else 2 if skill_score < 60 else 3
            params['target_value'] = params['count']
        
        elif mission_type == "exploration":
            exploration_level = patterns.get('exploration_level', {})
            zones_explored = exploration_level.get('zones_explored', 0)
            
            # Encourage exploration of new zones
            unexplored_zones = [z for z in self.mall_zones if z not in patterns.get('favorite_zones', [])]
            if unexplored_zones:
                params['zone'] = random.choice(unexplored_zones)
            
            params['count'] = 1 if skill_score < 40 else 2 if skill_score < 70 else 3
            params['target_value'] = params['count']
        
        elif mission_type == "collection":
            params['count'] = 3 if skill_score < 40 else 5 if skill_score < 70 else 7
            params['target_value'] = params['count']
            
            # Add color theme
            colors = ['red', 'blue', 'green', 'gold', 'purple', 'orange']
            params['color'] = random.choice(colors)
        
        elif mission_type == "challenge":
            if random.random() < 0.5:
                # Speed challenge
                params['time_limit'] = 30 if skill_score < 40 else 20 if skill_score < 70 else 15
                params['target_value'] = 1
            else:
                # Precision challenge
                spending_patterns = patterns.get('spending_patterns', {})
                avg_spend = spending_patterns.get('average_spend', 100)
                params['target_amount'] = int(avg_spend + random.randint(-20, 50))
                params['target_value'] = params['target_amount']
        
        elif mission_type == "daily":
            params['count'] = 2 if skill_score < 40 else 3 if skill_score < 70 else 4
            params['target_value'] = 1
        
        return params
    
    def generate_weekly_missions(self, user_id: str, count: int = 5) -> List[Dict[str, Any]]:
        """Generate weekly missions with higher rewards and complexity"""
        try:
            patterns = self.analyze_user_patterns(user_id)
            user = db.get_user(user_id)
            
            if not user:
                return []
            
            missions = []
            
            for i in range(count):
                # Weekly missions are more complex
                mission_type = random.choice(['challenge', 'collection', 'spending', 'exploration'])
                mission = self._generate_mission_by_type(mission_type, patterns, user)
                
                if mission:
                    # Increase rewards for weekly missions
                    mission['reward_coins'] = int(mission['reward_coins'] * 1.5)
                    mission['reward_xp'] = int(mission['reward_xp'] * 1.5)
                    mission['expires_at'] = (datetime.now() + timedelta(days=7)).isoformat()
                    missions.append(mission)
            
            return missions
            
        except Exception as e:
            print(f"Error generating weekly missions: {e}")
            return []
    
    def generate_event_missions(self, user_id: str, event_type: str) -> List[Dict[str, Any]]:
        """Generate special event missions"""
        try:
            patterns = self.analyze_user_patterns(user_id)
            user = db.get_user(user_id)
            
            if not user:
                return []
            
            event_missions = []
            
            if event_type == "national_day":
                # UAE National Day special missions
                event_missions.extend([
                    {
                        "mission_id": f"event_mission_{int(datetime.now().timestamp())}_{random.randint(1000, 9999)}",
                        "user_id": user['user_id'],
                        "title": "🇦🇪 National Day Celebration",
                        "description": "Visit 5 stores with UAE flag decorations",
                        "mission_type": "event",
                        "target_value": 5,
                        "reward_coins": 100,
                        "reward_xp": 200,
                        "expires_at": (datetime.now() + timedelta(days=3)).isoformat(),
                        "metadata": {"event_type": "national_day"}
                    },
                    {
                        "mission_id": f"event_mission_{int(datetime.now().timestamp())}_{random.randint(1000, 9999)}",
                        "user_id": user['user_id'],
                        "title": "🎊 Festival Shopping",
                        "description": "Spend AED 200 during National Day celebrations",
                        "mission_type": "event",
                        "target_value": 200,
                        "reward_coins": 150,
                        "reward_xp": 300,
                        "expires_at": (datetime.now() + timedelta(days=3)).isoformat(),
                        "metadata": {"event_type": "national_day"}
                    }
                ])
            
            elif event_type == "eid":
                # Eid special missions
                event_missions.extend([
                    {
                        "mission_id": f"event_mission_{int(datetime.now().timestamp())}_{random.randint(1000, 9999)}",
                        "user_id": user['user_id'],
                        "title": "🌙 Eid Shopping Spree",
                        "description": "Visit 3 clothing stores for Eid shopping",
                        "mission_type": "event",
                        "target_value": 3,
                        "reward_coins": 80,
                        "reward_xp": 160,
                        "expires_at": (datetime.now() + timedelta(days=5)).isoformat(),
                        "metadata": {"event_type": "eid"}
                    }
                ])
            
            return event_missions
            
        except Exception as e:
            print(f"Error generating event missions: {e}")
            return []

# Global AI mission generator instance
ai_mission_generator = AIMissionGenerator() 