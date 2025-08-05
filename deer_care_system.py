#!/usr/bin/env python3
"""
Deer Care System for Deerfields Mall Gamification System
Allows players to care for deer companions with feeding, entertainment, and shelter mechanics
"""

import random
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from database import db

class DeerCareSystem:
    """Deer care system with feeding, entertainment, and shelter mechanics"""
    
    def __init__(self):
        self.deer_types = {
            "arabian_oryx": {
                "name": "Arabian Oryx",
                "description": "Majestic desert deer with golden horns",
                "base_stats": {"health": 100, "happiness": 80, "energy": 90, "hunger": 20},
                "growth_rate": {"health": 2, "happiness": 3, "energy": 2, "hunger": -1},
                "max_level": 50,
                "abilities": ["desert_adaptation", "herd_leader", "water_conservation", "heat_resistance"],
                "visual_effects": ["golden_glow", "horn_sparkle", "desert_wind", "majestic_pose"],
                "preferred_food": ["desert_grass", "cactus_fruit", "fresh_water"],
                "entertainment": ["desert_exploration", "herd_gathering", "water_finding", "star_gazing"]
            },
            "gazelle": {
                "name": "Desert Gazelle",
                "description": "Swift and graceful desert gazelle",
                "base_stats": {"health": 85, "happiness": 90, "energy": 95, "hunger": 15},
                "growth_rate": {"health": 1.5, "happiness": 4, "energy": 3, "hunger": -1.5},
                "max_level": 45,
                "abilities": ["swift_movement", "acrobatic_jumps", "keen_senses", "social_bonding"],
                "visual_effects": ["speed_trail", "graceful_movement", "social_glow", "playful_bounce"],
                "preferred_food": ["fresh_grass", "herbs", "clean_water", "fruits"],
                "entertainment": ["racing_games", "jumping_contests", "social_play", "exploration"]
            },
            "mountain_deer": {
                "name": "Mountain Deer",
                "description": "Strong mountain deer with impressive antlers",
                "base_stats": {"health": 120, "happiness": 75, "energy": 85, "hunger": 25},
                "growth_rate": {"health": 3, "happiness": 2, "energy": 2.5, "hunger": -2},
                "max_level": 60,
                "abilities": ["mountain_climbing", "antler_strength", "weather_resistance", "territory_guard"],
                "visual_effects": ["mountain_aura", "antler_glow", "strength_particles", "territory_mark"],
                "preferred_food": ["mountain_herbs", "bark", "mineral_salt", "fresh_water"],
                "entertainment": ["mountain_climbing", "antler_showcase", "territory_patrol", "strength_training"]
            }
        }
        
        self.food_types = {
            "desert_grass": {"health": 10, "happiness": 5, "energy": 8, "cost": 5},
            "fresh_grass": {"health": 8, "happiness": 8, "energy": 10, "cost": 8},
            "mountain_herbs": {"health": 15, "happiness": 3, "energy": 12, "cost": 12},
            "cactus_fruit": {"health": 5, "happiness": 12, "energy": 6, "cost": 6},
            "herbs": {"health": 6, "happiness": 10, "energy": 7, "cost": 7},
            "bark": {"health": 12, "happiness": 2, "energy": 15, "cost": 10},
            "fruits": {"health": 4, "happiness": 15, "energy": 5, "cost": 9},
            "mineral_salt": {"health": 20, "happiness": 1, "energy": 8, "cost": 15},
            "fresh_water": {"health": 3, "happiness": 3, "energy": 20, "cost": 3},
            "clean_water": {"health": 2, "happiness": 4, "energy": 18, "cost": 4},
            "premium_feed": {"health": 25, "happiness": 20, "energy": 25, "cost": 25}
        }
        
        self.entertainment_activities = {
            "desert_exploration": {"happiness": 15, "energy": -5, "cost": 10},
            "herd_gathering": {"happiness": 20, "energy": -3, "cost": 8},
            "water_finding": {"happiness": 10, "energy": -8, "cost": 12},
            "star_gazing": {"happiness": 25, "energy": -2, "cost": 5},
            "racing_games": {"happiness": 18, "energy": -10, "cost": 15},
            "jumping_contests": {"happiness": 22, "energy": -12, "cost": 18},
            "social_play": {"happiness": 30, "energy": -6, "cost": 10},
            "exploration": {"happiness": 12, "energy": -7, "cost": 8},
            "mountain_climbing": {"happiness": 16, "energy": -15, "cost": 20},
            "antler_showcase": {"happiness": 28, "energy": -4, "cost": 12},
            "territory_patrol": {"happiness": 14, "energy": -9, "cost": 14},
            "strength_training": {"happiness": 20, "energy": -14, "cost": 16}
        }
        
        self.shelter_types = {
            "basic_shelter": {
                "name": "Basic Deer Shelter",
                "description": "Simple shelter providing basic protection",
                "health_boost": 5,
                "happiness_boost": 3,
                "energy_boost": 2,
                "cost": 50,
                "capacity": 1
            },
            "desert_oasis": {
                "name": "Desert Oasis Shelter",
                "description": "Luxurious oasis with water and shade",
                "health_boost": 15,
                "happiness_boost": 20,
                "energy_boost": 10,
                "cost": 200,
                "capacity": 3
            },
            "mountain_lodge": {
                "name": "Mountain Lodge Shelter",
                "description": "Sturdy mountain lodge with panoramic views",
                "health_boost": 20,
                "happiness_boost": 15,
                "energy_boost": 15,
                "cost": 300,
                "capacity": 5
            },
            "royal_pavilion": {
                "name": "Royal Deer Pavilion",
                "description": "Ultimate luxury shelter for royal deer",
                "health_boost": 30,
                "happiness_boost": 35,
                "energy_boost": 25,
                "cost": 500,
                "capacity": 10
            }
        }
    
    def create_deer(self, user_id: str, deer_type: str = "arabian_oryx") -> Dict[str, Any]:
        """Create a new deer companion for the user"""
        try:
            if deer_type not in self.deer_types:
                return {"status": "error", "message": "Invalid deer type"}
            
            deer_template = self.deer_types[deer_type]
            deer = {
                "user_id": user_id,
                "deer_id": f"deer_{user_id}_{int(time.time())}",
                "type": deer_type,
                "name": deer_template["name"],
                "description": deer_template["description"],
                "level": 1,
                "xp": 0,
                "health": deer_template["base_stats"]["health"],
                "happiness": deer_template["base_stats"]["happiness"],
                "energy": deer_template["base_stats"]["energy"],
                "hunger": deer_template["base_stats"]["hunger"],
                "abilities": deer_template["abilities"][:2],  # Start with 2 abilities
                "visual_effects": deer_template["visual_effects"][:1],  # Start with 1 effect
                "preferred_food": deer_template["preferred_food"],
                "entertainment": deer_template["entertainment"],
                "shelter": None,
                "last_fed": None,
                "last_entertained": None,
                "created_at": datetime.now().isoformat(),
                "last_care": datetime.now().isoformat()
            }
            
            # Save to database
            if DATABASE_AVAILABLE:
                db.save_deer(deer)
            else:
                # Fallback to memory storage
                if not hasattr(self, 'deer_storage'):
                    self.deer_storage = {}
                self.deer_storage[deer["deer_id"]] = deer
            
            print(f"🦌 Created {deer['name']} for user {user_id}")
            return {"status": "success", "deer": deer}
            
        except Exception as e:
            return {"status": "error", "message": f"Error creating deer: {str(e)}"}
    
    def get_deer(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's deer companion"""
        try:
            if DATABASE_AVAILABLE:
                return db.get_deer(user_id)
            else:
                # Fallback to memory storage
                if hasattr(self, 'deer_storage'):
                    for deer_id, deer in self.deer_storage.items():
                        if deer["user_id"] == user_id:
                            return deer
                return None
        except Exception as e:
            print(f"Error getting deer: {e}")
            return None
    
    def feed_deer(self, user_id: str, food_type: str = "fresh_grass") -> Dict[str, Any]:
        """Feed the deer to increase health and reduce hunger"""
        try:
            deer = self.get_deer(user_id)
            if not deer:
                return {"status": "error", "message": "No deer found"}
            
            if food_type not in self.food_types:
                return {"status": "error", "message": "Invalid food type"}
            
            food_effects = self.food_types[food_type]
            
            # Check if deer is too full
            if deer["hunger"] < 10:
                return {"status": "error", "message": "Deer is not hungry"}
            
            # Apply food effects
            deer["health"] = min(100, deer["health"] + food_effects["health"])
            deer["happiness"] = min(100, deer["happiness"] + food_effects["happiness"])
            deer["energy"] = min(100, deer["energy"] + food_effects["energy"])
            deer["hunger"] = max(0, deer["hunger"] - 15)  # Reduce hunger
            deer["last_fed"] = datetime.now().isoformat()
            deer["last_care"] = datetime.now().isoformat()
            
            # Add XP for feeding
            xp_gained = 5 + (food_effects["cost"] // 5)
            deer["xp"] += xp_gained
            
            # Check for level up
            level_up_result = self._check_deer_level_up(deer)
            
            # Save to database
            if DATABASE_AVAILABLE:
                db.update_deer(deer["deer_id"], deer)
            else:
                if hasattr(self, 'deer_storage'):
                    self.deer_storage[deer["deer_id"]] = deer
            
            print(f"🦌 Fed {deer['name']} with {food_type} (+{xp_gained} XP)")
            return {
                "status": "success",
                "deer": deer,
                "food_effects": food_effects,
                "xp_gained": xp_gained,
                "level_up": level_up_result,
                "message": f"Fed {deer['name']} with {food_type}!"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error feeding deer: {str(e)}"}
    
    def entertain_deer(self, user_id: str, activity: str = "social_play") -> Dict[str, Any]:
        """Entertain the deer to increase happiness"""
        try:
            deer = self.get_deer(user_id)
            if not deer:
                return {"status": "error", "message": "No deer found"}
            
            if activity not in self.entertainment_activities:
                return {"status": "error", "message": "Invalid activity"}
            
            activity_effects = self.entertainment_activities[activity]
            
            # Check if deer has enough energy
            if deer["energy"] < abs(activity_effects["energy"]):
                return {"status": "error", "message": "Deer is too tired for this activity"}
            
            # Apply activity effects
            deer["happiness"] = min(100, deer["happiness"] + activity_effects["happiness"])
            deer["energy"] = max(0, deer["energy"] + activity_effects["energy"])  # energy is negative
            deer["last_entertained"] = datetime.now().isoformat()
            deer["last_care"] = datetime.now().isoformat()
            
            # Add XP for entertainment
            xp_gained = 8 + (activity_effects["cost"] // 10)
            deer["xp"] += xp_gained
            
            # Check for level up
            level_up_result = self._check_deer_level_up(deer)
            
            # Save to database
            if DATABASE_AVAILABLE:
                db.update_deer(deer["deer_id"], deer)
            else:
                if hasattr(self, 'deer_storage'):
                    self.deer_storage[deer["deer_id"]] = deer
            
            print(f"🎮 Entertained {deer['name']} with {activity} (+{xp_gained} XP)")
            return {
                "status": "success",
                "deer": deer,
                "activity_effects": activity_effects,
                "xp_gained": xp_gained,
                "level_up": level_up_result,
                "message": f"Entertained {deer['name']} with {activity}!"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error entertaining deer: {str(e)}"}
    
    def build_shelter(self, user_id: str, shelter_type: str = "basic_shelter") -> Dict[str, Any]:
        """Build a shelter for the deer"""
        try:
            deer = self.get_deer(user_id)
            if not deer:
                return {"status": "error", "message": "No deer found"}
            
            if shelter_type not in self.shelter_types:
                return {"status": "error", "message": "Invalid shelter type"}
            
            shelter_info = self.shelter_types[shelter_type]
            
            # Check if user has enough coins (this would be integrated with the main system)
            # For now, we'll assume they have enough
            
            # Apply shelter effects
            deer["health"] = min(100, deer["health"] + shelter_info["health_boost"])
            deer["happiness"] = min(100, deer["happiness"] + shelter_info["happiness_boost"])
            deer["energy"] = min(100, deer["energy"] + shelter_info["energy_boost"])
            deer["shelter"] = shelter_type
            deer["last_care"] = datetime.now().isoformat()
            
            # Add XP for building shelter
            xp_gained = 20 + (shelter_info["cost"] // 20)
            deer["xp"] += xp_gained
            
            # Check for level up
            level_up_result = self._check_deer_level_up(deer)
            
            # Save to database
            if DATABASE_AVAILABLE:
                db.update_deer(deer["deer_id"], deer)
            else:
                if hasattr(self, 'deer_storage'):
                    self.deer_storage[deer["deer_id"]] = deer
            
            print(f"🏠 Built {shelter_info['name']} for {deer['name']} (+{xp_gained} XP)")
            return {
                "status": "success",
                "deer": deer,
                "shelter": shelter_info,
                "xp_gained": xp_gained,
                "level_up": level_up_result,
                "message": f"Built {shelter_info['name']} for {deer['name']}!"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error building shelter: {str(e)}"}
    
    def get_deer_status(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive deer status and care recommendations"""
        try:
            deer = self.get_deer(user_id)
            if not deer:
                return {"status": "error", "message": "No deer found"}
            
            # Calculate care needs
            now = datetime.now()
            last_care = datetime.fromisoformat(deer["last_care"])
            hours_since_care = (now - last_care).total_seconds() / 3600
            
            care_needs = {
                "needs_food": deer["hunger"] > 50,
                "needs_entertainment": deer["happiness"] < 60,
                "needs_rest": deer["energy"] < 30,
                "needs_shelter": deer["shelter"] is None,
                "hours_since_care": hours_since_care
            }
            
            # Generate care recommendations
            recommendations = []
            if care_needs["needs_food"]:
                recommendations.append("Feed your deer to reduce hunger")
            if care_needs["needs_entertainment"]:
                recommendations.append("Entertain your deer to increase happiness")
            if care_needs["needs_rest"]:
                recommendations.append("Let your deer rest to regain energy")
            if care_needs["needs_shelter"]:
                recommendations.append("Build a shelter for your deer")
            
            return {
                "status": "success",
                "deer": deer,
                "care_needs": care_needs,
                "recommendations": recommendations
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error getting deer status: {str(e)}"}
    
    def _check_deer_level_up(self, deer: Dict[str, Any]) -> Dict[str, Any]:
        """Check if deer should level up and apply level up effects"""
        try:
            deer_template = self.deer_types[deer["type"]]
            xp_needed = deer["level"] * 50  # 50 XP per level
            
            if deer["xp"] >= xp_needed and deer["level"] < deer_template["max_level"]:
                old_level = deer["level"]
                deer["level"] += 1
                deer["xp"] -= xp_needed
                
                # Apply level up bonuses
                growth_rates = deer_template["growth_rate"]
                deer["health"] = min(100, deer["health"] + growth_rates["health"])
                deer["happiness"] = min(100, deer["happiness"] + growth_rates["happiness"])
                deer["energy"] = min(100, deer["energy"] + growth_rates["energy"])
                
                # Unlock new abilities and effects
                if len(deer["abilities"]) < len(deer_template["abilities"]):
                    new_ability = deer_template["abilities"][len(deer["abilities"])]
                    deer["abilities"].append(new_ability)
                
                if len(deer["visual_effects"]) < len(deer_template["visual_effects"]):
                    new_effect = deer_template["visual_effects"][len(deer["visual_effects"])]
                    deer["visual_effects"].append(new_effect)
                
                print(f"🎉 {deer['name']} leveled up to level {deer['level']}!")
                return {
                    "leveled_up": True,
                    "old_level": old_level,
                    "new_level": deer["level"],
                    "new_ability": new_ability if len(deer["abilities"]) > len(deer_template["abilities"]) - 1 else None,
                    "new_effect": new_effect if len(deer["visual_effects"]) > len(deer_template["visual_effects"]) - 1 else None
                }
            
            return {"leveled_up": False}
            
        except Exception as e:
            print(f"Error in level up check: {e}")
            return {"leveled_up": False}
    
    def get_available_food(self) -> Dict[str, Any]:
        """Get list of available food types"""
        return {"status": "success", "food_types": self.food_types}
    
    def get_available_activities(self) -> Dict[str, Any]:
        """Get list of available entertainment activities"""
        return {"status": "success", "activities": self.entertainment_activities}
    
    def get_available_shelters(self) -> Dict[str, Any]:
        """Get list of available shelter types"""
        return {"status": "success", "shelters": self.shelter_types}

# Initialize database availability
try:
    from database import db
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    print("[DEER CARE] Database module not available, using in-memory storage")

# Create global instance
deer_care_system = DeerCareSystem() 