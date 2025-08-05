#!/usr/bin/env python3
"""
Empire Management System for Deerfields Mall Gamification System
Allows players to purchase facilities and develop their empire using in-game currency
"""

import random
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from database import db

class EmpireManagementSystem:
    """Empire management system with facility purchasing and development mechanics"""
    
    def __init__(self):
        self.facility_types = {
            "food_court": {
                "name": "Food Court",
                "description": "A bustling food court with various restaurants",
                "base_cost": 1000,
                "upgrade_cost_multiplier": 1.5,
                "max_level": 10,
                "income_per_hour": 50,
                "visitor_capacity": 100,
                "happiness_boost": 10,
                "unlock_requirements": {"level": 5, "coins": 500},
                "visual_effects": ["food_aroma", "busy_atmosphere", "chef_hats"],
                "special_events": ["food_festival", "chef_competition", "taste_testing"]
            },
            "entertainment_center": {
                "name": "Entertainment Center",
                "description": "Modern entertainment center with games and activities",
                "base_cost": 2000,
                "upgrade_cost_multiplier": 1.8,
                "max_level": 8,
                "income_per_hour": 80,
                "visitor_capacity": 80,
                "happiness_boost": 20,
                "unlock_requirements": {"level": 8, "coins": 1000},
                "visual_effects": ["neon_lights", "game_sounds", "excitement_aura"],
                "special_events": ["gaming_tournament", "arcade_night", "vr_experience"]
            },
            "luxury_boutique": {
                "name": "Luxury Boutique",
                "description": "High-end boutique with premium fashion items",
                "base_cost": 3000,
                "upgrade_cost_multiplier": 2.0,
                "max_level": 6,
                "income_per_hour": 120,
                "visitor_capacity": 50,
                "happiness_boost": 15,
                "unlock_requirements": {"level": 12, "coins": 2000},
                "visual_effects": ["elegant_lighting", "fashion_display", "luxury_aura"],
                "special_events": ["fashion_show", "designer_meet", "exclusive_sale"]
            },
            "tech_store": {
                "name": "Tech Store",
                "description": "Modern technology store with latest gadgets",
                "base_cost": 2500,
                "upgrade_cost_multiplier": 1.7,
                "max_level": 7,
                "income_per_hour": 100,
                "visitor_capacity": 60,
                "happiness_boost": 12,
                "unlock_requirements": {"level": 10, "coins": 1500},
                "visual_effects": ["tech_glow", "digital_display", "innovation_aura"],
                "special_events": ["tech_launch", "gadget_demo", "coding_workshop"]
            },
            "spa_wellness": {
                "name": "Spa & Wellness Center",
                "description": "Relaxing spa and wellness center",
                "base_cost": 4000,
                "upgrade_cost_multiplier": 2.2,
                "max_level": 5,
                "income_per_hour": 150,
                "visitor_capacity": 40,
                "happiness_boost": 25,
                "unlock_requirements": {"level": 15, "coins": 3000},
                "visual_effects": ["calm_aura", "steam_effects", "relaxation_music"],
                "special_events": ["wellness_retreat", "massage_day", "meditation_session"]
            },
            "cinema": {
                "name": "Cinema Complex",
                "description": "Multi-screen cinema with latest movies",
                "base_cost": 5000,
                "upgrade_cost_multiplier": 2.5,
                "max_level": 4,
                "income_per_hour": 200,
                "visitor_capacity": 200,
                "happiness_boost": 18,
                "unlock_requirements": {"level": 18, "coins": 4000},
                "visual_effects": ["movie_projector", "popcorn_aroma", "cinema_lights"],
                "special_events": ["movie_premiere", "film_festival", "classic_movie_night"]
            }
        }
        
        self.empire_bonuses = {
            "facility_count": {
                3: {"income_multiplier": 1.1, "happiness_boost": 5},
                5: {"income_multiplier": 1.2, "happiness_boost": 10},
                8: {"income_multiplier": 1.3, "happiness_boost": 15},
                12: {"income_multiplier": 1.5, "happiness_boost": 20},
                15: {"income_multiplier": 2.0, "happiness_boost": 30}
            },
            "total_level": {
                10: {"visitor_capacity": 50, "special_event_chance": 0.1},
                25: {"visitor_capacity": 100, "special_event_chance": 0.2},
                50: {"visitor_capacity": 200, "special_event_chance": 0.3},
                100: {"visitor_capacity": 500, "special_event_chance": 0.5}
            }
        }
        
        self.special_events = {
            "food_festival": {
                "name": "Food Festival",
                "description": "Celebrate culinary excellence",
                "duration_hours": 24,
                "income_multiplier": 2.0,
                "visitor_boost": 1.5,
                "cost": 500
            },
            "fashion_show": {
                "name": "Fashion Show",
                "description": "Showcase latest fashion trends",
                "duration_hours": 6,
                "income_multiplier": 3.0,
                "visitor_boost": 2.0,
                "cost": 1000
            },
            "tech_launch": {
                "name": "Tech Launch Event",
                "description": "Launch of latest technology",
                "duration_hours": 12,
                "income_multiplier": 2.5,
                "visitor_boost": 1.8,
                "cost": 800
            },
            "wellness_retreat": {
                "name": "Wellness Retreat",
                "description": "Relaxation and wellness event",
                "duration_hours": 48,
                "income_multiplier": 1.8,
                "visitor_boost": 1.3,
                "cost": 600
            }
        }
    
    def create_empire(self, user_id: str) -> Dict[str, Any]:
        """Create a new empire for the user"""
        try:
            empire = {
                "user_id": user_id,
                "empire_id": f"empire_{user_id}_{int(time.time())}",
                "name": f"{user_id}'s Empire",
                "level": 1,
                "xp": 0,
                "total_income": 0,
                "total_visitors": 0,
                "facilities": [],
                "active_events": [],
                "empire_bonuses": {},
                "created_at": datetime.now().isoformat(),
                "last_income_collection": datetime.now().isoformat()
            }
            
            # Save to database
            if DATABASE_AVAILABLE:
                db.save_empire(empire)
            else:
                # Fallback to memory storage
                if not hasattr(self, 'empire_storage'):
                    self.empire_storage = {}
                self.empire_storage[empire["empire_id"]] = empire
            
            print(f"🏛️ Created empire for user {user_id}")
            return {"status": "success", "empire": empire}
            
        except Exception as e:
            return {"status": "error", "message": f"Error creating empire: {str(e)}"}
    
    def get_empire(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's empire"""
        try:
            if DATABASE_AVAILABLE:
                return db.get_empire(user_id)
            else:
                # Fallback to memory storage
                if hasattr(self, 'empire_storage'):
                    for empire_id, empire in self.empire_storage.items():
                        if empire["user_id"] == user_id:
                            return empire
                return None
        except Exception as e:
            print(f"Error getting empire: {e}")
            return None
    
    def purchase_facility(self, user_id: str, facility_type: str, user_level: int = 1, user_coins: int = 0) -> Dict[str, Any]:
        """Purchase a new facility for the empire"""
        try:
            empire = self.get_empire(user_id)
            if not empire:
                # Create empire if it doesn't exist
                empire_result = self.create_empire(user_id)
                if empire_result["status"] != "success":
                    return empire_result
                empire = empire_result["empire"]
            
            if facility_type not in self.facility_types:
                return {"status": "error", "message": "Invalid facility type"}
            
            facility_template = self.facility_types[facility_type]
            
            # Check unlock requirements
            requirements = facility_template["unlock_requirements"]
            if user_level < requirements["level"]:
                return {"status": "error", "message": f"Level {requirements['level']} required to unlock {facility_template['name']}"}
            
            if user_coins < requirements["coins"]:
                return {"status": "error", "message": f"{requirements['coins']} coins required to unlock {facility_template['name']}"}
            
            # Check if user has enough coins for the facility
            facility_cost = facility_template["base_cost"]
            if user_coins < facility_cost:
                return {"status": "error", "message": f"Insufficient coins. Need {facility_cost} coins for {facility_template['name']}"}
            
            # Create facility
            facility = {
                "facility_id": f"facility_{user_id}_{facility_type}_{int(time.time())}",
                "type": facility_type,
                "name": facility_template["name"],
                "description": facility_template["description"],
                "level": 1,
                "income_per_hour": facility_template["income_per_hour"],
                "visitor_capacity": facility_template["visitor_capacity"],
                "happiness_boost": facility_template["happiness_boost"],
                "visual_effects": facility_template["visual_effects"][:1],  # Start with 1 effect
                "special_events": facility_template["special_events"],
                "purchased_at": datetime.now().isoformat(),
                "last_upgrade": datetime.now().isoformat()
            }
            
            # Add facility to empire
            empire["facilities"].append(facility)
            
            # Update empire bonuses
            self._update_empire_bonuses(empire)
            
            # Save to database
            if DATABASE_AVAILABLE:
                db.update_empire(empire["empire_id"], empire)
            else:
                if hasattr(self, 'empire_storage'):
                    self.empire_storage[empire["empire_id"]] = empire
            
            print(f"🏢 Purchased {facility['name']} for {user_id} (-{facility_cost} coins)")
            return {
                "status": "success",
                "facility": facility,
                "empire": empire,
                "cost": facility_cost,
                "remaining_coins": user_coins - facility_cost,
                "message": f"Successfully purchased {facility['name']}!"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error purchasing facility: {str(e)}"}
    
    def upgrade_facility(self, user_id: str, facility_id: str, user_coins: int = 0) -> Dict[str, Any]:
        """Upgrade an existing facility"""
        try:
            empire = self.get_empire(user_id)
            if not empire:
                return {"status": "error", "message": "No empire found"}
            
            # Find the facility
            facility = None
            facility_index = None
            for i, f in enumerate(empire["facilities"]):
                if f["facility_id"] == facility_id:
                    facility = f
                    facility_index = i
                    break
            
            if not facility:
                return {"status": "error", "message": "Facility not found"}
            
            facility_template = self.facility_types[facility["type"]]
            
            # Check if facility can be upgraded
            if facility["level"] >= facility_template["max_level"]:
                return {"status": "error", "message": "Facility is already at maximum level"}
            
            # Calculate upgrade cost
            upgrade_cost = int(facility_template["base_cost"] * (facility_template["upgrade_cost_multiplier"] ** (facility["level"] - 1)))
            
            if user_coins < upgrade_cost:
                return {"status": "error", "message": f"Insufficient coins. Need {upgrade_cost} coins for upgrade"}
            
            # Apply upgrade
            old_level = facility["level"]
            facility["level"] += 1
            facility["income_per_hour"] = int(facility["income_per_hour"] * 1.3)  # 30% increase
            facility["visitor_capacity"] = int(facility["visitor_capacity"] * 1.2)  # 20% increase
            facility["happiness_boost"] = int(facility["happiness_boost"] * 1.1)  # 10% increase
            facility["last_upgrade"] = datetime.now().isoformat()
            
            # Unlock new visual effects
            if len(facility["visual_effects"]) < len(facility_template["visual_effects"]):
                new_effect = facility_template["visual_effects"][len(facility["visual_effects"])]
                facility["visual_effects"].append(new_effect)
            
            # Update empire
            empire["facilities"][facility_index] = facility
            self._update_empire_bonuses(empire)
            
            # Save to database
            if DATABASE_AVAILABLE:
                db.update_empire(empire["empire_id"], empire)
            else:
                if hasattr(self, 'empire_storage'):
                    self.empire_storage[empire["empire_id"]] = empire
            
            print(f"⬆️ Upgraded {facility['name']} to level {facility['level']} (-{upgrade_cost} coins)")
            return {
                "status": "success",
                "facility": facility,
                "empire": empire,
                "cost": upgrade_cost,
                "remaining_coins": user_coins - upgrade_cost,
                "old_level": old_level,
                "new_level": facility["level"],
                "message": f"Successfully upgraded {facility['name']} to level {facility['level']}!"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error upgrading facility: {str(e)}"}
    
    def collect_income(self, user_id: str) -> Dict[str, Any]:
        """Collect income from all facilities"""
        try:
            empire = self.get_empire(user_id)
            if not empire:
                return {"status": "error", "message": "No empire found"}
            
            if not empire["facilities"]:
                return {"status": "error", "message": "No facilities to collect income from"}
            
            # Calculate time since last collection
            last_collection = datetime.fromisoformat(empire["last_income_collection"])
            now = datetime.now()
            hours_passed = (now - last_collection).total_seconds() / 3600
            
            if hours_passed < 1:
                return {"status": "error", "message": "Income can only be collected once per hour"}
            
            # Calculate total income
            total_income = 0
            facility_incomes = {}
            
            for facility in empire["facilities"]:
                # Apply empire bonuses
                income_multiplier = empire["empire_bonuses"].get("income_multiplier", 1.0)
                facility_income = int(facility["income_per_hour"] * hours_passed * income_multiplier)
                facility_incomes[facility["facility_id"]] = facility_income
                total_income += facility_income
            
            # Update empire
            empire["total_income"] += total_income
            empire["last_income_collection"] = now.isoformat()
            
            # Save to database
            if DATABASE_AVAILABLE:
                db.update_empire(empire["empire_id"], empire)
            else:
                if hasattr(self, 'empire_storage'):
                    self.empire_storage[empire["empire_id"]] = empire
            
            print(f"💰 Collected {total_income} coins from empire facilities")
            return {
                "status": "success",
                "total_income": total_income,
                "facility_incomes": facility_incomes,
                "hours_passed": hours_passed,
                "empire": empire,
                "message": f"Collected {total_income} coins from your empire!"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error collecting income: {str(e)}"}
    
    def start_special_event(self, user_id: str, facility_id: str, event_type: str, user_coins: int = 0) -> Dict[str, Any]:
        """Start a special event at a facility"""
        try:
            empire = self.get_empire(user_id)
            if not empire:
                return {"status": "error", "message": "No empire found"}
            
            # Find the facility
            facility = None
            for f in empire["facilities"]:
                if f["facility_id"] == facility_id:
                    facility = f
                    break
            
            if not facility:
                return {"status": "error", "message": "Facility not found"}
            
            if event_type not in self.special_events:
                return {"status": "error", "message": "Invalid event type"}
            
            event_template = self.special_events[event_type]
            
            if user_coins < event_template["cost"]:
                return {"status": "error", "message": f"Insufficient coins. Need {event_template['cost']} coins for this event"}
            
            # Create event
            event = {
                "event_id": f"event_{user_id}_{event_type}_{int(time.time())}",
                "type": event_type,
                "name": event_template["name"],
                "description": event_template["description"],
                "facility_id": facility_id,
                "start_time": datetime.now().isoformat(),
                "end_time": (datetime.now() + timedelta(hours=event_template["duration_hours"])).isoformat(),
                "duration_hours": event_template["duration_hours"],
                "income_multiplier": event_template["income_multiplier"],
                "visitor_boost": event_template["visitor_boost"],
                "cost": event_template["cost"]
            }
            
            # Add event to empire
            empire["active_events"].append(event)
            
            # Save to database
            if DATABASE_AVAILABLE:
                db.update_empire(empire["empire_id"], empire)
            else:
                if hasattr(self, 'empire_storage'):
                    self.empire_storage[empire["empire_id"]] = empire
            
            print(f"🎉 Started {event['name']} at {facility['name']} (-{event_template['cost']} coins)")
            return {
                "status": "success",
                "event": event,
                "empire": empire,
                "cost": event_template["cost"],
                "remaining_coins": user_coins - event_template["cost"],
                "message": f"Started {event['name']} at {facility['name']}!"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error starting event: {str(e)}"}
    
    def get_empire_status(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive empire status"""
        try:
            empire = self.get_empire(user_id)
            if not empire:
                return {"status": "error", "message": "No empire found"}
            
            # Calculate current stats
            total_income_per_hour = sum(f["income_per_hour"] for f in empire["facilities"])
            total_visitor_capacity = sum(f["visitor_capacity"] for f in empire["facilities"])
            total_happiness_boost = sum(f["happiness_boost"] for f in empire["facilities"])
            
            # Check for available upgrades
            available_upgrades = []
            for facility in empire["facilities"]:
                facility_template = self.facility_types[facility["type"]]
                if facility["level"] < facility_template["max_level"]:
                    upgrade_cost = int(facility_template["base_cost"] * (facility_template["upgrade_cost_multiplier"] ** (facility["level"] - 1)))
                    available_upgrades.append({
                        "facility_id": facility["facility_id"],
                        "facility_name": facility["name"],
                        "current_level": facility["level"],
                        "upgrade_cost": upgrade_cost
                    })
            
            # Check for available purchases
            available_purchases = []
            for facility_type, template in self.facility_types.items():
                # Check if user already has this facility type
                has_facility = any(f["type"] == facility_type for f in empire["facilities"])
                if not has_facility:
                    available_purchases.append({
                        "type": facility_type,
                        "name": template["name"],
                        "description": template["description"],
                        "cost": template["base_cost"],
                        "requirements": template["unlock_requirements"]
                    })
            
            return {
                "status": "success",
                "empire": empire,
                "stats": {
                    "total_income_per_hour": total_income_per_hour,
                    "total_visitor_capacity": total_visitor_capacity,
                    "total_happiness_boost": total_happiness_boost,
                    "facility_count": len(empire["facilities"]),
                    "active_events": len(empire["active_events"])
                },
                "available_upgrades": available_upgrades,
                "available_purchases": available_purchases
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error getting empire status: {str(e)}"}
    
    def _update_empire_bonuses(self, empire: Dict[str, Any]):
        """Update empire bonuses based on facilities and levels"""
        try:
            facility_count = len(empire["facilities"])
            total_level = sum(f["level"] for f in empire["facilities"])
            
            # Apply facility count bonuses
            empire["empire_bonuses"] = {}
            for count, bonus in self.empire_bonuses["facility_count"].items():
                if facility_count >= count:
                    empire["empire_bonuses"].update(bonus)
            
            # Apply total level bonuses
            for level, bonus in self.empire_bonuses["total_level"].items():
                if total_level >= level:
                    empire["empire_bonuses"].update(bonus)
            
        except Exception as e:
            print(f"Error updating empire bonuses: {e}")
    
    def get_available_facilities(self) -> Dict[str, Any]:
        """Get list of available facility types"""
        return {"status": "success", "facilities": self.facility_types}
    
    def get_available_events(self) -> Dict[str, Any]:
        """Get list of available special events"""
        return {"status": "success", "events": self.special_events}

# Initialize database availability
try:
    from database import db
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    print("[EMPIRE MANAGEMENT] Database module not available, using in-memory storage")

# Create global instance
empire_management_system = EmpireManagementSystem() 