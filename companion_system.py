#!/usr/bin/env python3
"""
Companion System for Deerfields Mall Gamification System
Provides enhanced companion mechanics with growth, visual effects, and level-up features
"""

import random
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from database import db

class CompanionSystem:
    """Enhanced companion system with growth mechanics and visual effects"""
    
    def __init__(self):
        self.companion_types = {
            "falcon_drone": {
                "name": "Falcon Drone",
                "description": "Traditional Emirati falcon companion",
                "base_stats": {"power": 1.0, "speed": 1.5, "intelligence": 1.2},
                "growth_rate": {"power": 0.2, "speed": 0.1, "intelligence": 0.15},
                "max_level": 50,
                "abilities": ["hover", "camera_feed", "light_effects", "falcon_vision"],
                "visual_effects": ["falcon_glow", "wing_flap", "hover_particles"]
            },
            "pet_cat": {
                "name": "Mall Cat",
                "description": "Friendly feline companion",
                "base_stats": {"power": 0.8, "speed": 1.8, "intelligence": 1.0},
                "growth_rate": {"power": 0.15, "speed": 0.2, "intelligence": 0.1},
                "max_level": 40,
                "abilities": ["stealth", "quick_movement", "curiosity", "playful"],
                "visual_effects": ["cat_purr", "tail_wag", "paw_prints"]
            },
            "flying_camera": {
                "name": "Flying Camera",
                "description": "Advanced aerial companion",
                "base_stats": {"power": 1.2, "speed": 1.3, "intelligence": 1.5},
                "growth_rate": {"power": 0.1, "speed": 0.15, "intelligence": 0.25},
                "max_level": 60,
                "abilities": ["aerial_view", "recording", "scanning", "mapping"],
                "visual_effects": ["camera_flash", "scan_lines", "hover_glow"]
            },
            "desert_fox": {
                "name": "Desert Fox",
                "description": "Clever desert companion",
                "base_stats": {"power": 0.9, "speed": 1.6, "intelligence": 1.3},
                "growth_rate": {"power": 0.18, "speed": 0.18, "intelligence": 0.2},
                "max_level": 45,
                "abilities": ["desert_navigation", "resource_finding", "stealth", "adaptation"],
                "visual_effects": ["fox_trail", "desert_wind", "sand_particles"]
            }
        }
        
        self.companion_states = {}
        self.visual_effects_queue = []
    
    def create_companion(self, user_id: str, companion_type: str, name: str = None) -> Dict[str, Any]:
        """Create a new companion for a user"""
        try:
            if companion_type not in self.companion_types:
                return {"status": "error", "message": "Invalid companion type"}
            
            companion_config = self.companion_types[companion_type]
            
            if not name:
                name = companion_config["name"]
            
            companion_data = {
                "companion_id": f"companion_{int(time.time())}_{random.randint(1000, 9999)}",
                "user_id": user_id,
                "name": name,
                "companion_type": companion_type,
                "level": 1,
                "xp": 0,
                "power": companion_config["base_stats"]["power"],
                "speed": companion_config["base_stats"]["speed"],
                "intelligence": companion_config["base_stats"]["intelligence"],
                "happiness": 100,
                "energy": 100,
                "hunger": 0,
                "last_fed": datetime.now().isoformat(),
                "last_activity": datetime.now().isoformat(),
                "abilities_unlocked": companion_config["abilities"][:1],  # Start with first ability
                "visual_effects": companion_config["visual_effects"][:1],
                "created_at": datetime.now().isoformat(),
                "growth_stage": "baby"
            }
            
            # Save to database
            if db.add_companion(companion_data):
                self.companion_states[user_id] = companion_data
                self._trigger_visual_effect("companion_created", companion_data)
                
                return {
                    "status": "success",
                    "companion": companion_data,
                    "message": f"Companion {name} created successfully!"
                }
            else:
                return {"status": "error", "message": "Failed to save companion to database"}
                
        except Exception as e:
            return {"status": "error", "message": f"Error creating companion: {str(e)}"}
    
    def get_companion(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's companion information"""
        try:
            # Check cache first
            if user_id in self.companion_states:
                return self.companion_states[user_id]
            
            # Get from database
            cursor = db.conn.execute('''
                SELECT * FROM companions WHERE user_id = ?
            ''', (user_id,))
            row = cursor.fetchone()
            
            if row:
                companion_data = dict(row)
                self.companion_states[user_id] = companion_data
                return companion_data
            
            return None
            
        except Exception as e:
            print(f"Error getting companion: {e}")
            return None
    
    def feed_companion(self, user_id: str, food_type: str = "regular") -> Dict[str, Any]:
        """Feed companion to increase happiness and energy"""
        try:
            companion = self.get_companion(user_id)
            if not companion:
                return {"status": "error", "message": "No companion found"}
            
            # Calculate feeding effects
            feeding_effects = self._calculate_feeding_effects(food_type)
            
            # Update companion stats
            companion["happiness"] = min(100, companion["happiness"] + feeding_effects["happiness"])
            companion["energy"] = min(100, companion["energy"] + feeding_effects["energy"])
            companion["hunger"] = max(0, companion["hunger"] - feeding_effects["hunger_reduction"])
            companion["last_fed"] = datetime.now().isoformat()
            
            # Check for level up from feeding
            level_up_result = self._check_level_up(companion)
            
            # Save to database
            db.update_companion(user_id, companion)
            
            # Trigger visual effects
            self._trigger_visual_effect("companion_fed", {
                "companion": companion,
                "food_type": food_type,
                "effects": feeding_effects,
                "level_up": level_up_result.get("leveled_up", False)
            })
            
            return {
                "status": "success",
                "companion": companion,
                "feeding_effects": feeding_effects,
                "level_up": level_up_result,
                "message": f"Fed {companion['name']} with {food_type} food!"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error feeding companion: {str(e)}"}
    
    def _calculate_feeding_effects(self, food_type: str) -> Dict[str, int]:
        """Calculate effects of different food types"""
        effects = {
            "regular": {"happiness": 10, "energy": 15, "hunger_reduction": 20},
            "premium": {"happiness": 20, "energy": 25, "hunger_reduction": 30},
            "luxury": {"happiness": 30, "energy": 35, "hunger_reduction": 40},
            "special": {"happiness": 25, "energy": 30, "hunger_reduction": 35, "xp_bonus": 10}
        }
        
        return effects.get(food_type, effects["regular"])
    
    def companion_level_up(self, user_id: str) -> Dict[str, Any]:
        """Level up companion and unlock new abilities"""
        try:
            companion = self.get_companion(user_id)
            if not companion:
                return {"status": "error", "message": "No companion found"}
            
            companion_type = companion["companion_type"]
            companion_config = self.companion_types[companion_type]
            
            # Calculate XP needed for next level
            current_level = companion["level"]
            xp_needed = current_level * 100
            
            if companion["xp"] < xp_needed:
                return {
                    "status": "error", 
                    "message": f"Not enough XP. Need {xp_needed - companion['xp']} more XP"
                }
            
            # Level up
            companion["level"] += 1
            companion["xp"] -= xp_needed
            
            # Increase stats
            growth_rate = companion_config["growth_rate"]
            companion["power"] += growth_rate["power"]
            companion["speed"] += growth_rate["speed"]
            companion["intelligence"] += growth_rate["intelligence"]
            
            # Update growth stage
            companion["growth_stage"] = self._calculate_growth_stage(companion["level"])
            
            # Unlock new abilities
            new_abilities = self._unlock_abilities(companion, companion_config)
            companion["abilities_unlocked"].extend(new_abilities)
            
            # Unlock new visual effects
            new_effects = self._unlock_visual_effects(companion, companion_config)
            companion["visual_effects"].extend(new_effects)
            
            # Save to database
            db.update_companion(user_id, companion)
            
            # Trigger level up effects
            self._trigger_visual_effect("companion_level_up", {
                "companion": companion,
                "new_level": companion["level"],
                "new_abilities": new_abilities,
                "new_effects": new_effects
            })
            
            return {
                "status": "success",
                "companion": companion,
                "new_level": companion["level"],
                "new_abilities": new_abilities,
                "new_effects": new_effects,
                "message": f"{companion['name']} reached level {companion['level']}!"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error leveling up companion: {str(e)}"}
    
    def _check_level_up(self, companion: Dict[str, Any]) -> Dict[str, Any]:
        """Check if companion can level up"""
        current_level = companion["level"]
        xp_needed = current_level * 100
        
        if companion["xp"] >= xp_needed:
            return self.companion_level_up(companion["user_id"])
        
        return {"leveled_up": False, "xp_needed": xp_needed - companion["xp"]}
    
    def _calculate_growth_stage(self, level: int) -> str:
        """Calculate companion growth stage based on level"""
        if level <= 5:
            return "baby"
        elif level <= 15:
            return "young"
        elif level <= 30:
            return "adult"
        elif level <= 45:
            return "mature"
        else:
            return "elder"
    
    def _unlock_abilities(self, companion: Dict[str, Any], config: Dict[str, Any]) -> List[str]:
        """Unlock new abilities based on level"""
        current_level = companion["level"]
        all_abilities = config["abilities"]
        unlocked_abilities = companion["abilities_unlocked"]
        
        new_abilities = []
        
        # Unlock abilities at specific levels
        ability_unlock_levels = {
            1: 0,   # First ability unlocked at creation
            5: 1,   # Second ability at level 5
            10: 2,  # Third ability at level 10
            20: 3,  # Fourth ability at level 20
            35: 4   # All abilities at level 35
        }
        
        for level, ability_index in ability_unlock_levels.items():
            if current_level >= level and ability_index < len(all_abilities):
                ability = all_abilities[ability_index]
                if ability not in unlocked_abilities:
                    new_abilities.append(ability)
        
        return new_abilities
    
    def _unlock_visual_effects(self, companion: Dict[str, Any], config: Dict[str, Any]) -> List[str]:
        """Unlock new visual effects based on level"""
        current_level = companion["level"]
        all_effects = config["visual_effects"]
        unlocked_effects = companion["visual_effects"]
        
        new_effects = []
        
        # Unlock effects at specific levels
        effect_unlock_levels = {
            1: 0,   # First effect unlocked at creation
            8: 1,   # Second effect at level 8
            15: 2,  # Third effect at level 15
        }
        
        for level, effect_index in effect_unlock_levels.items():
            if current_level >= level and effect_index < len(all_effects):
                effect = all_effects[effect_index]
                if effect not in unlocked_effects:
                    new_effects.append(effect)
        
        return new_effects
    
    def add_companion_xp(self, user_id: str, xp_amount: int, activity_type: str = "general") -> Dict[str, Any]:
        """Add XP to companion from various activities"""
        try:
            companion = self.get_companion(user_id)
            if not companion:
                return {"status": "error", "message": "No companion found"}
            
            # Calculate XP bonus based on companion happiness and energy
            happiness_bonus = companion["happiness"] / 100.0
            energy_bonus = companion["energy"] / 100.0
            total_bonus = (happiness_bonus + energy_bonus) / 2.0
            
            # Apply bonus
            final_xp = int(xp_amount * (1 + total_bonus))
            
            # Add XP
            companion["xp"] += final_xp
            companion["last_activity"] = datetime.now().isoformat()
            
            # Check for level up
            level_up_result = self._check_level_up(companion)
            
            # Save to database
            db.update_companion(user_id, companion)
            
            # Trigger XP gain effect
            self._trigger_visual_effect("companion_xp_gain", {
                "companion": companion,
                "xp_gained": final_xp,
                "activity_type": activity_type,
                "level_up": level_up_result.get("leveled_up", False)
            })
            
            return {
                "status": "success",
                "companion": companion,
                "xp_gained": final_xp,
                "bonus_applied": total_bonus,
                "level_up": level_up_result,
                "message": f"{companion['name']} gained {final_xp} XP!"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error adding companion XP: {str(e)}"}
    
    def use_companion_ability(self, user_id: str, ability_name: str) -> Dict[str, Any]:
        """Use a companion ability"""
        try:
            companion = self.get_companion(user_id)
            if not companion:
                return {"status": "error", "message": "No companion found"}
            
            if ability_name not in companion["abilities_unlocked"]:
                return {"status": "error", "message": f"Ability {ability_name} not unlocked"}
            
            # Check energy cost
            energy_cost = self._get_ability_energy_cost(ability_name)
            if companion["energy"] < energy_cost:
                return {"status": "error", "message": "Not enough energy to use ability"}
            
            # Use ability
            companion["energy"] -= energy_cost
            companion["last_activity"] = datetime.now().isoformat()
            
            # Calculate ability effects
            ability_effects = self._calculate_ability_effects(ability_name, companion)
            
            # Save to database
            db.update_companion(user_id, companion)
            
            # Trigger ability effect
            self._trigger_visual_effect("companion_ability_used", {
                "companion": companion,
                "ability": ability_name,
                "effects": ability_effects
            })
            
            return {
                "status": "success",
                "companion": companion,
                "ability_used": ability_name,
                "effects": ability_effects,
                "energy_cost": energy_cost,
                "message": f"{companion['name']} used {ability_name}!"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error using companion ability: {str(e)}"}
    
    def _get_ability_energy_cost(self, ability_name: str) -> int:
        """Get energy cost for using an ability"""
        energy_costs = {
            "hover": 5,
            "camera_feed": 10,
            "light_effects": 3,
            "falcon_vision": 15,
            "stealth": 8,
            "quick_movement": 12,
            "curiosity": 2,
            "playful": 4,
            "aerial_view": 20,
            "recording": 15,
            "scanning": 25,
            "mapping": 30,
            "desert_navigation": 10,
            "resource_finding": 15,
            "adaptation": 8
        }
        
        return energy_costs.get(ability_name, 10)
    
    def _calculate_ability_effects(self, ability_name: str, companion: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate effects of using an ability"""
        effects = {
            "xp_gain": 0,
            "happiness_gain": 0,
            "special_effect": None
        }
        
        # Base effects for different abilities
        if ability_name in ["hover", "falcon_vision", "aerial_view"]:
            effects["xp_gain"] = 5
            effects["happiness_gain"] = 2
        elif ability_name in ["camera_feed", "recording", "scanning"]:
            effects["xp_gain"] = 8
            effects["happiness_gain"] = 3
        elif ability_name in ["playful", "curiosity"]:
            effects["xp_gain"] = 3
            effects["happiness_gain"] = 5
        elif ability_name in ["stealth", "quick_movement"]:
            effects["xp_gain"] = 6
            effects["happiness_gain"] = 2
        elif ability_name in ["desert_navigation", "resource_finding"]:
            effects["xp_gain"] = 10
            effects["happiness_gain"] = 4
            effects["special_effect"] = "found_hidden_item"
        
        # Apply companion stats bonuses
        intelligence_bonus = companion["intelligence"] / 10.0
        effects["xp_gain"] = int(effects["xp_gain"] * (1 + intelligence_bonus))
        
        return effects
    
    def _trigger_visual_effect(self, effect_type: str, data: Dict[str, Any]):
        """Trigger visual effects for companion actions"""
        effect = {
            "type": effect_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        self.visual_effects_queue.append(effect)
        
        # In a real implementation, this would trigger actual visual effects
        print(f"[COMPANION VISUAL EFFECT] {effect_type}: {data}")
    
    def get_companion_stats(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive companion statistics"""
        try:
            companion = self.get_companion(user_id)
            if not companion:
                return {"status": "error", "message": "No companion found"}
            
            companion_type = companion["companion_type"]
            config = self.companion_types[companion_type]
            
            # Calculate progress to next level
            current_level = companion["level"]
            xp_needed = current_level * 100
            progress = (companion["xp"] / xp_needed) * 100 if xp_needed > 0 else 100
            
            # Calculate stat percentages
            happiness_percent = companion["happiness"]
            energy_percent = companion["energy"]
            hunger_percent = companion["hunger"]
            
            # Get available abilities
            all_abilities = config["abilities"]
            unlocked_abilities = companion["abilities_unlocked"]
            locked_abilities = [ability for ability in all_abilities if ability not in unlocked_abilities]
            
            return {
                "status": "success",
                "companion": companion,
                "stats": {
                    "level": companion["level"],
                    "xp": companion["xp"],
                    "xp_needed": xp_needed,
                    "progress_to_next_level": progress,
                    "power": companion["power"],
                    "speed": companion["speed"],
                    "intelligence": companion["intelligence"],
                    "happiness": happiness_percent,
                    "energy": energy_percent,
                    "hunger": hunger_percent,
                    "growth_stage": companion["growth_stage"]
                },
                "abilities": {
                    "unlocked": unlocked_abilities,
                    "locked": locked_abilities,
                    "total": len(all_abilities)
                },
                "visual_effects": companion["visual_effects"],
                "config": {
                    "name": config["name"],
                    "description": config["description"],
                    "max_level": config["max_level"]
                }
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error getting companion stats: {str(e)}"}

# Global companion system instance
companion_system = CompanionSystem() 