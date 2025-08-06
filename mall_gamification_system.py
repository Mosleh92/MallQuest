# Mall Gamification AI Control Panel – ULTRA Version (Advanced + Graphics-Oriented)

# -----------------------------
# SYSTEM OVERVIEW
# -----------------------------
# This upgraded AI control panel supports:
# - Visual simulation layer for animated coin drops & interactive quests
# - Location-aware gamification (AR zones, café quests, map-based zones)
# - Seasonal events, pet companions, shop upgrades
# - Branded coin systems & in-game ads for monetization
# - Full AI mission generation, streak logic, event scheduling
# - Four separate dashboards:
#   1. Player Panel
#   2. Super Admin Panel
#   3. Shopkeeper Panel
#   4. Customer Service Panel
# - Arabic & English multilingual logic supported for messages and achievements
# - ✅ Multilingual UI Panel (Arabic / English support in all front-end outputs)
# - ✅ Indoor Wi-Fi Restriction: Full system only accessible inside mall Wi-Fi (Deerfields only)

# -----------------------------
# 1. IMPORTS AND SETUP
# -----------------------------
import random
import re
import time
from datetime import datetime, timedelta
from collections import defaultdict
import json
import hashlib
import uuid
import logging
import logger as logger_config
logger = logging.getLogger(__name__)
from flash_events import FlashEventManager, FlashEventAdminInterface
from wheel_of_fortune import WheelOfFortune

# Import 3D Graphics Module
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("graphics_3d", "3d_graphics_module.py")
    graphics_3d_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(graphics_3d_module)
    
    initialize_3d_system = graphics_3d_module.initialize_3d_system
    trigger_3d_effect = graphics_3d_module.trigger_visual_effect
    graphics_controller = graphics_3d_module.graphics_controller
    
    GRAPHICS_3D_AVAILABLE = True
except ImportError:
    GRAPHICS_3D_AVAILABLE = False
    logger.warning("[SYSTEM] 3D Graphics module not available, using basic effects")

# Import Database System
try:
    from database import db
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    logger.warning("[SYSTEM] Database module not available, using in-memory storage")

# Import AI Mission Generator
try:
    from ai_mission_generator import ai_mission_generator
    AI_MISSIONS_AVAILABLE = True
except ImportError:
    AI_MISSIONS_AVAILABLE = False
    logger.warning("[SYSTEM] AI Mission Generator not available")

# Import WiFi Verification
try:
    from wifi_verification import wifi_verification
    WIFI_VERIFICATION_AVAILABLE = True
except ImportError:
    WIFI_VERIFICATION_AVAILABLE = False
    logger.warning("[SYSTEM] WiFi Verification not available")

# Import Companion System
try:
    from companion_system import companion_system
    COMPANION_SYSTEM_AVAILABLE = True
except ImportError:
    COMPANION_SYSTEM_AVAILABLE = False
    logger.warning("[SYSTEM] Companion System not available")

# Import WebAR Treasure Hunt
try:
    from webar_treasure_hunt import WebARTreasureHunt
    WEBAR_TREASURE_AVAILABLE = True
except ImportError:
    WEBAR_TREASURE_AVAILABLE = False
    logger.warning("[SYSTEM] WebAR Treasure Hunt module not available")

# Import Smart Cache Manager for memory management
try:
    from performance_module import get_smart_cache_manager
    smart_cache_manager = get_smart_cache_manager()
    SMART_CACHE_AVAILABLE = True
    logger.info("[✅] Smart Cache Manager loaded")
except ImportError:
    SMART_CACHE_AVAILABLE = False
    logger.warning("[⚠️] Smart Cache Manager not available - using basic storage")

# Import Security and Performance modules
try:
    from security_module import (
        SecurityManager, SecureDatabase, InputValidator, 
        log_security_event, get_security_manager, get_secure_database
    )
    from performance_module import (
        PerformanceManager, PerformanceMonitor, record_performance_event,
        get_performance_manager, get_performance_monitor
    )
    SECURITY_PERFORMANCE_AVAILABLE = True
    logger.info("[✅] Security and Performance modules loaded")
except ImportError:
    SECURITY_PERFORMANCE_AVAILABLE = False
    logger.warning("[⚠️] Security and Performance modules not available")

# Visual/Graphics System
def trigger_visual_effect(effect_type: str, payload=None):
    """Enhanced visual effects with 3D graphics support"""
    if GRAPHICS_3D_AVAILABLE:
        # Use 3D graphics effects
        if payload:
            return trigger_3d_effect(effect_type, payload=payload)
        else:
            return trigger_3d_effect(effect_type)
    else:
        # Fallback to basic effects
        logger.info(f"[GRAPHIC EFFECT]: {effect_type} >> {payload}")
        return {"type": effect_type, "payload": payload, "mode": "basic"}

# Smart data storage with memory management
if SMART_CACHE_AVAILABLE:
    # Use SmartCacheManager for controlled memory usage
    user_data = smart_cache_manager
    store_data = smart_cache_manager
    logger.info("[✅] Using Smart Cache Manager for memory management")
else:
    # Fallback to basic storage (limited size)
    user_data = defaultdict(dict)
    store_data = defaultdict(dict)
    logger.warning("[⚠️] Using basic storage - memory growth not controlled")

purchase_logs = []
suspicious_receipts = []  # NEW: store receipts flagged as suspicious

# -----------------------------
# 2. MULTILINGUAL SYSTEM
# -----------------------------
class MultilingualSystem:
    def __init__(self):
        self.translations = {
            "welcome_message": {
                "en": "Welcome to Deerfields Mall Rewards!",
                "ar": "مرحبًا بكم في نظام مكافآت ديرفيلدز مول!"
            },
            "level_up": {
                "en": "🎉 Level Up! You're now level {level}",
                "ar": "🎉 ترقية مستوى! أنت الآن في المستوى {level}"
            },
            "receipt_accepted": {
                "en": "🧾 Receipt accepted! You've earned {points} points.",
                "ar": "🧾 تم قبول الفاتورة! لقد حصلت على {points} نقطة."
            },
            "daily_login": {
                "en": "🎁 Daily Login Reward: {coins} Coins",
                "ar": "🎁 تسجيل دخول يومي: {coins} عملة"
            },
            "invalid_receipt": {
                "en": "❌ Invalid mall receipt. Only Deerfields Mall receipts are accepted.",
                "ar": "❌ فقط فواتير ديرفيلدز مول مقبولة."
            },
            "suspicious_receipt": {
                "en": "⚠️ Receipt flagged as suspicious. Pending review.",
                "ar": "⚠️ تم الإبلاغ عن الفاتورة كمشبوهة. تحت المراجعة."
            },
            "receipt_submitted": {
                "en": "🧾 Receipt from {store}: +{coins} Coins",
                "ar": "🧾 فاتورة من {store}: +{coins} عملة"
            },
            "admin_removed_receipt": {
                "en": "❌ Admin removed receipt: -{coins} Coins ({reason})",
                "ar": "❌ تمت إزالة الفاتورة من قِبل المشرف: -{coins} عملة ({reason})"
            },
            "mission_completed": {
                "en": "✅ Mission completed: {mission_name}",
                "ar": "✅ تم إكمال المهمة: {mission_name}"
            },
            "streak_bonus": {
                "en": "🔥 {day_count} Day Streak! +{bonus} bonus coins",
                "ar": "🔥 {day_count} يوم متتالي! +{bonus} عملة إضافية"
            }
        }

    def get_text(self, key: str, language: str = "en", **kwargs):
        template = self.translations.get(key, {}).get(language, key)
        return template.format(**kwargs)

# -----------------------------
# 3. INTELLIGENT REWARD SYSTEM
# -----------------------------
class IntelligentRewardSystem:
    def __init__(self):
        self.base_multiplier = 0.1
        self.category_multipliers = {
            'fashion': 1.3,      # 30% more for fashion
            'electronics': 1.2,  # 20% more for electronics
            'food': 0.8,         # 20% less for food
            'luxury': 1.5,       # 50% more for luxury
            'books': 1.4,        # 40% more for books
            'sports': 1.1,       # 10% more for sports
            'beauty': 1.25,      # 25% more for beauty
            'home': 1.15         # 15% more for home
        }
        
        self.vip_multipliers = {
            'Bronze': 1.0,
            'Silver': 1.2,
            'Gold': 1.5,
            'Platinum': 2.0,
            'Diamond': 2.5
        }
        
        self.time_multipliers = {
            'morning': 1.1,      # 6-12
            'afternoon': 1.0,    # 12-18
            'evening': 1.3,      # 18-22
            'night': 0.8         # 22-6
        }
        
        self.streak_multipliers = {
            1: 1.0,    # No streak
            3: 1.1,    # 3-day streak
            7: 1.2,    # 7-day streak
            14: 1.3,   # 14-day streak
            30: 1.5,   # 30-day streak
            60: 2.0    # 60-day streak
        }
    
    def calculate_dynamic_reward(self, amount: float, category: str, 
                               user_profile: dict, context: dict = None) -> dict:
        """Calculate intelligent reward based on multiple factors"""
        
        # Base reward
        base_coins = amount * self.base_multiplier
        
        # Category multiplier
        category_mult = self.category_multipliers.get(category.lower(), 1.0)
        
        # VIP tier multiplier
        vip_tier = user_profile.get('vip_tier', 'Bronze')
        vip_mult = self.vip_multipliers.get(vip_tier, 1.0)
        
        # Time-based multiplier
        hour = datetime.now().hour
        if 6 <= hour < 12:
            time_period = 'morning'
        elif 12 <= hour < 18:
            time_period = 'afternoon'
        elif 18 <= hour < 22:
            time_period = 'evening'
        else:
            time_period = 'night'
        time_mult = self.time_multipliers.get(time_period, 1.0)
        
        # Event multiplier
        event_mult = context.get('event_multiplier', 1.0) if context else 1.0
        
        # Streak multiplier
        streak = user_profile.get('login_streak', 0)
        streak_mult = 1.0
        for streak_threshold, multiplier in sorted(self.streak_multipliers.items(), reverse=True):
            if streak >= streak_threshold:
                streak_mult = multiplier
                break
        
        # Calculate total multiplier
        total_mult = category_mult * vip_mult * time_mult * event_mult * streak_mult
        final_coins = int(base_coins * total_mult)
        
        # Bonus rewards
        bonus_rewards = self.calculate_bonus_rewards(amount, user_profile, context)
        
        # Celebration level
        celebration_level = self.get_celebration_level(final_coins)
        
        return {
            'base_coins': int(base_coins),
            'multiplier_breakdown': {
                'category': category_mult,
                'vip': vip_mult,
                'time': time_mult,
                'event': event_mult,
                'streak': streak_mult,
                'total': total_mult
            },
            'total_coins': final_coins,
            'bonus_rewards': bonus_rewards,
            'celebration_level': celebration_level,
            'xp_earned': int(final_coins * 0.5)  # XP is half of coins
        }
    
    def calculate_bonus_rewards(self, amount: float, user_profile: dict, context: dict = None) -> dict:
        """Calculate bonus rewards based on various factors"""
        bonuses = {}
        
        # High amount bonus
        if amount >= 1000:
            bonuses['high_amount'] = {'type': 'coins', 'value': 100, 'reason': 'High purchase amount'}
        elif amount >= 500:
            bonuses['medium_amount'] = {'type': 'coins', 'value': 50, 'reason': 'Medium purchase amount'}
        
        # Milestone bonus
        total_purchases = user_profile.get('total_purchases', 0)
        if total_purchases % 10 == 0 and total_purchases > 0:
            bonuses['milestone'] = {'type': 'special_item', 'value': 'golden_badge', 'reason': f'{total_purchases}th purchase'}
        
        # First time category bonus
        category = context.get('category', '') if context else ''
        if category and category not in user_profile.get('visited_categories', []):
            bonuses['new_category'] = {'type': 'coins', 'value': 25, 'reason': f'First time at {category}'}
        
        # Weekend bonus
        if datetime.now().weekday() >= 5:  # Saturday or Sunday
            bonuses['weekend'] = {'type': 'coins', 'value': 20, 'reason': 'Weekend bonus'}
        
        return bonuses
    
    def get_celebration_level(self, coins: int) -> str:
        """Determine celebration level based on reward"""
        if coins >= 200:
            return 'epic'
        elif coins >= 100:
            return 'super'
        elif coins >= 50:
            return 'great'
        else:
            return 'normal'

# -----------------------------
# 4. PERSONALIZED MISSION GENERATOR
# -----------------------------
class PersonalizedMissionGenerator:
    def __init__(self):
        self.mission_templates = {
            'daily': {
                'visit_stores': {
                    'template': 'Visit {count} different stores today',
                    'target_range': (2, 5),
                    'reward_range': (10, 30)
                },
                'spend_amount': {
                    'template': 'Spend {amount} AED at {category} stores',
                    'target_range': (50, 200),
                    'reward_range': (15, 40)
                },
                'submit_receipts': {
                    'template': 'Submit {count} receipts today',
                    'target_range': (1, 3),
                    'reward_range': (10, 25)
                },
                'login_streak': {
                    'template': 'Maintain a {count}-day login streak',
                    'target_range': (3, 7),
                    'reward_range': (20, 50)
                }
            },
            'weekly': {
                'total_spending': {
                    'template': 'Spend {amount} AED this week',
                    'target_range': (200, 1000),
                    'reward_range': (50, 150)
                },
                'store_exploration': {
                    'template': 'Visit {count} different store categories',
                    'target_range': (3, 8),
                    'reward_range': (30, 80)
                },
                'streak_achievement': {
                    'template': 'Achieve a {count}-day login streak',
                    'target_range': (5, 14),
                    'reward_range': (40, 100)
                }
            },
            'seasonal': {
                'event_participation': {
                    'template': 'Participate in {event_name} event',
                    'target_range': (1, 1),
                    'reward_range': (100, 300)
                },
                'seasonal_spending': {
                    'template': 'Spend {amount} AED during {season}',
                    'target_range': (500, 2000),
                    'reward_range': (100, 250)
                }
            }
        }
    
    def generate_personalized_mission(self, user_profile: dict, mission_type: str = 'daily') -> dict:
        """Generate AI-powered personalized mission based on user behavior"""
        
        # Analyze user behavior patterns
        user_patterns = self.analyze_user_behavior(user_profile)
        
        # Select appropriate mission template
        available_templates = self.mission_templates.get(mission_type, self.mission_templates['daily'])
        mission_key = self.select_mission_type(user_patterns, available_templates)
        template_data = available_templates[mission_key]
        
        # Generate mission parameters based on user level and history
        mission_params = self.generate_mission_parameters(user_profile, template_data)
        
        # Create mission
        mission = {
            'id': str(uuid.uuid4()),
            'type': mission_type,
            'title': template_data['template'].format(**mission_params),
            'progress': 0,
            'target': mission_params['target'],
            'reward': mission_params['reward'],
            'xp_reward': int(mission_params['reward'] * 0.5),
            'expires': datetime.now() + timedelta(days=7 if mission_type == 'weekly' else 1),
            'completed': False,
            'difficulty': mission_params['difficulty'],
            'category': mission_params.get('category', 'general'),
            'personalized': True
        }
        
        return mission
    
    def analyze_user_behavior(self, user_profile: dict) -> dict:
        """Analyze user behavior patterns for personalization"""
        patterns = {
            'spending_level': 'low',
            'preferred_categories': [],
            'activity_frequency': 'low',
            'streak_behavior': 'inconsistent'
        }
        
        # Analyze spending level
        total_spent = user_profile.get('total_spent', 0)
        if total_spent > 1000:
            patterns['spending_level'] = 'high'
        elif total_spent > 500:
            patterns['spending_level'] = 'medium'
        
        # Analyze preferred categories
        purchase_history = user_profile.get('purchase_history', [])
        category_counts = {}
        for purchase in purchase_history:
            category = purchase.get('category', 'general')
            category_counts[category] = category_counts.get(category, 0) + 1
        
        if category_counts:
            patterns['preferred_categories'] = sorted(category_counts.keys(), 
                                                    key=lambda x: category_counts[x], reverse=True)[:3]
        
        # Analyze activity frequency
        login_streak = user_profile.get('login_streak', 0)
        if login_streak > 7:
            patterns['activity_frequency'] = 'high'
        elif login_streak > 3:
            patterns['activity_frequency'] = 'medium'
        
        # Analyze streak behavior
        if login_streak > 14:
            patterns['streak_behavior'] = 'consistent'
        elif login_streak > 7:
            patterns['streak_behavior'] = 'moderate'
        
        return patterns
    
    def select_mission_type(self, user_patterns: dict, available_templates: dict) -> str:
        """Select mission type based on user patterns"""
        import random
        
        # Weighted selection based on user behavior
        weights = {}
        
        for mission_key in available_templates.keys():
            weight = 1.0  # Base weight
            
            # Adjust weight based on user patterns
            if 'spend' in mission_key and user_patterns['spending_level'] == 'high':
                weight *= 1.5
            elif 'visit' in mission_key and user_patterns['activity_frequency'] == 'high':
                weight *= 1.3
            elif 'streak' in mission_key and user_patterns['streak_behavior'] == 'consistent':
                weight *= 1.2
            
            weights[mission_key] = weight
        
        # Select mission type based on weights
        total_weight = sum(weights.values())
        rand_val = random.uniform(0, total_weight)
        
        current_weight = 0
        for mission_key, weight in weights.items():
            current_weight += weight
            if rand_val <= current_weight:
                return mission_key
        
        return list(available_templates.keys())[0]  # Fallback
    
    def generate_mission_parameters(self, user_profile: dict, template_data: dict) -> dict:
        """Generate mission parameters based on user level and history"""
        import random
        
        user_level = user_profile.get('level', 1)
        spending_level = user_profile.get('total_spent', 0)
        
        # Base parameters
        target_min, target_max = template_data['target_range']
        reward_min, reward_max = template_data['reward_range']
        
        # Adjust based on user level
        level_multiplier = 1 + (user_level - 1) * 0.1  # 10% increase per level
        
        # Adjust based on spending level
        spending_multiplier = 1.0
        if spending_level > 1000:
            spending_multiplier = 1.3
        elif spending_level > 500:
            spending_multiplier = 1.1
        
        # Calculate final parameters
        target = int(random.randint(target_min, target_max) * level_multiplier * spending_multiplier)
        reward = int(random.randint(reward_min, reward_max) * level_multiplier * spending_multiplier)
        
        # Determine difficulty
        difficulty = 'easy'
        if target > target_max * 1.5:
            difficulty = 'hard'
        elif target > target_max * 1.2:
            difficulty = 'medium'
        
        params = {
            'target': target,
            'reward': reward,
            'difficulty': difficulty
        }
        
        # Add category-specific parameters
        if 'category' in template_data['template']:
            preferred_categories = user_profile.get('preferred_categories', ['fashion', 'electronics'])
            params['category'] = random.choice(preferred_categories)
        
        if 'amount' in template_data['template']:
            params['amount'] = target
        
        if 'count' in template_data['template']:
            params['count'] = target
        
        if 'event_name' in template_data['template']:
            params['event_name'] = 'Summer Sale'  # Default event name
        
        if 'season' in template_data['template']:
            current_month = datetime.now().month
            if 3 <= current_month <= 5:
                season = 'Spring'
            elif 6 <= current_month <= 8:
                season = 'Summer'
            elif 9 <= current_month <= 11:
                season = 'Autumn'
            else:
                season = 'Winter'
            params['season'] = season
        
        return params

# -----------------------------
# 5. USER PROFILE STRUCTURE
# -----------------------------
class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.coins = 0
        self.xp = 0
        self.level = 1
        self.vip_tier = "Bronze"
        self.vip_points = 0
        self.last_login = datetime.now()
        self.receipts = []
        self.visits = []
        self.missions = []
        self.rewards = []
        self.inventory = []
        self.achievements = []
        self.family_members = []
        self.purchase_history = []
        self.redeemable_points = 0
        self.language = "en"  # 'en' or 'ar'
        self.multilingual = MultilingualSystem()
        
        # Advanced progression system
        self.total_spent = 0
        self.visited_categories = []
        self.total_purchases = 0
        self.achievement_points = 0
        self.social_score = 0
        
        # VIP tier benefits
        self.vip_benefits = {
            'Bronze': {
                'coin_multiplier': 1.0,
                'xp_multiplier': 1.0,
                'daily_bonus': 5,
                'special_offers': False,
                'priority_support': False
            },
            'Silver': {
                'coin_multiplier': 1.2,
                'xp_multiplier': 1.1,
                'daily_bonus': 10,
                'special_offers': True,
                'priority_support': False
            },
            'Gold': {
                'coin_multiplier': 1.5,
                'xp_multiplier': 1.2,
                'daily_bonus': 20,
                'special_offers': True,
                'priority_support': True
            },
            'Platinum': {
                'coin_multiplier': 2.0,
                'xp_multiplier': 1.5,
                'daily_bonus': 50,
                'special_offers': True,
                'priority_support': True,
                'exclusive_events': True
            },
            'Diamond': {
                'coin_multiplier': 2.5,
                'xp_multiplier': 2.0,
                'daily_bonus': 100,
                'special_offers': True,
                'priority_support': True,
                'exclusive_events': True,
                'personal_concierge': True
            }
        }
        
        # Companion system
        self.companion = {
            "name": "Koinko",
            "level": 1,
            "power": 1,
            "xp": 0,
            "happiness": 100,
            "hunger": 0,
            "abilities": ["coin_bonus"],
            "bonus_effect": "+10% chance on wheel rewards"
        }
        
        # Streak and progression
        self.combo_streak = 0
        self.multitap_level = 1
        self.energy_limit = 10
        self.fake_urgency_flags = []
        self.locked_rewards = {}
        self.login_streak = 0
        self.last_streak_date = None
        
        # Social features
        self.friends = []
        self.team_id = None
        self.leaderboard_position = 0
        self.social_achievements = []
        
        # Event participation
        self.event_participation = {}
        self.seasonal_progress = {}

    def t(self, message_en, message_ar):
        return message_ar if self.language == "ar" else message_en

    def update_level(self):
        """Advanced level progression based on XP"""
        # Calculate level based on XP (not just coins)
        xp_required = self.level * 100  # 100 XP per level
        if self.xp >= xp_required:
            self.level = min(100, self.xp // 100 + 1)
            
            # Level up rewards
            if self.level > 1:
                level_bonus = self.level * 10
                self.coins += level_bonus
                self.rewards.append(self.multilingual.get_text("level_up", self.language, level=self.level))
                trigger_visual_effect("level_up", {"level": self.level, "bonus": level_bonus})
    
    def update_vip_tier(self):
        """Update VIP tier based on spending and activity"""
        # Calculate VIP points based on multiple factors
        spending_points = self.total_spent // 100  # 1 point per 100 AED spent
        activity_points = self.login_streak * 10  # 10 points per login streak day
        achievement_points = self.achievement_points
        social_points = self.social_score
        
        self.vip_points = spending_points + activity_points + achievement_points + social_points
        
        # Determine VIP tier
        if self.vip_points >= 10000:
            new_tier = "Diamond"
        elif self.vip_points >= 5000:
            new_tier = "Platinum"
        elif self.vip_points >= 2000:
            new_tier = "Gold"
        elif self.vip_points >= 500:
            new_tier = "Silver"
        else:
            new_tier = "Bronze"
        
        # VIP tier upgrade rewards
        if new_tier != self.vip_tier:
            old_tier = self.vip_tier
            self.vip_tier = new_tier
            
            # Tier upgrade bonus
            tier_bonuses = {
                'Silver': 50,
                'Gold': 100,
                'Platinum': 200,
                'Diamond': 500
            }
            
            if new_tier in tier_bonuses:
                bonus = tier_bonuses[new_tier]
                self.coins += bonus
                self.rewards.append(f"🎉 VIP Tier Upgrade to {new_tier}! +{bonus} coins")
                trigger_visual_effect("vip_upgrade", {"tier": new_tier, "bonus": bonus})
    
    def get_vip_benefits(self):
        """Get current VIP tier benefits"""
        return self.vip_benefits.get(self.vip_tier, self.vip_benefits['Bronze'])
    
    def add_xp(self, amount: int, source: str = "general"):
        """Add XP with VIP multiplier"""
        vip_benefits = self.get_vip_benefits()
        xp_multiplier = vip_benefits['xp_multiplier']
        final_xp = int(amount * xp_multiplier)
        
        self.xp += final_xp
        
        # Check for level up
        old_level = self.level
        self.update_level()
        
        return {
            'xp_gained': final_xp,
            'multiplier': xp_multiplier,
            'leveled_up': self.level > old_level,
            'source': source
        }

    def login(self):
        now = datetime.now()
        if (now - self.last_login).days >= 1:
            # Streak logic
            if self.last_streak_date and (now.date() - self.last_streak_date).days == 1:
                self.login_streak += 1
            elif (now.date() - self.last_login.date()).days > 1:
                self.login_streak = 1
            else:
                self.login_streak = 1
            
            self.last_streak_date = now.date()
            
            # VIP-enhanced daily reward
            vip_benefits = self.get_vip_benefits()
            base_reward = vip_benefits['daily_bonus']
            streak_bonus = min(self.login_streak * 2, 20)  # Max 20 bonus coins
            total_reward = base_reward + streak_bonus
            
            # Apply VIP coin multiplier
            coin_multiplier = vip_benefits['coin_multiplier']
            final_reward = int(total_reward * coin_multiplier)
            
            self.coins += final_reward
            
            # Add XP for login
            login_xp = 10 + (self.login_streak * 2)  # Base 10 XP + 2 per streak day
            xp_result = self.add_xp(login_xp, "daily_login")
            
            self.rewards.append(self.multilingual.get_text("daily_login", self.language, coins=final_reward))
            
            if self.login_streak > 1:
                self.rewards.append(self.multilingual.get_text("streak_bonus", self.language, 
                                                              day_count=self.login_streak, bonus=streak_bonus))
            
            # Update VIP tier
            self.update_vip_tier()
            
            trigger_visual_effect("daily_login_bonus", {
                "coins": final_reward, 
                "streak": self.login_streak,
                "vip_tier": self.vip_tier,
                "xp_gained": xp_result['xp_gained']
            })
        self.last_login = now
    
    def add_friend(self, friend_id: str):
        """Add a friend for social features"""
        if friend_id not in self.friends and friend_id != self.user_id:
            self.friends.append(friend_id)
            self.social_score += 10
            self.rewards.append(f"👥 Added friend: {friend_id}")
            return True
        return False
    
    def join_team(self, team_id: str):
        """Join a team for team challenges"""
        self.team_id = team_id
        self.social_score += 20
        self.rewards.append(f"👥 Joined team: {team_id}")
        return True
    
    def earn_achievement(self, achievement_id: str, achievement_name: str, points: int = 10):
        """Earn an achievement"""
        if achievement_id not in [a['id'] for a in self.achievements]:
            achievement = {
                'id': achievement_id,
                'name': achievement_name,
                'points': points,
                'earned_at': datetime.now()
            }
            self.achievements.append(achievement)
            self.achievement_points += points
            self.social_score += points
            self.rewards.append(f"🏆 Achievement unlocked: {achievement_name}")
            trigger_visual_effect("achievement_unlocked", {"achievement": achievement_name, "points": points})
            return True
        return False

    def add_purchase(self, amount, store_category):
        """Add purchase with advanced tracking"""
        purchase = {
            "amount": amount,
            "category": store_category,
            "timestamp": datetime.now()
        }
        self.purchase_history.append(purchase)
        
        # Update totals
        self.total_spent += amount
        self.total_purchases += 1
        
        # Track visited categories
        if store_category not in self.visited_categories:
            self.visited_categories.append(store_category)
        
        # Calculate points with VIP benefits
        points_result = self.calculate_points(amount, store_category)
        
        # Update VIP tier
        self.update_vip_tier()
        
        # Check for achievements
        self.check_purchase_achievements(amount, store_category)
        
        return points_result

    def calculate_points(self, amount, category):
        """Calculate points with VIP multipliers"""
        vip_benefits = self.get_vip_benefits()
        coin_multiplier = vip_benefits['coin_multiplier']
        
        # Base points calculation
        base_points = int(amount * 0.1)  # 10% of amount as base points
        
        # Category bonus
        category_bonus = 0
        if category not in [p["category"] for p in self.purchase_history]:
            category_bonus = 25  # First time category bonus
        
        # Apply VIP multiplier
        final_points = int((base_points + category_bonus) * coin_multiplier)
        
        # Add to redeemable points
        self.redeemable_points += final_points
        
        # Add XP
        xp_gained = int(amount * 0.05)  # 5% of amount as XP
        xp_result = self.add_xp(xp_gained, "purchase")
        
        return {
            'base_points': base_points,
            'category_bonus': category_bonus,
            'vip_multiplier': coin_multiplier,
            'final_points': final_points,
            'xp_gained': xp_result['xp_gained']
        }
    
    def check_purchase_achievements(self, amount, category):
        """Check for purchase-related achievements"""
        # High spender achievement
        if amount >= 1000:
            self.earn_achievement("high_spender", "High Roller", 50)
        
        # Category explorer achievement
        if len(self.visited_categories) >= 5:
            self.earn_achievement("category_explorer", "Category Explorer", 30)
        
        # Frequent shopper achievement
        if self.total_purchases >= 10:
            self.earn_achievement("frequent_shopper", "Frequent Shopper", 40)
        
        # VIP spender achievement
        if self.total_spent >= 5000:
            self.earn_achievement("vip_spender", "VIP Spender", 100)

# -----------------------------
# 4. BONUS: Receipt Upload & Reward
# -----------------------------
def submit_receipt(user: User, amount: float, store: str):
    if not store.lower().startswith("deerfields"):
        user.rewards.append(user.multilingual.get_text("invalid_receipt", user.language))
        return

    verification = ai_verify_receipt(user, amount, store)
    if not verification["valid"]:
        suspicious_receipts.append({
            "user_id": user.user_id,
            "store": store,
            "amount": amount,
            "confidence": verification.get("confidence", 0),
            "reason": verification.get("reason", "unknown"),
            "timestamp": datetime.now()
        })
        user.rewards.append(user.multilingual.get_text("suspicious_receipt", user.language))
        return

    coins_earned = int(amount // 10)
    user.coins += coins_earned
    user.receipts.append({"store": store, "amount": amount, "coins": coins_earned})
    user.rewards.append(user.multilingual.get_text("receipt_submitted", user.language, 
                                                   store=store, coins=coins_earned))
    trigger_visual_effect("receipt_submitted", {"coins": coins_earned, "store": store})
    user.update_level()

# -----------------------------
# 5. AI Receipt Verification
# -----------------------------
def ai_verify_receipt(user: User, amount: float, store: str) -> dict:
    if not store.lower().startswith("deerfields"):
        return {"valid": False, "reason": "invalid_store", "confidence": 1.0}

    suspicious_patterns = [
        {"pattern": r"\b\d{5,}\b", "reason": "amount_too_high"},
        {"pattern": r"midnight|3am", "reason": "unusual_time"}
    ]
    receipt_str = f"{store} {amount}"

    for pattern in suspicious_patterns:
        if re.search(pattern["pattern"], receipt_str, re.IGNORECASE):
            return {"valid": False, "reason": pattern["reason"], "confidence": 0.7}

    return {"valid": True, "reason": "", "confidence": 0.95}

# -----------------------------
# 6. Manual Receipt Removal (Admin)
# -----------------------------
def admin_remove_receipt(user: User, index: int, reason: str = "Invalid/Fraudulent"):
    if 0 <= index < len(user.receipts):
        removed = user.receipts.pop(index)
        user.coins -= removed["coins"]
        user.rewards.append(user.multilingual.get_text("admin_removed_receipt", user.language,
                                                       coins=removed["coins"], reason=reason))
        trigger_visual_effect("receipt_removed", {"coins_removed": removed["coins"], "reason": reason})

# -----------------------------
# 7. Abu Dhabi Special Features
# -----------------------------
class AbuDhabiSpecialFeatures:
    def __init__(self):
        self.localized_features = {
            "ramadan_mode": True,
            "national_day_events": True,
            "vip_treatment": {
                "golden_visa": True,
                "premium_residents": True
            },
            "luxury_brand_integration": [
                "Emirates Palace",
                "LuLu Group",
                "Al Futtaim"
            ]
        }

# -----------------------------
# 8. Indoor Mall-Only Access Enforcement
# -----------------------------
def is_inside_mall(user_ip_or_network: str) -> bool:
    mall_wifi_ssid = "Deerfields_Free_WiFi"
    return user_ip_or_network == mall_wifi_ssid

def get_available_features(user: User, user_ip: str):
    if is_inside_mall(user_ip):
        return ["earn_coins", "submit_receipt", "play_games", "join_challenges"]
    else:
        return ["browse_offers", "view_stores", "view_own_profile"]

# -----------------------------
# 9. AI Mission Generation System
# -----------------------------
class AIMissionGenerator:
    def __init__(self):
        self.mission_templates = {
            "daily": [
                "Visit {store_count} different stores today",
                "Spend {amount} AED at {category} stores",
                "Submit {receipt_count} receipts today"
            ],
            "weekly": [
                "Achieve a {day_count}-day login streak",
                "Earn {coin_target} coins this week",
                "Visit the mall {visit_count} times this week"
            ],
            "seasonal": [
                "Participate in {event_name} event",
                "Complete {challenge_count} challenges during {season}",
                "Earn {bonus_coins} bonus coins during {holiday}"
            ]
        }
    
    def generate_mission(self, user: User, mission_type: str = "daily") -> dict:
        template = random.choice(self.mission_templates.get(mission_type, self.mission_templates["daily"]))
        
        mission_data = {
            "id": str(uuid.uuid4()),
            "type": mission_type,
            "title": template,
            "progress": 0,
            "target": random.randint(3, 10),
            "reward": random.randint(10, 50),
            "expires": datetime.now() + timedelta(days=7 if mission_type == "weekly" else 1),
            "completed": False
        }
        
        return mission_data

# -----------------------------
# 10. Event Scheduling System
# -----------------------------
class EventScheduler:
    def __init__(self):
        self.events = []
        self.seasonal_events = {
            "ramadan": {
                "start": "2024-03-10",
                "end": "2024-04-09",
                "bonus_multiplier": 2.0,
                "special_rewards": ["Iftar Vouchers", "Ramadan Coins"]
            },
            "national_day": {
                "start": "2024-12-02",
                "end": "2024-12-03",
                "bonus_multiplier": 1.5,
                "special_rewards": ["UAE Flag Items", "National Pride Coins"]
            }
        }
    
    def add_event(self, event_name: str, start_date: str, end_date: str, 
                  bonus_multiplier: float = 1.0, special_rewards: list = None):
        self.events.append({
            "name": event_name,
            "start": start_date,
            "end": end_date,
            "bonus_multiplier": bonus_multiplier,
            "special_rewards": special_rewards or []
        })
    
    def get_active_events(self) -> list:
        now = datetime.now()
        active_events = []
        
        for event in self.events:
            start_date = datetime.strptime(event["start"], "%Y-%m-%d")
            end_date = datetime.strptime(event["end"], "%Y-%m-%d")
            
            if start_date <= now <= end_date:
                active_events.append(event)
        
        return active_events

# -----------------------------
# 11. Shopkeeper Management System
# -----------------------------
class Shopkeeper:
    def __init__(self, shop_id: str, shop_name: str, category: str):
        self.shop_id = shop_id
        self.shop_name = shop_name
        self.category = category
        self.total_sales = 0
        self.customer_count = 0
        self.rating = 5.0
        self.reviews = []
        self.special_offers = []
        self.inventory = []
    
    def add_sale(self, amount: float, customer_id: str):
        self.total_sales += amount
        self.customer_count += 1
        
        # Generate special offer based on sales performance
        if self.total_sales > 10000:
            self.special_offers.append({
                "type": "discount",
                "value": "20% off",
                "valid_until": datetime.now() + timedelta(days=7)
            })
    
    def add_review(self, rating: int, comment: str, customer_id: str):
        self.reviews.append({
            "rating": rating,
            "comment": comment,
            "customer_id": customer_id,
            "timestamp": datetime.now()
        })
        
        # Update average rating
        total_rating = sum(review["rating"] for review in self.reviews)
        self.rating = total_rating / len(self.reviews)

# -----------------------------
# 12. Customer Service System
# -----------------------------
class CustomerService:
    def __init__(self):
        self.tickets = []
        self.responses = {
            "receipt_issue": {
                "en": "We're investigating your receipt issue. Please allow 24-48 hours for review.",
                "ar": "نحن نتحقق من مشكلة الفاتورة. يرجى السماح بـ 24-48 ساعة للمراجعة."
            },
            "coin_missing": {
                "en": "Your missing coins have been restored. Thank you for your patience.",
                "ar": "تم استعادة العملات المفقودة. شكراً لصبرك."
            },
            "technical_issue": {
                "en": "Our technical team is working on resolving this issue.",
                "ar": "فريقنا التقني يعمل على حل هذه المشكلة."
            }
        }
    
    def create_ticket(self, user_id: str, issue_type: str, description: str, language: str = "en"):
        ticket = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "issue_type": issue_type,
            "description": description,
            "status": "open",
            "created_at": datetime.now(),
            "language": language,
            "assigned_to": None
        }
        self.tickets.append(ticket)
        return ticket["id"]
    
    def respond_to_ticket(self, ticket_id: str, response: str, agent_id: str):
        for ticket in self.tickets:
            if ticket["id"] == ticket_id:
                ticket["status"] = "resolved"
                ticket["response"] = response
                ticket["resolved_by"] = agent_id
                ticket["resolved_at"] = datetime.now()
                break

# -----------------------------
# 13. Main System Controller
# -----------------------------
class MallGamificationSystem:
    def __init__(self):
        self.users = {}
        self.shopkeepers = {}
        self.suspicious_receipts = []  # Add suspicious receipts list
        self.multilingual = MultilingualSystem()
        self.mission_generator = AIMissionGenerator()
        self.personalized_mission_generator = PersonalizedMissionGenerator()
        self.intelligent_reward_system = IntelligentRewardSystem()
        self.event_scheduler = EventScheduler()
        self.flash_events = FlashEventManager()
        self.flash_event_admin = FlashEventAdminInterface(self.flash_events)
        self.customer_service = CustomerService()
        self.abu_dhabi_features = AbuDhabiSpecialFeatures()
        self.wheel_of_fortune = WheelOfFortune(self)

        # Initialize WebAR Treasure Hunt if available
        self.webar_available = WEBAR_TREASURE_AVAILABLE
        if self.webar_available:
            self.webar_treasure_hunt = WebARTreasureHunt()
            logger.info("[SYSTEM] WebAR Treasure Hunt initialized")
        else:
            self.webar_treasure_hunt = None
            logger.warning("[SYSTEM] WebAR Treasure Hunt not available")
        
        # Initialize security and performance modules if available
        if SECURITY_PERFORMANCE_AVAILABLE:
            self.security_manager = get_security_manager()
            self.secure_database = get_secure_database()
            self.performance_manager = get_performance_manager()
            self.performance_monitor = get_performance_monitor()
            logger.info("[✅] Security and Performance modules integrated")
        else:
            self.security_manager = None
            self.secure_database = None
            self.performance_manager = None
            self.performance_monitor = None
            logger.warning("[⚠️] Security and Performance modules not available")
        
        # Social features
        self.leaderboards = {
            'coins': [],
            'xp': [],
            'streak': [],
            'achievements': [],
            'spending': []
        }
        
        # Team system
        self.teams = {}

        # Event management
        self.active_events = []
        self.team_challenges = {}

        # Event logging
        self.event_log = []
        
        # Initialize 3D Graphics if available
        self.graphics_3d_available = GRAPHICS_3D_AVAILABLE
        if self.graphics_3d_available:
            try:
                initialize_3d_system()
                logger.info("[SYSTEM] 3D Graphics system initialized successfully")
            except Exception as e:
                logger.warning(f"[SYSTEM] 3D Graphics initialization failed: {e}")
                self.graphics_3d_available = False

        # Initialize Database if available
        self.database_available = DATABASE_AVAILABLE
        if self.database_available:
            logger.info("[SYSTEM] Database system initialized successfully")
        else:
            logger.info("[SYSTEM] Using in-memory storage")

        # Initialize AI Mission Generator if available
        self.ai_missions_available = AI_MISSIONS_AVAILABLE
        if self.ai_missions_available:
            logger.info("[SYSTEM] AI Mission Generator initialized successfully")

        # Initialize WiFi Verification if available
        self.wifi_verification_available = WIFI_VERIFICATION_AVAILABLE
        if self.wifi_verification_available:
            logger.info("[SYSTEM] WiFi Verification system initialized successfully")

        # Initialize Companion System if available
        self.companion_system_available = COMPANION_SYSTEM_AVAILABLE
        if self.companion_system_available:
            logger.info("[SYSTEM] Companion System initialized successfully")
        
        # Initialize some sample data
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        # Add sample shopkeepers
        self.shopkeepers["store1"] = Shopkeeper("store1", "Deerfields Fashion", "clothing")
        self.shopkeepers["store2"] = Shopkeeper("store2", "Deerfields Electronics", "electronics")
        self.shopkeepers["store3"] = Shopkeeper("store3", "Deerfields Café", "food")
        
        # Add sample events
        self.event_scheduler.add_event("Summer Sale", "2024-06-01", "2024-06-30", 1.5, ["Summer Coins"])
        self.event_scheduler.add_event("Back to School", "2024-08-15", "2024-09-15", 1.3, ["School Supplies"])
 codex/clean-up-sample-data-initialization
        # Initialize sample flash event zone and event for time-bound promotions
=======

        # Initialize sample flash event zone and event
 main
        self.flash_event_admin.define_zone("center_court", (0.0, 0.0), 50.0)
        self.flash_event_admin.schedule_event(
            "Weekend Blast",
            datetime.now() - timedelta(days=1),
            datetime.now() + timedelta(days=1),
            ["center_court"],
            multiplier=1.2,
        )
        self.activate_events()

    def activate_events(self):
        """Update active flash events based on current time."""
        events = self.flash_events.activate_events()
        self.active_events = [e.name for e in events]
        return events

    def deactivate_event(self, name: str) -> None:
        """Deactivate a flash event."""
        self.flash_events.deactivate_event(name)
        self.active_events = [e.name for e in self.flash_events.activate_events()]

    def track_event_participation(self, user_id: str, event_name: str, progress: int = 1) -> bool:
        """Track participant progress in a flash event."""
        return self.flash_events.record_participation(event_name, user_id, progress)

    def get_event_progress(self, user_id: str, event_name: str) -> int:
        """Retrieve progress for a participant in a flash event."""
        return self.flash_events.get_participant_progress(event_name, user_id)

    def admin_define_zone(self, zone_id: str, coordinates: tuple, radius: float) -> None:
        """Admin interface to define AR zones."""
        self.flash_event_admin.define_zone(zone_id, coordinates, radius)

    def admin_schedule_flash_event(
        self,
        name: str,
        start: datetime,
        end: datetime,
        zone_ids: list,
        multiplier: float = 1.0,
    ) -> None:
        """Admin interface to schedule flash events."""
        self.flash_event_admin.schedule_event(name, start, end, zone_ids, multiplier)



    def log_event(self, event_type: str, details: dict):
        """Record system events for auditing and analytics."""
        self.event_log.append({
            'type': event_type,
            'details': details,
            'timestamp': datetime.now()
        })

    def handle_coin_duel_result(self, duel_id: str, winner_id: str, loser_id: str, scores: dict):
        """Allocate rewards to duel winner and log the outcome."""
        reward = 50
        winner = self.get_user(winner_id)
        loser = self.get_user(loser_id)
        if winner:
            winner.coins += reward
            winner.update_level()
            winner.rewards.append(f"🏆 Won coin duel against {loser_id} +{reward} coins")
        if loser:
            loser.rewards.append(f"🎮 Lost coin duel against {winner_id}")
        self.log_event('coin_duel_completed', {
            'duel_id': duel_id,
            'winner': winner_id,
            'loser': loser_id,
            'scores': scores,
            'reward': reward
        })
        return {'winner': winner_id, 'loser': loser_id, 'reward': reward}

 codex/clean-up-sample-data-initialization
    def spin_wheel(self, user_id: str):
        """Expose wheel of fortune spin for users."""
        return self.wheel_of_fortune.spin(user_id)

=======
    

    def spin_wheel(self, user_id: str):
        """Expose wheel of fortune spin for users."""
        return self.wheel_of_fortune.spin(user_id)
 main
    def create_user(self, user_id: str, language: str = "en") -> User:
        """Create a new user with smart caching"""
        if SMART_CACHE_AVAILABLE:
            # Use SmartCacheManager
            cached_user_data = user_data.get_user_data(user_id)
            if not cached_user_data:
                new_user = User(user_id)
                new_user.language = language
                user_data_dict = {
                    'user_id': user_id,
                    'language': language,
                    'coins': 0,
                    'level': 1,
                    'xp': 0,
                    'vip_tier': 'Bronze',
                    'login_streak': 0,
                    'last_login': datetime.now().isoformat(),
                    'purchases': [],
                    'missions': [],
                    'companions': []
                }
                user_data.set_user_data(user_id, user_data_dict)
                self.users[user_id] = new_user
            else:
                self.users[user_id] = User(user_id)
                self.users[user_id].language = cached_user_data.get('language', language)
        else:
            # Fallback to basic storage
            if user_id not in self.users:
                self.users[user_id] = User(user_id)
                self.users[user_id].language = language
        return self.users[user_id]
    
    def get_user(self, user_id: str) -> User:
        """Get user by ID with smart caching"""
        if SMART_CACHE_AVAILABLE:
            # Use SmartCacheManager
            cached_user_data = user_data.get_user_data(user_id)
            if cached_user_data:
                if user_id not in self.users:
                    self.users[user_id] = User(user_id)
                    self.users[user_id].language = cached_user_data.get('language', 'en')
                return self.users[user_id]
            return None
        else:
            # Fallback to basic storage
            return self.users.get(user_id)
    
    def process_receipt(self, user_id: str, amount: float, store: str):
        """Process receipt with intelligent rewards and security"""
        start_time = time.time()
        
        user = self.get_user(user_id)
        if not user:
            return {"status": "error", "message": "User not found"}
        
        # Security logging if available
        if self.security_manager:
            log_security_event('receipt_submission', {
                'user_id': user_id,
                'amount': amount,
                'store': store,
                'timestamp': datetime.now().isoformat()
            })
        
        # Determine store category
        store_category = self.determine_store_category(store)
        
        # Calculate intelligent rewards
        user_profile = {
            'vip_tier': user.vip_tier,
            'login_streak': user.login_streak,
            'total_spent': user.total_spent,
            'visited_categories': user.visited_categories,
            'total_purchases': user.total_purchases
        }
        
        context = {
            'category': store_category,
            'event_multiplier': self.get_active_event_multiplier(),
            'time_of_day': self.get_time_period()
        }
        
        reward_result = self.intelligent_reward_system.calculate_dynamic_reward(
            amount, store_category, user_profile, context
        )

        # Apply rewards
        user.coins += reward_result['total_coins']
        user.add_xp(reward_result['xp_earned'], 'receipt_submission')
        logger.info(
            "Reward assigned to %s: +%s coins, +%s XP",
            user_id,
            reward_result['total_coins'],
            reward_result['xp_earned'],
        )
        
        # Add purchase record
        purchase_result = user.add_purchase(amount, store_category)
        
        # Add receipt record
        user.receipts.append({
            "store": store,
            "amount": amount,
            "coins": reward_result['total_coins'],
            "category": store_category,
            "timestamp": datetime.now(),
            "multipliers": reward_result['multiplier_breakdown']
        })
        
        # Update leaderboards
        self.update_leaderboards(user_id, reward_result['total_coins'], user.xp)
        
        # Update shopkeeper data
        for shopkeeper in self.shopkeepers.values():
            if shopkeeper.shop_name.lower() in store.lower():
                shopkeeper.add_sale(amount, user_id)
                break
        
        # Performance monitoring
        if self.performance_monitor:
            processing_time = time.time() - start_time
            record_performance_event('receipt_processing', processing_time)
        
        # Trigger visual effects
        trigger_visual_effect("receipt_submitted", {
            "coins": reward_result['total_coins'],
            "store": store,
            "celebration_level": reward_result['celebration_level'],
            "multipliers": reward_result['multiplier_breakdown']
        })
        
        return {
            "status": "success",
            "coins_earned": reward_result['total_coins'],
            "xp_earned": reward_result['xp_earned'],
            "bonus_rewards": reward_result['bonus_rewards'],
            "celebration_level": reward_result['celebration_level'],
            "multipliers": reward_result['multiplier_breakdown']
        }
    
    def generate_user_missions(self, user_id: str, mission_type: str = "daily"):
        """Generate personalized missions using AI"""
        user = self.get_user(user_id)
        if not user:
            return {"status": "error", "message": "User not found"}
        
        # Create user profile for personalization
        user_profile = {
            'level': user.level,
            'vip_tier': user.vip_tier,
            'total_spent': user.total_spent,
            'visited_categories': user.visited_categories,
            'total_purchases': user.total_purchases,
            'login_streak': user.login_streak,
            'preferred_categories': self.get_user_preferred_categories(user),
            'activity_frequency': self.get_user_activity_frequency(user)
        }
        
        # Generate personalized mission
        mission = self.personalized_mission_generator.generate_personalized_mission(
            user_profile, mission_type
        )
        
        user.missions.append(mission)
        
        # Security logging
        if self.security_manager:
            log_security_event('mission_generated', {
                'user_id': user_id,
                'mission_type': mission_type,
                'mission_id': mission['id']
            })
        
        return {
            "status": "success",
            "mission": mission,
            "personalized": True
        }
    
    def determine_store_category(self, store_name: str) -> str:
        """Determine store category based on name"""
        store_lower = store_name.lower()
        
        category_keywords = {
            'fashion': ['fashion', 'clothing', 'apparel', 'style', 'boutique', 'designer'],
            'electronics': ['electronics', 'tech', 'gadget', 'phone', 'computer', 'digital'],
            'food': ['food', 'restaurant', 'cafe', 'kitchen', 'dining', 'bakery'],
            'luxury': ['luxury', 'premium', 'exclusive', 'designer', 'high-end'],
            'books': ['book', 'library', 'reading', 'literature'],
            'sports': ['sport', 'fitness', 'gym', 'athletic', 'outdoor'],
            'beauty': ['beauty', 'cosmetic', 'makeup', 'skincare', 'salon'],
            'home': ['home', 'furniture', 'decor', 'kitchen', 'garden']
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in store_lower for keyword in keywords):
                return category
        
        return 'general'
    
    def get_active_event_multiplier(self) -> float:
        """Get active event multiplier"""
        scheduler_events = self.event_scheduler.get_active_events()
        flash_events = self.flash_events.activate_events()
        multiplier = 1.0
        if scheduler_events:
            scheduler_mult = max(event.get('bonus_multiplier', 1.0) for event in scheduler_events)
            multiplier = max(multiplier, scheduler_mult)
        if flash_events:
            flash_mult = max(event.multiplier for event in flash_events)
            multiplier = max(multiplier, flash_mult)
            self.active_events = [event.name for event in flash_events]
        return multiplier
    
    def get_time_period(self) -> str:
        """Get current time period"""
        hour = datetime.now().hour
        if 6 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 18:
            return 'afternoon'
        elif 18 <= hour < 22:
            return 'evening'
        else:
            return 'night'
    
    def get_user_preferred_categories(self, user: User) -> list:
        """Get user's preferred categories based on purchase history"""
        category_counts = {}
        for purchase in user.purchase_history:
            category = purchase.get('category', 'general')
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Return top 3 categories
        return sorted(category_counts.keys(), 
                     key=lambda x: category_counts[x], reverse=True)[:3]
    
    def get_user_activity_frequency(self, user: User) -> str:
        """Get user activity frequency"""
        if user.login_streak > 7:
            return 'high'
        elif user.login_streak > 3:
            return 'medium'
        else:
            return 'low'
    
    def update_leaderboards(self, user_id: str, coins: int, xp: int):
        """Update leaderboards"""
        # Update coins leaderboard
        self.update_leaderboard_entry('coins', user_id, coins)
        
        # Update XP leaderboard
        self.update_leaderboard_entry('xp', user_id, xp)
        
        # Update streak leaderboard
        user = self.get_user(user_id)
        if user:
            self.update_leaderboard_entry('streak', user_id, user.login_streak)
            self.update_leaderboard_entry('achievements', user_id, len(user.achievements))
            self.update_leaderboard_entry('spending', user_id, user.total_spent)
    
    def update_leaderboard_entry(self, leaderboard_type: str, user_id: str, score: int):
        """Update a specific leaderboard entry"""
        if leaderboard_type not in self.leaderboards:
            self.leaderboards[leaderboard_type] = []
        
        # Find existing entry
        existing_entry = None
        for entry in self.leaderboards[leaderboard_type]:
            if entry.get('user_id') == user_id:
                existing_entry = entry
                break
        
        if existing_entry:
            existing_entry['score'] = score
            existing_entry['updated_at'] = datetime.now()
        else:
            self.leaderboards[leaderboard_type].append({
                'user_id': user_id,
                'score': score,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            })
        
        # Sort leaderboard
        self.leaderboards[leaderboard_type].sort(key=lambda x: x.get('score', 0), reverse=True)
    
    def get_leaderboard(self, leaderboard_type: str, limit: int = 10) -> list:
        """Get leaderboard for a specific type"""
        if leaderboard_type not in self.leaderboards:
            return []
        
        return self.leaderboards[leaderboard_type][:limit]
    
    def create_team(self, team_name: str, creator_id: str) -> str:
        """Create a new team"""
        team_id = str(uuid.uuid4())
        team = {
            'id': team_id,
            'name': team_name,
            'creator_id': creator_id,
            'members': [creator_id],
            'score': 0,
            'created_at': datetime.now(),
            'challenges': []
        }
        self.teams[team_id] = team
        
        # Add user to team
        user = self.get_user(creator_id)
        if user:
            user.join_team(team_id)
        
        return team_id
    
    def join_team(self, user_id: str, team_id: str) -> bool:
        """Join a team"""
        if team_id in self.teams:
            team = self.teams[team_id]
            if user_id not in team['members']:
                team['members'].append(user_id)
                
                # Update user's team
                user = self.get_user(user_id)
                if user:
                    user.join_team(team_id)
                
                return True
        return False
    
    def create_team_challenge(self, challenge_name: str, target_score: int, 
                            reward: dict, duration_days: int = 7) -> str:
        """Create a team challenge"""
        challenge_id = str(uuid.uuid4())
        challenge = {
            'id': challenge_id,
            'name': challenge_name,
            'target_score': target_score,
            'reward': reward,
            'duration_days': duration_days,
            'start_time': datetime.now(),
            'end_time': datetime.now() + timedelta(days=duration_days),
            'teams': {},
            'status': 'active'
        }
        self.team_challenges[challenge_id] = challenge
        return challenge_id
    
    def update_team_challenge_score(self, challenge_id: str, team_id: str, points: int):
        """Update team score in a challenge"""
        if challenge_id in self.team_challenges:
            challenge = self.team_challenges[challenge_id]
            if team_id not in challenge['teams']:
                challenge['teams'][team_id] = {'score': 0}
            
            challenge['teams'][team_id]['score'] += points
            
            # Update team's overall score
            if team_id in self.teams:
                self.teams[team_id]['score'] += points
    
    def get_user_dashboard(self, user_id: str, user_ip: str = "Deerfields_Free_WiFi"):
        """Get comprehensive user dashboard with all features"""
        user = self.get_user(user_id)
        if not user:
            return None
        
        available_features = get_available_features(user, user_ip)
        active_events = self.event_scheduler.get_active_events()
        
        # Get VIP benefits
        vip_benefits = user.get_vip_benefits()
        
        # Get leaderboard positions
        leaderboard_positions = {}
        for leaderboard_type in ['coins', 'xp', 'streak', 'achievements', 'spending']:
            leaderboard = self.get_leaderboard(leaderboard_type, 100)
            for i, entry in enumerate(leaderboard):
                if entry.get('user_id') == user_id:
                    leaderboard_positions[leaderboard_type] = i + 1
                    break
        
        # Get team information
        team_info = None
        if user.team_id and user.team_id in self.teams:
            team = self.teams[user.team_id]
            team_info = {
                'team_id': team['id'],
                'team_name': team['name'],
                'members_count': len(team['members']),
                'team_score': team['score'],
                'position': self.get_team_leaderboard_position(team['id'])
            }
        
        # Get active team challenges
        active_challenges = []
        for challenge_id, challenge in self.team_challenges.items():
            if challenge['status'] == 'active' and challenge['end_time'] > datetime.now():
                if user.team_id and user.team_id in challenge['teams']:
                    team_score = challenge['teams'][user.team_id]['score']
                    active_challenges.append({
                        'challenge_id': challenge_id,
                        'name': challenge['name'],
                        'target_score': challenge['target_score'],
                        'team_score': team_score,
                        'progress': min(100, (team_score / challenge['target_score']) * 100),
                        'days_remaining': (challenge['end_time'] - datetime.now()).days
                    })
        
        # Get performance metrics if available
        performance_metrics = None
        if self.performance_monitor:
            performance_metrics = self.performance_monitor.get_performance_report()
        
        return {
            "user_info": {
                "user_id": user.user_id,
                "coins": user.coins,
                "xp": user.xp,
                "level": user.level,
                "vip_tier": user.vip_tier,
                "vip_points": user.vip_points,
                "language": user.language,
                "total_spent": user.total_spent,
                "total_purchases": user.total_purchases,
                "achievement_points": user.achievement_points,
                "social_score": user.social_score
            },
            "vip_benefits": vip_benefits,
            "available_features": available_features,
            "active_events": active_events,
            "recent_rewards": user.rewards[-5:],
            "missions": user.missions,
            "login_streak": user.login_streak,
            "companion": user.companion,
            "achievements": user.achievements,
            "leaderboard_positions": leaderboard_positions,
            "team_info": team_info,
            "active_challenges": active_challenges,
            "friends": user.friends,
            "performance_metrics": performance_metrics,
            "visited_categories": user.visited_categories,
            "purchase_history": user.purchase_history[-10:],  # Last 10 purchases
            "webar_available": self.webar_available,
            "webar_attempts": self.webar_treasure_hunt.get_remaining_attempts(user_id)
            if self.webar_available else 0,
        }
    
    def get_team_leaderboard_position(self, team_id: str) -> int:
        """Get team's position in team leaderboard"""
        team_scores = []
        for team in self.teams.values():
            team_scores.append((team['id'], team['score']))
        
        # Sort by score
        team_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Find position
        for i, (tid, score) in enumerate(team_scores):
            if tid == team_id:
                return i + 1
        
        return 0
    
    def get_admin_dashboard(self):
        total_users = len(self.users)
        total_coins = sum(user.coins for user in self.users.values())
        suspicious_count = len(suspicious_receipts)
        
        return {
            "total_users": total_users,
            "total_coins": total_coins,
            "suspicious_receipts": suspicious_count,
            "active_events": self.event_scheduler.get_active_events(),
            "flash_events": [
                {
                    "name": e.name,
                    "start": e.start,
                    "end": e.end,
                    "zones": e.zones,
                    "multiplier": e.multiplier,
                }
                for e in self.flash_events.activate_events()
            ],
            "ar_zones": {
                zone_id: {
                    "name": zone.name,
                    "coordinates": zone.coordinates,
                    "radius": zone.radius,
                }
                for zone_id, zone in self.flash_events.zones.items()
            },
            "shopkeeper_stats": {
                shop_id: {
                    "total_sales": shopkeeper.total_sales,
                    "customer_count": shopkeeper.customer_count,
                    "rating": shopkeeper.rating
                }
                for shop_id, shopkeeper in self.shopkeepers.items()
            }
        }
    
    def get_shopkeeper_dashboard(self, shop_id: str):
        shopkeeper = self.shopkeepers.get(shop_id)
        if not shopkeeper:
            return None
        
        return {
            "shop_info": {
                "shop_id": shopkeeper.shop_id,
                "shop_name": shopkeeper.shop_name,
                "category": shopkeeper.category
            },
            "stats": {
                "total_sales": shopkeeper.total_sales,
                "customer_count": shopkeeper.customer_count,
                "rating": shopkeeper.rating
            },
            "recent_reviews": shopkeeper.reviews[-5:],
            "special_offers": shopkeeper.special_offers
        }
    
    def get_customer_service_dashboard(self):
        open_tickets = [t for t in self.customer_service.tickets if t["status"] == "open"]
        resolved_tickets = [t for t in self.customer_service.tickets if t["status"] == "resolved"]
        
        return {
            "open_tickets": len(open_tickets),
            "resolved_tickets": len(resolved_tickets),
            "recent_tickets": self.customer_service.tickets[-10:],
            "response_templates": self.customer_service.responses
        }
    
    def enhanced_process_receipt(self, user_id: str, amount: float, store: str, receipt_image: str = None):
        """Enhanced receipt processing with database and 3D effects"""
        try:
            user = self.get_user(user_id)
            if not user:
                return {"status": "error", "message": "User not found"}
            
            # Verify WiFi connection if available
            if self.wifi_verification_available:
                wifi_status = wifi_verification.is_inside_mall()
                if not wifi_status:
                    return {"status": "error", "message": "Must be connected to mall WiFi"}
            
            # Process receipt
            submit_receipt(user, amount, store)
            
            # Save to database if available
            if self.database_available:
                receipt_data = {
                    "receipt_id": f"receipt_{int(time.time())}_{random.randint(1000, 9999)}",
                    "user_id": user_id,
                    "store_name": store,
                    "amount": amount,
                    "receipt_image": receipt_image,
                    "ai_verification_status": "verified",
                    "ai_confidence": 0.95
                }
                db.add_receipt(receipt_data)
                
                # Add activity log
                activity_data = {
                    "activity_id": f"activity_{int(time.time())}_{random.randint(1000, 9999)}",
                    "user_id": user_id,
                    "activity_type": "receipt_scan",
                    "description": f"Scanned receipt from {store}",
                    "coins_earned": int(amount // 10),
                    "xp_earned": int(amount // 5),
                    "metadata": {"store": store, "amount": amount}
                }
                db.add_activity(activity_data)
            
            # Add companion XP if available
            if self.companion_system_available:
                companion_system.add_companion_xp(user_id, int(amount // 5), "receipt_scan")
            
            # Trigger 3D visual effects
            trigger_visual_effect("receipt_submitted", {
                "coins": int(amount // 10),
                "store": store,
                "amount": amount
            })
            
            return {
                "status": "success",
                "coins_earned": int(amount // 10),
                "xp_earned": int(amount // 5),
                "message": f"Receipt processed successfully! Earned {int(amount // 10)} coins"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error processing receipt: {str(e)}"}
    
    def generate_ai_missions(self, user_id: str, mission_type: str = "daily"):
        """Generate AI-powered personalized missions"""
        try:
            if not self.ai_missions_available:
                return self.generate_user_missions(user_id, mission_type)
            
            user = self.get_user(user_id)
            if not user:
                return {"status": "error", "message": "User not found"}
            
            if mission_type == "daily":
                missions = ai_mission_generator.generate_daily_missions(user_id, 3)
            elif mission_type == "weekly":
                missions = ai_mission_generator.generate_weekly_missions(user_id, 5)
            else:
                missions = ai_mission_generator.generate_daily_missions(user_id, 1)
            
            # Save missions to database if available
            if self.database_available:
                for mission in missions:
                    db.add_mission(mission)
            
            # Add to user's mission list
            user.missions.extend(missions)
            
            return {
                "status": "success",
                "missions": missions,
                "count": len(missions)
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error generating missions: {str(e)}"}

    def participate_treasure_hunt(self, user_id: str):
        """Participate in the WebAR Treasure Hunt."""
        try:
            if not self.webar_available:
                return {"status": "error", "message": "WebAR Treasure Hunt not available"}

            user = self.get_user(user_id)
            if not user:
                return {"status": "error", "message": "User not found"}

            result = self.webar_treasure_hunt.participate(user_id)
            if result.get("status") == "success":
                coins = result.get("coins", 0)
                user.coins += coins
                user.rewards.append(f"AR Treasure Hunt reward: +{coins} coins")
                mission = {
                    "id": str(uuid.uuid4()),
                    "type": "ar_treasure_hunt",
                    "title": "AR Treasure Hunt",
                    "progress": 1,
                    "target": 1,
                    "reward": coins,
                    "xp_reward": int(coins * 0.5),
                    "completed": True,
                }
                user.missions.append(mission)
            return result
        except Exception as e:
            return {"status": "error", "message": f"Error in treasure hunt: {str(e)}"}

    def create_companion(self, user_id: str, companion_type: str, name: str = None):
        """Create a companion for the user"""
        try:
            if not self.companion_system_available:
                return {"status": "error", "message": "Companion system not available"}
            
            result = companion_system.create_companion(user_id, companion_type, name)
            
            if result["status"] == "success":
                # Update user's companion reference
                user = self.get_user(user_id)
                if user:
                    user.companion = result["companion"]
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Error creating companion: {str(e)}"}
    
    def feed_companion(self, user_id: str, food_type: str = "regular"):
        """Feed the user's companion"""
        try:
            if not self.companion_system_available:
                return {"status": "error", "message": "Companion system not available"}
            
            return companion_system.feed_companion(user_id, food_type)
            
        except Exception as e:
            return {"status": "error", "message": f"Error feeding companion: {str(e)}"}
    
    def use_companion_ability(self, user_id: str, ability_name: str):
        """Use a companion ability"""
        try:
            if not self.companion_system_available:
                return {"status": "error", "message": "Companion system not available"}
            
            return companion_system.use_companion_ability(user_id, ability_name)
            
        except Exception as e:
            return {"status": "error", "message": f"Error using companion ability: {str(e)}"}
    
    def get_companion_stats(self, user_id: str):
        """Get companion statistics"""
        try:
            if not self.companion_system_available:
                return {"status": "error", "message": "Companion system not available"}
            
            return companion_system.get_companion_stats(user_id)
            
        except Exception as e:
            return {"status": "error", "message": f"Error getting companion stats: {str(e)}"}
    
    def check_wifi_status(self, user_id: str = None):
        """Check WiFi connection status"""
        try:
            if not self.wifi_verification_available:
                return {"status": "error", "message": "WiFi verification not available"}
            
            network_quality = wifi_verification.get_network_quality()
            mall_networks = wifi_verification.get_mall_networks()
            
            return {
                "status": "success",
                "network_quality": network_quality,
                "mall_networks": mall_networks,
                "is_inside_mall": wifi_verification.is_inside_mall()
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error checking WiFi status: {str(e)}"}
    
    def get_available_features(self, user: User, user_ip: str):
        """Get available features based on user location"""
        if is_inside_mall(user_ip):
            return ["earn_coins", "submit_receipt", "play_games", "join_challenges"]
        else:
            return ["browse_offers", "view_stores", "view_own_profile"]
    
    def get_system_stats(self):
        """Get comprehensive system statistics"""
        try:
            stats = {
                "total_users": len(self.users),
                "total_coins": sum(user.coins for user in self.users.values()),
                "suspicious_receipts": len(suspicious_receipts),
                "active_events": self.event_scheduler.get_active_events()
            }
            
            # Add database stats if available
            if self.database_available:
                db_stats = db.get_system_stats()
                stats.update(db_stats)
            
            # Add WiFi status if available
            if self.wifi_verification_available:
                stats["wifi_status"] = wifi_verification.get_network_quality()
            
            return {
                "status": "success",
                "stats": stats
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error getting system stats: {str(e)}"}

# -----------------------------
# 14. Example Usage and Testing
# -----------------------------
if __name__ == "__main__":
    # Initialize the system
    mall_system = MallGamificationSystem()
    
    # Create a test user
    test_user = mall_system.create_user("user123", "en")
    test_user.login()
    
    # Process some receipts
    mall_system.process_receipt("user123", 150.0, "Deerfields Fashion")
    mall_system.process_receipt("user123", 75.0, "Deerfields Electronics")
    
    # Generate missions
    mall_system.generate_user_missions("user123", "daily")
    
    # Get dashboards
    user_dashboard = mall_system.get_user_dashboard("user123")
    admin_dashboard = mall_system.get_admin_dashboard()
    shopkeeper_dashboard = mall_system.get_shopkeeper_dashboard("store1")
    cs_dashboard = mall_system.get_customer_service_dashboard()
    
    logger.info("=== USER DASHBOARD ===")
    logger.info(json.dumps(user_dashboard, indent=2, default=str))
    
    logger.info("\n=== ADMIN DASHBOARD ===")
    logger.info(json.dumps(admin_dashboard, indent=2, default=str))
    
    logger.info("\n=== SHOPKEEPER DASHBOARD ===")
    logger.info(json.dumps(shopkeeper_dashboard, indent=2, default=str))
    
    logger.info("\n=== CUSTOMER SERVICE DASHBOARD ===")
    logger.info(json.dumps(cs_dashboard, indent=2, default=str)) 

# Integration of Treasure Hunt
from ar_treasure_hunt import TreasureHuntManager

