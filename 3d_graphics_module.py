# 3D Graphics Module for Deerfields Mall Gamification System
# Provides immersive visual experiences with realistic mall environments

# Fixed import structure for proper dependency management
import sys
import os
import logging
import logger as logger_config

logger = logging.getLogger(__name__)
sys.path.append(os.path.dirname(__file__))

try:
    from database import db
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    logger.warning("[WARNING] Database module not available")

import json
import random
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import math

# Proper error handling for missing dependencies
class SafeSystemInitializer:
    def __init__(self):
        self.modules = {}
        self._load_modules()
    
    def _load_modules(self):
        """Safely load all modules with fallbacks"""
        modules_to_load = [
            ('database', 'db'),
            ('ai_mission_generator', 'ai_mission_generator'),
            ('wifi_verification', 'wifi_verification'),
            ('companion_system', 'companion_system')
        ]
        
        for module_name, object_name in modules_to_load:
            try:
                module = __import__(module_name)
                self.modules[module_name] = getattr(module, object_name)
                logger.info(f"[✅] {module_name} loaded successfully")
            except ImportError as e:
                self.modules[module_name] = None
                logger.warning(f"[⚠️] {module_name} not available: {e}")
    
    def get_module(self, module_name):
        """Safely get module with None fallback"""
        return self.modules.get(module_name)

class GraphicsEngine:
    """3D Graphics Engine for Mall Gamification System"""
    
    def __init__(self):
        self.graphics_mode = "realistic"
        self.quality_level = "ultra"
        self.lighting_preset = "indoor_daylight"
        self.shadows_enabled = True
        self.smooth_physics = True
        self.loaded_models = {}
        self.active_effects = []
        self.player_position = {"x": 0, "y": 0, "z": 0}
        self.camera_position = {"x": 0, "y": 5, "z": 10}
        self.player_character = None
        self.player_animations = {}
        self.movement_zones = {}
        self.camera_mode = "third_person"
        self.camera_smooth_tracking = True
        self.interactive_zones = {}
        self.minigames = {}
        self.wifi_restrictions = {}
        self.reward_effects = {}
        self.ui_system = {}
        self.language_support = {}
        self.main_menu = {}
        self.top_bar = {}
        self.incentive_system = {}
        self.sound_system = {}
        self.quest_system = {}
        self.brand_integration = {}
        self.invite_system = {}
        self.user_management = {}
        self.environment_3d = {}
        self.avatar_system = {}
        self.shop_system = {}
        self.mission_system = {}
        self.ai_npc_system = {}
        self.path_system = {}
        self.kid_zone_system = {}
        self.location_tracking = {}
        
    def enable_3d_graphics(self, mode: str = "realistic"):
        """Enable 3D graphics with specified mode"""
        self.graphics_mode = mode
        logger.info(f"[3D GRAPHICS] Enabled {mode} mode")
        return {"status": "success", "mode": mode}
    
    def set_graphics_quality(self, level: str = "ultra"):
        """Set graphics quality level"""
        self.quality_level = level
        logger.info(f"[3D GRAPHICS] Quality set to {level}")
        return {"status": "success", "quality": level}
    
    def load_3d_model(self, model_name: str, resolution: str = "high", lighting: str = "realistic"):
        """Load 3D model with specified settings"""
        model_data = {
            "name": model_name,
            "resolution": resolution,
            "lighting": lighting,
            "loaded_at": datetime.now(),
            "vertices": self._generate_mall_vertices(),
            "textures": self._generate_mall_textures(),
            "animations": self._generate_mall_animations()
        }
        
        self.loaded_models[model_name] = model_data
        logger.info(f"[3D GRAPHICS] Loaded {model_name} with {resolution} resolution")
        return {"status": "success", "model": model_name}
    
    def set_lighting(self, preset: str = "indoor_daylight", shadows: bool = True):
        """Set lighting configuration"""
        self.lighting_preset = preset
        self.shadows_enabled = shadows
        
        lighting_config = {
            "indoor_daylight": {
                "ambient": {"r": 0.3, "g": 0.3, "b": 0.3},
                "directional": {"r": 0.8, "g": 0.8, "b": 0.7, "intensity": 1.0},
                "shadows": shadows
            },
            "evening": {
                "ambient": {"r": 0.2, "g": 0.2, "b": 0.3},
                "directional": {"r": 0.6, "g": 0.5, "b": 0.8, "intensity": 0.7},
                "shadows": shadows
            },
            "night": {
                "ambient": {"r": 0.1, "g": 0.1, "b": 0.2},
                "directional": {"r": 0.3, "g": 0.3, "b": 0.5, "intensity": 0.4},
                "shadows": shadows
            }
        }
        
        logger.info(f"[3D GRAPHICS] Lighting set to {preset} with shadows: {shadows}")
        return {"status": "success", "lighting": preset, "config": lighting_config.get(preset, {})}
    
    def set_player_motion(self, smooth_physics: bool = True):
        """Configure player motion physics"""
        self.smooth_physics = smooth_physics
        logger.info(f"[3D GRAPHICS] Smooth physics: {smooth_physics}")
        return {"status": "success", "smooth_physics": smooth_physics}
    
    def create_player_character(self, name: str = "Visitor", avatar_style: str = "modern"):
        """Create player character with specified style"""
        self.player_character = {
            "name": name,
            "avatar_style": avatar_style,
            "position": {"x": 0, "y": 0, "z": 0},
            "rotation": {"x": 0, "y": 0, "z": 0},
            "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
            "model": f"avatar_{avatar_style}.glb",
            "textures": self._generate_avatar_textures(avatar_style),
            "animations": {},
            "created_at": datetime.now()
        }
        
        logger.info(f"[3D GRAPHICS] Player character created: {name} ({avatar_style} style)")
        return {"status": "success", "character": self.player_character}
    
    def add_player_animations(self, animation_list: List[str]):
        """Add animations to player character"""
        if not self.player_character:
            return {"status": "error", "message": "Player character not created"}
        
        available_animations = {
            "walk": {
                "file": "walk_animation.glb",
                "duration": 1.0,
                "loop": True,
                "speed": 1.0
            },
            "run": {
                "file": "run_animation.glb",
                "duration": 0.8,
                "loop": True,
                "speed": 1.5
            },
            "idle": {
                "file": "idle_animation.glb",
                "duration": 2.0,
                "loop": True,
                "speed": 1.0
            },
            "jump": {
                "file": "jump_animation.glb",
                "duration": 1.2,
                "loop": False,
                "speed": 1.0
            },
            "wave": {
                "file": "wave_animation.glb",
                "duration": 1.5,
                "loop": False,
                "speed": 1.0
            },
            "dance": {
                "file": "dance_animation.glb",
                "duration": 3.0,
                "loop": True,
                "speed": 1.0
            }
        }
        
        for anim_name in animation_list:
            if anim_name in available_animations:
                self.player_character["animations"][anim_name] = available_animations[anim_name]
                logger.info(f"[3D GRAPHICS] Added animation: {anim_name}")
        
        return {"status": "success", "animations_added": len(animation_list)}
    
    def set_movement_zone(self, area: str = "mall_interior", movement_type: str = "freewalk"):
        """Set movement zone and type for player"""
        movement_zones = {
            "mall_interior": {
                "bounds": {
                    "min": {"x": -100, "y": 0, "z": -100},
                    "max": {"x": 100, "y": 20, "z": 100}
                },
                "restricted_areas": [
                    {"x": -50, "y": 0, "z": -50, "radius": 10},  # Fountain area
                    {"x": 0, "y": 0, "z": 10, "radius": 5}       # Escalator area
                ],
                "movement_type": movement_type,
                "collision_detection": True
            },
            "store_interior": {
                "bounds": {
                    "min": {"x": -30, "y": 0, "z": -20},
                    "max": {"x": 30, "y": 8, "z": 20}
                },
                "restricted_areas": [],
                "movement_type": "constrained",
                "collision_detection": True
            },
            "outdoor_area": {
                "bounds": {
                    "min": {"x": -200, "y": 0, "z": -200},
                    "max": {"x": 200, "y": 0, "z": 200}
                },
                "restricted_areas": [],
                "movement_type": "freewalk",
                "collision_detection": False
            }
        }
        
        if area in movement_zones:
            self.movement_zones[area] = movement_zones[area]
            logger.info(f"[3D GRAPHICS] Movement zone set: {area} ({movement_type})")
            return {"status": "success", "zone": area, "movement_type": movement_type}
        else:
            return {"status": "error", "message": f"Unknown area: {area}"}
    
    def enable_third_person_camera(self, smooth_tracking: bool = True):
        """Enable third-person camera with smooth tracking"""
        self.camera_mode = "third_person"
        self.camera_smooth_tracking = smooth_tracking
        
        camera_config = {
            "mode": "third_person",
            "position": {"x": 0, "y": 5, "z": 10},
            "target": {"x": 0, "y": 1, "z": 0},
            "smooth_tracking": smooth_tracking,
            "tracking_speed": 0.1 if smooth_tracking else 1.0,
            "field_of_view": 60,
            "near_clip": 0.1,
            "far_clip": 1000,
            "collision_detection": True
        }
        
        logger.info(f"[3D GRAPHICS] Third-person camera enabled (smooth tracking: {smooth_tracking})")
        return {"status": "success", "camera_config": camera_config}
    
    def move_player(self, direction: str, speed: float = 1.0):
        """Move player character in specified direction"""
        if not self.player_character:
            return {"status": "error", "message": "Player character not created"}
        
        # Calculate new position based on direction
        movement_vectors = {
            "forward": {"x": 0, "y": 0, "z": -1},
            "backward": {"x": 0, "y": 0, "z": 1},
            "left": {"x": -1, "y": 0, "z": 0},
            "right": {"x": 1, "y": 0, "z": 0},
            "up": {"x": 0, "y": 1, "z": 0},
            "down": {"x": 0, "y": -1, "z": 0}
        }
        
        if direction in movement_vectors:
            vector = movement_vectors[direction]
            new_position = {
                "x": self.player_character["position"]["x"] + vector["x"] * speed,
                "y": self.player_character["position"]["y"] + vector["y"] * speed,
                "z": self.player_character["position"]["z"] + vector["z"] * speed
            }
            
            # Check movement zone boundaries
            if self._is_position_valid(new_position):
                self.player_character["position"] = new_position
                self.player_position = new_position
                
                # Update camera position if in third-person mode
                if self.camera_mode == "third_person":
                    self._update_camera_position()
                
                logger.info(f"[3D GRAPHICS] Player moved {direction} to {new_position}")
                return {"status": "success", "new_position": new_position}
            else:
                return {"status": "error", "message": "Movement blocked by zone boundaries"}
        
        return {"status": "error", "message": f"Unknown direction: {direction}"}
    
    def play_animation(self, animation_name: str):
        """Play specific animation for player character"""
        if not self.player_character:
            return {"status": "error", "message": "Player character not created"}
        
        if animation_name in self.player_character["animations"]:
            animation = self.player_character["animations"][animation_name]
            logger.info(f"[3D GRAPHICS] Playing animation: {animation_name} ({animation['duration']}s)")
            return {"status": "success", "animation": animation_name, "duration": animation["duration"]}
        else:
            return {"status": "error", "message": f"Animation not found: {animation_name}"}
    
    def _is_position_valid(self, position: Dict) -> bool:
        """Check if position is within movement zone boundaries"""
        for zone_name, zone in self.movement_zones.items():
            bounds = zone["bounds"]
            if (bounds["min"]["x"] <= position["x"] <= bounds["max"]["x"] and
                bounds["min"]["y"] <= position["y"] <= bounds["max"]["y"] and
                bounds["min"]["z"] <= position["z"] <= bounds["max"]["z"]):
                return True
        return False
    
    def _update_camera_position(self):
        """Update camera position for third-person view"""
        if self.camera_mode == "third_person" and self.player_character:
            player_pos = self.player_character["position"]
            
            # Calculate camera offset
            camera_offset = {"x": 0, "y": 5, "z": 10}
            
            if self.camera_smooth_tracking:
                # Smooth camera tracking
                self.camera_position = {
                    "x": player_pos["x"] + camera_offset["x"],
                    "y": player_pos["y"] + camera_offset["y"],
                    "z": player_pos["z"] + camera_offset["z"]
                }
            else:
                # Instant camera tracking
                self.camera_position = {
                    "x": player_pos["x"] + camera_offset["x"],
                    "y": player_pos["y"] + camera_offset["y"],
                    "z": player_pos["z"] + camera_offset["z"]
                }
    
    def _generate_avatar_textures(self, style: str) -> Dict:
        """Generate avatar textures based on style"""
        texture_templates = {
            "modern": {
                "body": "modern_body.png",
                "face": "modern_face.png",
                "clothes": "modern_clothes.png",
                "accessories": "modern_accessories.png"
            },
            "casual": {
                "body": "casual_body.png",
                "face": "casual_face.png",
                "clothes": "casual_clothes.png",
                "accessories": "casual_accessories.png"
            },
            "formal": {
                "body": "formal_body.png",
                "face": "formal_face.png",
                "clothes": "formal_clothes.png",
                "accessories": "formal_accessories.png"
            },
            "sporty": {
                "body": "sporty_body.png",
                "face": "sporty_face.png",
                "clothes": "sporty_clothes.png",
                "accessories": "sporty_accessories.png"
            }
        }
        
        return texture_templates.get(style, texture_templates["modern"])
    
    def create_interactive_zone(self, name: str, location: str, reward_type: str = "coin"):
        """Create interactive mission zone with rewards"""
        zone_config = {
            "name": name,
            "location": location,
            "reward_type": reward_type,
            "position": self._get_zone_position(location),
            "radius": 5.0,
            "active": True,
            "cooldown": 300,  # 5 minutes
            "last_triggered": None,
            "visual_effects": {
                "glow": True,
                "particles": True,
                "color": self._get_reward_color(reward_type)
            },
            "created_at": datetime.now()
        }
        
        self.interactive_zones[name] = zone_config
        logger.info(f"[3D GRAPHICS] Interactive zone created: {name} at {location}")
        return {"status": "success", "zone": zone_config}
    
    def trigger_reward_effect(self, type: str = "coin_sparkle", amount: int = 10):
        """Trigger reward effects with visual feedback"""
        effect_config = {
            "type": type,
            "amount": amount,
            "duration": 3.0,
            "particles": self._generate_reward_particles(type, amount),
            "sound": f"{type}_sound.wav",
            "visual": self._get_effect_visual(type),
            "triggered_at": datetime.now()
        }
        
        self.reward_effects[f"{type}_{amount}"] = effect_config
        
        # Trigger visual effect
        if type == "coin_sparkle":
            self._trigger_coin_sparkle_effect(amount)
        elif type == "xp_burst":
            self._trigger_xp_burst_effect(amount)
        elif type == "vip_flash":
            self._trigger_vip_flash_effect(amount)
        
        logger.info(f"[3D GRAPHICS] Reward effect triggered: {type} ({amount})")
        return {"status": "success", "effect": effect_config}
    
    def load_minigame(self, name: str, location: str, cooldown: str = "2h"):
        """Load minigame at specific location"""
        cooldown_seconds = self._parse_cooldown(cooldown)
        
        minigame_config = {
            "name": name,
            "location": location,
            "position": self._get_zone_position(location),
            "cooldown": cooldown_seconds,
            "last_played": None,
            "active": True,
            "type": self._get_minigame_type(name),
            "rewards": self._get_minigame_rewards(name),
            "visual_effects": {
                "glow": True,
                "animation": True,
                "color": "#FFD700"  # Gold color
            },
            "created_at": datetime.now()
        }
        
        self.minigames[name] = minigame_config
        logger.info(f"[3D GRAPHICS] Minigame loaded: {name} at {location} (cooldown: {cooldown})")
        return {"status": "success", "minigame": minigame_config}
    
    def lock_game_to_wifi(self, ssid: str = "Deerfields_Free_WiFi"):
        """Lock game to specific WiFi network"""
        wifi_config = {
            "ssid": ssid,
            "locked": True,
            "check_interval": 30,  # Check every 30 seconds
            "last_check": datetime.now(),
            "connection_status": "unknown",
            "warnings": {
                "en": "Please connect to mall WiFi to play.",
                "ar": "يرجى الاتصال بشبكة واي فاي المول للعب."
            }
        }
        
        self.wifi_restrictions["main"] = wifi_config
        logger.info(f"[3D GRAPHICS] Game locked to WiFi: {ssid}")
        return {"status": "success", "wifi_config": wifi_config}
    
    def set_outside_warning(self, message_en: str, message_ar: str):
        """Set warning messages for outside connections"""
        warning_config = {
            "en": message_en,
            "ar": message_ar,
            "active": True,
            "display_duration": 5.0,
            "style": {
                "background": "#FF4444",
                "text_color": "#FFFFFF",
                "border": "#CC0000"
            }
        }
        
        self.wifi_restrictions["warning"] = warning_config
        logger.warning(f"[3D GRAPHICS] Outside warning set: {message_en}")
        return {"status": "success", "warning": warning_config}
    
    def check_wifi_connection(self) -> bool:
        """Check if connected to mall WiFi"""
        if "main" not in self.wifi_restrictions:
            return True  # No restriction if not set
        
        wifi_config = self.wifi_restrictions["main"]
        # Simulate WiFi check (in real implementation, this would check actual network)
        current_ssid = self._simulate_wifi_check()
        
        is_connected = current_ssid == wifi_config["ssid"]
        wifi_config["connection_status"] = "connected" if is_connected else "disconnected"
        wifi_config["last_check"] = datetime.now()
        
        return is_connected
    
    def trigger_zone_interaction(self, zone_name: str, player_position: Dict) -> Dict:
        """Trigger interaction with mission zone"""
        if zone_name not in self.interactive_zones:
            return {"status": "error", "message": "Zone not found"}
        
        zone = self.interactive_zones[zone_name]
        
        # Check if player is in zone
        if not self._is_player_in_zone(player_position, zone):
            return {"status": "error", "message": "Player not in zone"}
        
        # Check cooldown
        if self._is_zone_on_cooldown(zone):
            remaining_time = self._get_remaining_cooldown(zone)
            return {"status": "error", "message": f"Zone on cooldown: {remaining_time}s remaining"}
        
        # Trigger reward
        reward_result = self.trigger_reward_effect(zone["reward_type"], 10)
        
        # Update zone cooldown
        zone["last_triggered"] = datetime.now()
        
        logger.info(f"[3D GRAPHICS] Zone interaction triggered: {zone_name}")
        return {"status": "success", "reward": reward_result, "zone": zone_name}
    
    def start_minigame(self, minigame_name: str, player_position: Dict) -> Dict:
        """Start minigame if player is in location"""
        if minigame_name not in self.minigames:
            return {"status": "error", "message": "Minigame not found"}
        
        minigame = self.minigames[minigame_name]
        
        # Check if player is at minigame location
        if not self._is_player_in_zone(player_position, minigame):
            return {"status": "error", "message": "Player not at minigame location"}
        
        # Check cooldown
        if self._is_zone_on_cooldown(minigame):
            remaining_time = self._get_remaining_cooldown(minigame)
            return {"status": "error", "message": f"Minigame on cooldown: {remaining_time}s remaining"}
        
        # Start minigame
        minigame["last_played"] = datetime.now()
        
        logger.info(f"[3D GRAPHICS] Minigame started: {minigame_name}")
        return {"status": "success", "minigame": minigame_name, "rewards": minigame["rewards"]}
    
    def _get_zone_position(self, location: str) -> Dict:
        """Get position for specific location"""
        location_positions = {
            "food_court": {"x": 0, "y": 0, "z": 50},
            "entrance_zone": {"x": 0, "y": 0, "z": -80},
            "fashion_area": {"x": -40, "y": 0, "z": 0},
            "electronics_area": {"x": 40, "y": 0, "z": 0},
            "cafe_zone": {"x": 20, "y": 0, "z": 30},
            "fountain_area": {"x": -50, "y": 0, "z": -50},
            "escalator_zone": {"x": 0, "y": 0, "z": 10}
        }
        
        return location_positions.get(location, {"x": 0, "y": 0, "z": 0})
    
    def _get_reward_color(self, reward_type: str) -> str:
        """Get color for reward type"""
        colors = {
            "coin": "#FFD700",      # Gold
            "xp": "#00FF00",        # Green
            "vip": "#FF00FF",       # Magenta
            "special": "#00FFFF"    # Cyan
        }
        return colors.get(reward_type, "#FFFFFF")
    
    def _generate_reward_particles(self, type: str, amount: int) -> List[Dict]:
        """Generate particles for reward effect"""
        particles = []
        for i in range(amount):
            particle = {
                "id": f"{type}_{i}",
                "position": {"x": random.uniform(-2, 2), "y": random.uniform(0, 3), "z": random.uniform(-2, 2)},
                "velocity": {"x": random.uniform(-1, 1), "y": random.uniform(1, 3), "z": random.uniform(-1, 1)},
                "color": self._get_reward_color(type),
                "size": random.uniform(0.1, 0.3),
                "lifetime": random.uniform(2.0, 4.0)
            }
            particles.append(particle)
        return particles
    
    def _get_effect_visual(self, type: str) -> Dict:
        """Get visual configuration for effect type"""
        visuals = {
            "coin_sparkle": {
                "type": "particle_burst",
                "color": "#FFD700",
                "intensity": "high",
                "duration": 3.0
            },
            "xp_burst": {
                "type": "energy_wave",
                "color": "#00FF00",
                "intensity": "medium",
                "duration": 2.5
            },
            "vip_flash": {
                "type": "lightning_flash",
                "color": "#FF00FF",
                "intensity": "very_high",
                "duration": 1.5
            }
        }
        return visuals.get(type, {"type": "basic", "color": "#FFFFFF", "intensity": "low", "duration": 1.0})
    
    def _parse_cooldown(self, cooldown: str) -> int:
        """Parse cooldown string to seconds"""
        if cooldown.endswith("h"):
            return int(cooldown[:-1]) * 3600
        elif cooldown.endswith("m"):
            return int(cooldown[:-1]) * 60
        elif cooldown.endswith("s"):
            return int(cooldown[:-1])
        else:
            return int(cooldown)
    
    def _get_minigame_type(self, name: str) -> str:
        """Get minigame type based on name"""
        minigame_types = {
            "SpinWheel": "luck_based",
            "MemoryGame": "skill_based",
            "TreasureHunt": "exploration",
            "QuizGame": "knowledge_based"
        }
        return minigame_types.get(name, "unknown")
    
    def _get_minigame_rewards(self, name: str) -> Dict:
        """Get rewards for minigame"""
        reward_templates = {
            "SpinWheel": {
                "coins": {"min": 5, "max": 50},
                "xp": {"min": 10, "max": 100},
                "special_items": ["VIP_Pass", "Rare_Item"]
            },
            "MemoryGame": {
                "coins": {"min": 10, "max": 30},
                "xp": {"min": 20, "max": 80}
            },
            "TreasureHunt": {
                "coins": {"min": 15, "max": 40},
                "xp": {"min": 25, "max": 90}
            },
            "QuizGame": {
                "coins": {"min": 8, "max": 25},
                "xp": {"min": 15, "max": 60}
            }
        }
        return reward_templates.get(name, {"coins": {"min": 5, "max": 20}, "xp": {"min": 10, "max": 50}})
    
    def _simulate_wifi_check(self) -> str:
        """Simulate WiFi network check"""
        # In real implementation, this would check actual network
        networks = ["Deerfields_Free_WiFi", "Other_Network", "Mobile_Data"]
        return random.choice(networks)
    
    def _is_player_in_zone(self, player_position: Dict, zone: Dict) -> bool:
        """Check if player is within zone radius"""
        zone_pos = zone["position"]
        distance = math.sqrt(
            (player_position["x"] - zone_pos["x"])**2 +
            (player_position["y"] - zone_pos["y"])**2 +
            (player_position["z"] - zone_pos["z"])**2
        )
        return distance <= zone["radius"]
    
    def _is_zone_on_cooldown(self, zone: Dict) -> bool:
        """Check if zone is on cooldown"""
        if not zone["last_triggered"]:
            return False
        
        elapsed = (datetime.now() - zone["last_triggered"]).total_seconds()
        return elapsed < zone["cooldown"]
    
    def _get_remaining_cooldown(self, zone: Dict) -> int:
        """Get remaining cooldown time in seconds"""
        if not zone["last_triggered"]:
            return 0
        
        elapsed = (datetime.now() - zone["last_triggered"]).total_seconds()
        remaining = zone["cooldown"] - elapsed
        return max(0, int(remaining))
    
    def _trigger_coin_sparkle_effect(self, amount: int):
        """Trigger coin sparkle visual effect"""
        logger.info(f"[3D GRAPHICS] 🪙 Coin sparkle effect: {amount} coins!")
        # In real implementation, this would trigger actual visual effects
    
    def _trigger_xp_burst_effect(self, amount: int):
        """Trigger XP burst visual effect"""
        logger.info(f"[3D GRAPHICS] ⚡ XP burst effect: {amount} XP!")
        # In real implementation, this would trigger actual visual effects
    
    def _trigger_vip_flash_effect(self, amount: int):
        """Trigger VIP flash visual effect"""
        logger.info(f"[3D GRAPHICS] 👑 VIP flash effect: {amount} VIP points!")
        # In real implementation, this would trigger actual visual effects
    
    def set_ui_language_support(self, languages: List[str]):
        """Set UI language support for bilingual interface"""
        supported_languages = {
            "en": {
                "name": "English",
                "direction": "ltr",
                "font": "Dubai",
                "translations": {
                    "play": "Play",
                    "quests": "Quests", 
                    "rewards": "Rewards",
                    "profile": "Profile",
                    "coins": "Coins",
                    "xp": "XP",
                    "level": "Level",
                    "settings": "Settings",
                    "language": "Language",
                    "back": "Back",
                    "confirm": "Confirm",
                    "cancel": "Cancel",
                    "loading": "Loading...",
                    "error": "Error",
                    "success": "Success"
                }
            },
            "ar": {
                "name": "العربية",
                "direction": "rtl",
                "font": "Dubai",
                "translations": {
                    "play": "العب",
                    "quests": "المهام",
                    "rewards": "المكافآت",
                    "profile": "الملف الشخصي",
                    "coins": "العملات",
                    "xp": "النقاط",
                    "level": "المستوى",
                    "settings": "الإعدادات",
                    "language": "اللغة",
                    "back": "رجوع",
                    "confirm": "تأكيد",
                    "cancel": "إلغاء",
                    "loading": "جاري التحميل...",
                    "error": "خطأ",
                    "success": "نجح"
                }
            }
        }
        
        # Validate requested languages
        valid_languages = []
        for lang in languages:
            if lang in supported_languages:
                valid_languages.append(lang)
                self.language_support[lang] = supported_languages[lang]
            else:
                logger.warning(f"[3D GRAPHICS] Warning: Language '{lang}' not supported")
        
        # Set default language
        if valid_languages:
            self.ui_system["current_language"] = valid_languages[0]
            self.ui_system["supported_languages"] = valid_languages
            logger.info(f"[3D GRAPHICS] UI language support set: {valid_languages}")
            return {"status": "success", "languages": valid_languages}
        else:
            return {"status": "error", "message": "No valid languages provided"}
    
    def load_main_menu(self, options: List[str], font: str = "Dubai"):
        """Load main menu with specified options"""
        menu_config = {
            "options": options,
            "font": font,
            "style": {
                "background": "#1a1a1a",
                "text_color": "#ffffff",
                "highlight_color": "#FFD700",
                "border_color": "#333333",
                "border_radius": 10,
                "padding": 20
            },
            "layout": {
                "position": "center",
                "width": 400,
                "height": 500,
                "spacing": 15
            },
            "animations": {
                "fade_in": True,
                "slide_in": True,
                "hover_effects": True
            },
            "created_at": datetime.now()
        }
        
        self.main_menu = menu_config
        logger.info(f"[3D GRAPHICS] Main menu loaded: {options} (font: {font})")
        return {"status": "success", "menu": menu_config}
    
    def add_top_bar(self, coins_visible: bool = True, language_toggle: bool = True):
        """Add top bar with coins display and language toggle"""
        top_bar_config = {
            "coins_visible": coins_visible,
            "language_toggle": language_toggle,
            "style": {
                "background": "#2a2a2a",
                "text_color": "#ffffff",
                "coin_color": "#FFD700",
                "border_color": "#444444",
                "height": 60,
                "padding": 15
            },
            "elements": {
                "coins_display": {
                    "visible": coins_visible,
                    "position": "left",
                    "icon": "🪙",
                    "font": "Dubai",
                    "size": 16
                },
                "language_toggle": {
                    "visible": language_toggle,
                    "position": "right",
                    "icon": "🌐",
                    "font": "Dubai",
                    "size": 14
                },
                "xp_display": {
                    "visible": True,
                    "position": "center",
                    "icon": "⚡",
                    "font": "Dubai",
                    "size": 14
                }
            },
            "animations": {
                "slide_down": True,
                "coin_counter": True,
                "language_switch": True
            },
            "created_at": datetime.now()
        }
        
        self.top_bar = top_bar_config
        logger.info(f"[3D GRAPHICS] Top bar added (coins: {coins_visible}, language: {language_toggle})")
        return {"status": "success", "top_bar": top_bar_config}
    
    def switch_language(self, language: str):
        """Switch UI language"""
        if language in self.language_support:
            self.ui_system["current_language"] = language
            lang_config = self.language_support[language]
            logger.info(f"[3D GRAPHICS] Language switched to: {lang_config['name']} ({lang_config['direction']})")
            return {"status": "success", "language": language, "direction": lang_config["direction"]}
        else:
            return {"status": "error", "message": f"Language '{language}' not supported"}
    
    def get_translation(self, key: str, language: str = None):
        """Get translation for specific key"""
        if not language:
            language = self.ui_system.get("current_language", "en")
        
        if language in self.language_support:
            translations = self.language_support[language]["translations"]
            return translations.get(key, key)
        else:
            return key
    
    def render_main_menu(self):
        """Render main menu with current language"""
        if not self.main_menu:
            return {"status": "error", "message": "Main menu not loaded"}
        
        current_lang = self.ui_system.get("current_language", "en")
        lang_config = self.language_support.get(current_lang, {})
        
        menu_items = []
        for option in self.main_menu["options"]:
            translated_option = self.get_translation(option.lower(), current_lang)
            menu_items.append({
                "original": option,
                "translated": translated_option,
                "direction": lang_config.get("direction", "ltr")
            })
        
        logger.info(f"[3D GRAPHICS] Main menu rendered in {current_lang}")
        return {"status": "success", "menu_items": menu_items, "language": current_lang}
    
    def render_top_bar(self, coins: int = 0, xp: int = 0):
        """Render top bar with current values"""
        if not self.top_bar:
            return {"status": "error", "message": "Top bar not loaded"}
        
        current_lang = self.ui_system.get("current_language", "en")
        lang_config = self.language_support.get(current_lang, {})
        
        top_bar_data = {
            "coins": {
                "value": coins,
                "label": self.get_translation("coins", current_lang),
                "visible": self.top_bar["coins_visible"]
            },
            "xp": {
                "value": xp,
                "label": self.get_translation("xp", current_lang),
                "visible": self.top_bar["elements"]["xp_display"]["visible"]
            },
            "language": {
                "current": current_lang,
                "name": lang_config.get("name", current_lang),
                "direction": lang_config.get("direction", "ltr"),
                "toggle_visible": self.top_bar["language_toggle"]
            }
        }
        
        logger.info(f"[3D GRAPHICS] Top bar rendered (coins: {coins}, xp: {xp}, lang: {current_lang})")
        return {"status": "success", "top_bar_data": top_bar_data}
    
    def update_coin_display(self, new_amount: int):
        """Update coin display in top bar"""
        if self.top_bar and self.top_bar["coins_visible"]:
            logger.info(f"[3D GRAPHICS] Coin display updated: {new_amount}")
            return {"status": "success", "coins": new_amount}
        else:
            return {"status": "error", "message": "Coin display not enabled"}
    
    def update_xp_display(self, new_amount: int):
        """Update XP display in top bar - FIXED VERSION"""
        if self.top_bar and self.top_bar["elements"]["xp_display"]["visible"]:
            logger.info(f"[3D GRAPHICS] XP display updated: {new_amount}")
            return {"status": "success", "xp": new_amount}
        else:
            return {"status": "error", "message": "XP display not enabled"}
    
    def enable_login_streak_rewards(self, days_required: int = 5, bonus_coins: int = 20):
        """Enable login streak rewards for continuous presence"""
        streak_config = {
            "days_required": days_required,
            "bonus_coins": bonus_coins,
            "active": True,
            "current_streak": 0,
            "max_streak": 0,
            "last_login": None,
            "rewards": {
                "daily": {"coins": 5, "xp": 10},
                "weekly": {"coins": 25, "xp": 50},
                "monthly": {"coins": 100, "xp": 200},
                "streak_bonus": {"coins": bonus_coins, "xp": bonus_coins * 2}
            },
            "visual_effects": {
                "streak_counter": True,
                "celebration_animation": True,
                "progress_bar": True
            },
            "created_at": datetime.now()
        }
        
        self.incentive_system["login_streak"] = streak_config
        logger.info(f"[3D GRAPHICS] Login streak rewards enabled: {days_required} days for {bonus_coins} coins")
        return {"status": "success", "streak_config": streak_config}
    
    def play_sound(self, sound_file: str):
        """Play sound effect for rewards and interactions"""
        sound_config = {
            "file": sound_file,
            "volume": 0.8,
            "loop": False,
            "category": self._get_sound_category(sound_file),
            "effects": {
                "fade_in": True,
                "spatial_audio": True,
                "priority": "high"
            },
            "played_at": datetime.now()
        }
        
        self.sound_system[sound_file] = sound_config
        
        # Trigger sound effect
        self._trigger_sound_effect(sound_file)
        
        logger.info(f"[3D GRAPHICS] Sound played: {sound_file}")
        return {"status": "success", "sound": sound_config}
    
    def create_daily_quest(self, title: str, reward: int = 15):
        """Create daily quest with specific reward"""
        quest_config = {
            "title": title,
            "reward": reward,
            "type": "daily",
            "status": "active",
            "progress": 0,
            "target": 1,
            "expires_at": self._get_tomorrow_midnight(),
            "requirements": self._parse_quest_requirements(title),
            "rewards": {
                "coins": reward,
                "xp": reward * 2,
                "special_items": []
            },
            "visual_effects": {
                "quest_icon": True,
                "progress_indicator": True,
                "completion_celebration": True
            },
            "created_at": datetime.now()
        }
        
        quest_id = f"daily_{int(time.time())}"
        self.quest_system[quest_id] = quest_config
        
        logger.info(f"[3D GRAPHICS] Daily quest created: {title} ({reward} coins)")
        return {"status": "success", "quest_id": quest_id, "quest": quest_config}
    
    def integrate_with_brand(self, brand_name: str, feature: str):
        """Integrate with luxury brands for exclusive features"""
        brand_config = {
            "name": brand_name,
            "feature": feature,
            "type": "luxury",
            "active": True,
            "exclusive_offers": self._generate_brand_offers(brand_name, feature),
            "rewards": {
                "coins": 50,
                "xp": 100,
                "special_items": [f"{brand_name}_Exclusive_Coupon"],
                "vip_points": 25
            },
            "visual_effects": {
                "brand_logo": True,
                "luxury_animation": True,
                "exclusive_glow": True
            },
            "integration_date": datetime.now()
        }
        
        self.brand_integration[brand_name] = brand_config
        logger.info(f"[3D GRAPHICS] Brand integration: {brand_name} - {feature}")
        return {"status": "success", "brand": brand_config}
    
    def record_login(self, user_id: str):
        """Record user login for streak tracking"""
        if "login_streak" not in self.incentive_system:
            return {"status": "error", "message": "Login streak system not enabled"}
        
        streak_config = self.incentive_system["login_streak"]
        today = datetime.now().date()
        
        # Check if this is a consecutive login
        if streak_config["last_login"]:
            last_login_date = streak_config["last_login"].date()
            days_diff = (today - last_login_date).days
            
            if days_diff == 1:
                # Consecutive login
                streak_config["current_streak"] += 1
                logger.info(f"[3D GRAPHICS] Consecutive login: Day {streak_config['current_streak']}")
            elif days_diff > 1:
                # Streak broken
                streak_config["current_streak"] = 1
                logger.info(f"[3D GRAPHICS] Streak broken, starting new streak")
            else:
                # Same day login
                logger.info(f"[3D GRAPHICS] Same day login recorded")
        else:
            # First login
            streak_config["current_streak"] = 1
            logger.info(f"[3D GRAPHICS] First login recorded")
        
        # Update max streak
        if streak_config["current_streak"] > streak_config["max_streak"]:
            streak_config["max_streak"] = streak_config["current_streak"]
        
        streak_config["last_login"] = datetime.now()
        
        # Check for streak rewards
        reward_result = self._check_streak_rewards(streak_config)
        
        return {"status": "success", "streak": streak_config["current_streak"], "reward": reward_result}
    
    def complete_quest(self, quest_id: str, user_id: str):
        """Complete quest and award rewards"""
        if quest_id not in self.quest_system:
            return {"status": "error", "message": "Quest not found"}
        
        quest = self.quest_system[quest_id]
        
        if quest["status"] != "active":
            return {"status": "error", "message": "Quest not active"}
        
        if quest["progress"] < quest["target"]:
            return {"status": "error", "message": "Quest not completed"}
        
        # Mark quest as completed
        quest["status"] = "completed"
        quest["completed_at"] = datetime.now()
        
        # Award rewards
        rewards = quest["rewards"]
        
        # Play completion sound
        self.play_sound("quest_complete.wav")
        
        # Trigger visual effects
        self._trigger_quest_completion_effects(quest)
        
        logger.info(f"[3D GRAPHICS] Quest completed: {quest['title']}")
        return {"status": "success", "rewards": rewards, "quest": quest}
    
    def update_quest_progress(self, quest_id: str, progress: int = 1):
        """Update quest progress"""
        if quest_id not in self.quest_system:
            return {"status": "error", "message": "Quest not found"}
        
        quest = self.quest_system[quest_id]
        
        if quest["status"] != "active":
            return {"status": "error", "message": "Quest not active"}
        
        quest["progress"] += progress
        
        # Check if quest is completed
        if quest["progress"] >= quest["target"]:
            quest["status"] = "ready_to_claim"
            logger.info(f"[3D GRAPHICS] Quest ready to claim: {quest['title']}")
        
        return {"status": "success", "progress": quest["progress"], "target": quest["target"]}
    
    def get_active_quests(self):
        """Get all active quests"""
        active_quests = {}
        for quest_id, quest in self.quest_system.items():
            if quest["status"] == "active" or quest["status"] == "ready_to_claim":
                active_quests[quest_id] = quest
        
        return {"status": "success", "quests": active_quests}
    
    def get_brand_offers(self, brand_name: str = None):
        """Get brand offers and integrations"""
        if brand_name:
            if brand_name in self.brand_integration:
                return {"status": "success", "brand": self.brand_integration[brand_name]}
            else:
                return {"status": "error", "message": "Brand not found"}
        else:
            return {"status": "success", "brands": self.brand_integration}
    
    def _get_sound_category(self, sound_file: str) -> str:
        """Get sound category based on file name"""
        if "coin" in sound_file.lower():
            return "rewards"
        elif "quest" in sound_file.lower():
            return "quests"
        elif "level" in sound_file.lower():
            return "achievements"
        elif "brand" in sound_file.lower():
            return "brands"
        else:
            return "general"
    
    def _trigger_sound_effect(self, sound_file: str):
        """Trigger sound effect"""
        category = self._get_sound_category(sound_file)
        
        if category == "rewards":
            logger.info(f"[3D GRAPHICS] 🔊 Playing reward sound: {sound_file}")
        elif category == "quests":
            logger.info(f"[3D GRAPHICS] 🎯 Playing quest sound: {sound_file}")
        elif category == "achievements":
            logger.info(f"[3D GRAPHICS] 🏆 Playing achievement sound: {sound_file}")
        elif category == "brands":
            logger.info(f"[3D GRAPHICS] 🏛️ Playing brand sound: {sound_file}")
        else:
            logger.info(f"[3D GRAPHICS] 🔊 Playing general sound: {sound_file}")
    
    def _get_tomorrow_midnight(self) -> datetime:
        """Get tomorrow at midnight for quest expiration"""
        tomorrow = datetime.now() + timedelta(days=1)
        return tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    
    def _parse_quest_requirements(self, title: str) -> Dict:
        """Parse quest requirements from title"""
        requirements = {}
        
        if "scan" in title.lower() and "receipt" in title.lower():
            requirements["action"] = "scan_receipt"
            requirements["count"] = 1
        elif "visit" in title.lower() and "store" in title.lower():
            requirements["action"] = "visit_store"
            requirements["count"] = 1
        elif "spend" in title.lower():
            requirements["action"] = "spend_coins"
            requirements["amount"] = 50
        elif "play" in title.lower() and "game" in title.lower():
            requirements["action"] = "play_minigame"
            requirements["count"] = 1
        
        return requirements
    
    def _generate_brand_offers(self, brand_name: str, feature: str) -> List[Dict]:
        """Generate brand-specific offers"""
        offers = []
        
        if "Emirates Palace" in brand_name:
            offers = [
                {
                    "type": "exclusive_coupon",
                    "title": "Emirates Palace Luxury Discount",
                    "description": "20% off on luxury items",
                    "value": 20,
                    "expires_in": "7 days"
                },
                {
                    "type": "vip_access",
                    "title": "VIP Lounge Access",
                    "description": "Exclusive VIP lounge entry",
                    "value": "unlimited",
                    "expires_in": "30 days"
                }
            ]
        elif "Burj Al Arab" in brand_name:
            offers = [
                {
                    "type": "dining_voucher",
                    "title": "Fine Dining Experience",
                    "description": "Complimentary dining voucher",
                    "value": 100,
                    "expires_in": "14 days"
                }
            ]
        else:
            offers = [
                {
                    "type": "general_offer",
                    "title": f"{brand_name} Special Offer",
                    "description": f"Exclusive {feature} from {brand_name}",
                    "value": 15,
                    "expires_in": "30 days"
                }
            ]
        
        return offers
    
    def _check_streak_rewards(self, streak_config: Dict) -> Dict:
        """Check and award streak rewards"""
        current_streak = streak_config["current_streak"]
        days_required = streak_config["days_required"]
        
        if current_streak >= days_required:
            # Award streak bonus
            bonus_coins = streak_config["bonus_coins"]
            bonus_xp = bonus_coins * 2
            
            # Play celebration sound
            self.play_sound("streak_celebration.wav")
            
            # Trigger visual effects
            self._trigger_streak_celebration_effects(current_streak)
            
            logger.info(f"[3D GRAPHICS] 🎉 Streak reward: {current_streak} days! +{bonus_coins} coins")
            
            return {
                "type": "streak_bonus",
                "coins": bonus_coins,
                "xp": bonus_xp,
                "streak": current_streak
            }
        
        return {"type": "daily_login", "coins": 5, "xp": 10}
    
    def _trigger_quest_completion_effects(self, quest: Dict):
        """Trigger quest completion visual effects"""
        logger.info(f"[3D GRAPHICS] 🎯 Quest completion effects: {quest['title']}")
        # In real implementation, this would trigger actual visual effects
    
    def _trigger_streak_celebration_effects(self, streak_days: int):
        """Trigger streak celebration visual effects"""
        logger.info(f"[3D GRAPHICS] 🎉 Streak celebration effects: {streak_days} days!")
        # In real implementation, this would trigger actual visual effects
    
    def generate_invite_link(self, user_id: str):
        """Generate invite link for user if inside mall WiFi"""
        # Check if user is connected to mall WiFi
        if self.check_wifi_connection():
            invite_link = f"https://deerfieldsmall.com/invite/{user_id}"
            
            invite_config = {
                "user_id": user_id,
                "link": invite_link,
                "generated_at": datetime.now(),
                "active": True,
                "clicks": 0,
                "referrals": [],
                "rewards": {
                    "inviter": {"coins": 50, "xp": 100},
                    "invitee": {"coins": 25, "xp": 50}
                }
            }
            
            self.invite_system[user_id] = invite_config
            logger.info(f"[3D GRAPHICS] Invite link generated: {invite_link}")
            return {"status": "success", "invite_link": invite_link, "config": invite_config}
        else:
            return {"status": "error", "message": "Must be connected to mall WiFi to generate invite link"}
    
    def is_inside_mall(self, wifi_ssid: str = "Deerfields_Free_WiFi") -> bool:
        """Check if user is inside mall based on WiFi connection"""
        return self.check_wifi_connection() and self.wifi_restrictions.get("main", {}).get("ssid") == wifi_ssid
    
    def track_invite_click(self, user_id: str, referrer_id: str):
        """Track invite link click and award rewards"""
        if user_id not in self.invite_system:
            return {"status": "error", "message": "Invalid invite link"}
        
        invite_config = self.invite_system[user_id]
        invite_config["clicks"] += 1
        
        # Add referral if not already tracked
        if referrer_id not in invite_config["referrals"]:
            invite_config["referrals"].append(referrer_id)
            
            # Award rewards to inviter
            inviter_rewards = invite_config["rewards"]["inviter"]
            logger.info(f"[3D GRAPHICS] Inviter rewards: +{inviter_rewards['coins']} coins, +{inviter_rewards['xp']} XP")
            
            # Award rewards to invitee
            invitee_rewards = invite_config["rewards"]["invitee"]
            logger.info(f"[3D GRAPHICS] Invitee rewards: +{invitee_rewards['coins']} coins, +{invitee_rewards['xp']} XP")
            
            # Play celebration sound
            self.play_sound("invite_success.wav")
            
            # Trigger visual effects
            self._trigger_invite_success_effects(user_id, referrer_id)
        
        return {"status": "success", "clicks": invite_config["clicks"], "referrals": len(invite_config["referrals"])}
    
    def get_invite_stats(self, user_id: str):
        """Get invite statistics for user"""
        if user_id not in self.invite_system:
            return {"status": "error", "message": "No invite data found"}
        
        invite_config = self.invite_system[user_id]
        return {
            "status": "success",
            "user_id": user_id,
            "link": invite_config["link"],
            "clicks": invite_config["clicks"],
            "referrals": len(invite_config["referrals"]),
            "total_rewards": {
                "coins": invite_config["rewards"]["inviter"]["coins"] * len(invite_config["referrals"]),
                "xp": invite_config["rewards"]["inviter"]["xp"] * len(invite_config["referrals"])
            },
            "generated_at": invite_config["generated_at"]
        }
    
    def create_user(self, user_id: str, name: str, email: str = None):
        """Create user for invite system"""
        user_config = {
            "user_id": user_id,
            "name": name,
            "email": email,
            "created_at": datetime.now(),
            "last_active": datetime.now(),
            "stats": {
                "total_coins": 0,
                "total_xp": 0,
                "level": 1,
                "invites_sent": 0,
                "invites_received": 0
            }
        }
        
        self.user_management[user_id] = user_config
        logger.info(f"[3D GRAPHICS] User created: {name} ({user_id})")
        return {"status": "success", "user": user_config}
    
    def get_user(self, user_id: str):
        """Get user information"""
        if user_id not in self.user_management:
            return {"status": "error", "message": "User not found"}
        
        return {"status": "success", "user": self.user_management[user_id]}
    
    def update_user_stats(self, user_id: str, coins: int = 0, xp: int = 0):
        """Update user statistics"""
        if user_id not in self.user_management:
            return {"status": "error", "message": "User not found"}
        
        user = self.user_management[user_id]
        user["stats"]["total_coins"] += coins
        user["stats"]["total_xp"] += xp
        user["last_active"] = datetime.now()
        
        # Level up calculation (every 1000 XP)
        new_level = (user["stats"]["total_xp"] // 1000) + 1
        if new_level > user["stats"]["level"]:
            user["stats"]["level"] = new_level
            logger.info(f"[3D GRAPHICS] User {user_id} leveled up to {new_level}!")
            self.play_sound("level_up.wav")
        
        return {"status": "success", "user": user}
    
    def _trigger_invite_success_effects(self, user_id: str, referrer_id: str):
        """Trigger invite success visual effects"""
        logger.info(f"[3D GRAPHICS] 🎉 Invite success effects: {user_id} invited by {referrer_id}")
        # In real implementation, this would trigger actual visual effects
    
    def load_environment(self, model_file: str, lighting: str = "realistic", resolution: str = "ultra"):
        """Load 3D mall interior environment"""
        environment_config = {
            "model_file": model_file,
            "lighting": lighting,
            "resolution": resolution,
            "loaded_at": datetime.now(),
            "features": {
                "realistic_lighting": lighting == "realistic",
                "ultra_resolution": resolution == "ultra",
                "dynamic_shadows": True,
                "reflections": True,
                "ambient_occlusion": True
            },
            "zones": {
                "zone_a": {"x": 0, "y": 0, "z": 0, "type": "shopping"},
                "zone_b": {"x": 50, "y": 0, "z": 0, "type": "beauty"},
                "zone_c": {"x": 100, "y": 0, "z": 0, "type": "receipt_scanning"},
                "main_entrance": {"x": -50, "y": 0, "z": 0, "type": "entrance"},
                "food_court": {"x": 150, "y": 0, "z": 0, "type": "dining"},
                "central_atrium": {"x": 25, "y": 0, "z": 25, "type": "common"}
            }
        }
        
        self.environment_3d["mall_interior"] = environment_config
        logger.info(f"[3D GRAPHICS] Environment loaded: {model_file} with {lighting} lighting at {resolution} resolution")
        return {"status": "success", "environment": environment_config}
    
    def set_camera(self, mode: str = "third_person", smooth: bool = True, collision: bool = True):
        """Set camera mode and properties"""
        camera_config = {
            "mode": mode,
            "smooth": smooth,
            "collision": collision,
            "position": {"x": 0, "y": 10, "z": -20},
            "target": {"x": 0, "y": 0, "z": 0},
            "fov": 60,
            "near_clip": 0.1,
            "far_clip": 1000,
            "settings": {
                "smooth_follow": smooth,
                "collision_detection": collision,
                "dynamic_fov": True,
                "motion_blur": True
            }
        }
        
        self.environment_3d["camera"] = camera_config
        logger.info(f"[3D GRAPHICS] Camera set: {mode} mode, smooth={smooth}, collision={collision}")
        return {"status": "success", "camera": camera_config}
    
    def create_avatar(self, name: str, style: str = "arab_emirati", outfit: str = "kandura", speed: float = 1.5):
        """Create player avatar with Emirati style"""
        avatar_config = {
            "name": name,
            "style": style,
            "outfit": outfit,
            "speed": speed,
            "position": {"x": 0, "y": 0, "z": 0},
            "rotation": {"x": 0, "y": 0, "z": 0},
            "appearance": {
                "kandura_color": "white",
                "ghutra_color": "red_white",
                "accessories": ["watch", "sunglasses"],
                "height": 1.75,
                "build": "average"
            },
            "animations": {
                "idle": "kandura_idle",
                "walk": "kandura_walk",
                "run": "kandura_run",
                "wave": "kandura_wave",
                "dance": "traditional_dance"
            },
            "created_at": datetime.now()
        }
        
        self.avatar_system[name] = avatar_config
        logger.info(f"[3D GRAPHICS] Avatar created: {name} with {style} style, {outfit} outfit")
        return {"status": "success", "avatar": avatar_config}
    
    def attach_companion(self, player_name: str, companion_type: str = "falcon_drone"):
        """Attach companion to player avatar"""
        companion_config = {
            "type": companion_type,
            "player": player_name,
            "position": {"x": 2, "y": 3, "z": 0},
            "follow_distance": 2.0,
            "behavior": {
                "follow_mode": "smooth",
                "hover_height": 3.0,
                "rotation_speed": 0.5,
                "idle_animation": "falcon_hover"
            },
            "features": {
                "camera_feed": True,
                "light_effects": True,
                "sound_effects": True
            }
        }
        
        if player_name in self.avatar_system:
            self.avatar_system[player_name]["companion"] = companion_config
            logger.info(f"[3D GRAPHICS] Companion attached: {companion_type} to {player_name}")
            return {"status": "success", "companion": companion_config}
        else:
            return {"status": "error", "message": "Player avatar not found"}
    
    def add_shop(self, location: str, brand: str, interactive: bool = True, offer: str = ""):
        """Add realistic shop with brand and offers"""
        shop_config = {
            "location": location,
            "brand": brand,
            "interactive": interactive,
            "offer": offer,
            "position": self._get_zone_position(location),
            "appearance": {
                "storefront": f"{brand.lower()}_storefront",
                "logo": f"{brand.lower()}_logo",
                "lighting": "store_lighting",
                "display_windows": True
            },
            "interactions": {
                "enter_shop": True,
                "view_offers": True,
                "scan_products": True,
                "purchase_items": True
            },
            "offers": [offer] if offer else [],
            "created_at": datetime.now()
        }
        
        shop_id = f"{brand.lower()}_{location}"
        self.shop_system[shop_id] = shop_config
        logger.info(f"[3D GRAPHICS] Shop added: {brand} at {location} with offer: {offer}")
        return {"status": "success", "shop": shop_config}
    
    def create_mission(self, title: str, reward: str, condition: str, location: str = None, time_limit: str = None):
        """Create realistic mission inside mall"""
        mission_config = {
            "title": title,
            "reward": reward,
            "condition": condition,
            "location": location,
            "time_limit": time_limit,
            "status": "active",
            "progress": 0,
            "target": self._parse_mission_target(condition),
            "requirements": self._parse_mission_requirements(condition),
            "rewards": self._parse_reward_string(reward),
            "visual_effects": {
                "mission_marker": True,
                "progress_bar": True,
                "completion_celebration": True
            },
            "created_at": datetime.now()
        }
        
        mission_id = f"mission_{int(time.time())}"
        self.mission_system[mission_id] = mission_config
        logger.info(f"[3D GRAPHICS] Mission created: {title} with reward {reward}")
        return {"status": "success", "mission_id": mission_id, "mission": mission_config}
    
    def trigger_visual_effect(self, effect_type: str, payload: Dict = None):
        """Trigger visual effects for rewards and interactions"""
        if payload is None:
            payload = {}
        
        effect_config = {
            "type": effect_type,
            "payload": payload,
            "triggered_at": datetime.now(),
            "duration": 3.0,
            "particles": self._generate_effect_particles(effect_type, payload)
        }
        
        # Enhanced visual effects
        if effect_type == "coin_shower":
            amount = payload.get("amount", 10)
            color = payload.get("color", "gold")
            logger.info(f"[3D GRAPHICS] 🪙 Coin shower effect: {amount} {color} coins!")
            self.play_sound("coin_collect.wav")
        elif effect_type == "mission_complete":
            logger.info(f"[3D GRAPHICS] 🎯 Mission completion effect!")
            self.play_sound("mission_complete.wav")
        elif effect_type == "level_up":
            logger.info(f"[3D GRAPHICS] 🏆 Level up celebration effect!")
            self.play_sound("level_up.wav")
        
        return {"status": "success", "effect": effect_config}
    
    def set_environment_lighting(self, mode: str, reflections: bool = True, firework_show: bool = False):
        """Set environment lighting for day/night and special events"""
        lighting_config = {
            "mode": mode,
            "reflections": reflections,
            "firework_show": firework_show,
            "settings": {
                "ambient_light": self._get_lighting_preset(mode),
                "directional_light": self._get_directional_light(mode),
                "reflection_intensity": 0.8 if reflections else 0.0,
                "shadow_quality": "ultra"
            },
            "special_effects": {
                "fireworks": firework_show,
                "particle_systems": True,
                "dynamic_lighting": True
            },
            "applied_at": datetime.now()
        }
        
        self.environment_3d["lighting"] = lighting_config
        logger.info(f"[3D GRAPHICS] Environment lighting set: {mode} mode with reflections={reflections}")
        return {"status": "success", "lighting": lighting_config}
    
    def add_banner(self, text: str, language: str = "ar", location: str = "entrance"):
        """Add banner for special events and celebrations"""
        banner_config = {
            "text": text,
            "language": language,
            "location": location,
            "position": self._get_zone_position(location),
            "appearance": {
                "font": "Dubai" if language == "ar" else "Arial",
                "size": "large",
                "color": "gold",
                "animation": "floating"
            },
            "effects": {
                "glow": True,
                "particles": True,
                "sound": "banner_appear.wav"
            },
            "created_at": datetime.now()
        }
        
        banner_id = f"banner_{int(time.time())}"
        self.environment_3d["banners"] = self.environment_3d.get("banners", {})
        self.environment_3d["banners"][banner_id] = banner_config
        logger.info(f"[3D GRAPHICS] Banner added: {text} at {location}")
        return {"status": "success", "banner": banner_config}
    
    def add_ai_npc(self, name: str, role: str, dialogue: Dict):
        """Add AI NPC for player guidance"""
        npc_config = {
            "name": name,
            "role": role,
            "dialogue": dialogue,
            "position": {"x": 0, "y": 0, "z": 0},
            "appearance": {
                "model": f"{role}_npc",
                "animations": ["idle", "wave", "talk"],
                "outfit": "mall_guide_uniform"
            },
            "behavior": {
                "greeting_distance": 5.0,
                "interaction_range": 3.0,
                "auto_approach": True,
                "helpful_responses": True
            },
            "ai_features": {
                "pathfinding": True,
                "conversation": True,
                "guidance": True,
                "multilingual": True
            },
            "created_at": datetime.now()
        }
        
        self.ai_npc_system[name] = npc_config
        logger.info(f"[3D GRAPHICS] AI NPC added: {name} as {role}")
        return {"status": "success", "npc": npc_config}
    
    def define_walk_path(self, start: str, end: str, waypoints: List[str]):
        """Define realistic walking path through mall"""
        path_config = {
            "start": start,
            "end": end,
            "waypoints": waypoints,
            "path_points": self._generate_path_points(start, end, waypoints),
            "properties": {
                "walking_speed": 1.5,
                "smooth_transitions": True,
                "collision_avoidance": True,
                "auto_navigation": True
            },
            "features": {
                "path_visualization": True,
                "progress_indicator": True,
                "shortcut_options": True
            },
            "created_at": datetime.now()
        }
        
        path_id = f"path_{start}_{end}"
        self.path_system[path_id] = path_config
        logger.info(f"[3D GRAPHICS] Walk path defined: {start} to {end} via {waypoints}")
        return {"status": "success", "path": path_config}
    
    def add_game_zone(self, name: str, activities: List[str], age_limit: int = 12):
        """Add kids play zone with age-appropriate activities"""
        zone_config = {
            "name": name,
            "activities": activities,
            "age_limit": age_limit,
            "position": {"x": 200, "y": 0, "z": 0},
            "appearance": {
                "theme": "colorful_playground",
                "safety_features": True,
                "bright_colors": True,
                "fun_lighting": True
            },
            "games": {
                "coin_hunt": {"difficulty": "easy", "reward": 10},
                "slide_game": {"difficulty": "easy", "reward": 15},
                "color_match": {"difficulty": "medium", "reward": 20}
            },
            "safety": {
                "age_verification": True,
                "parental_controls": True,
                "safe_environment": True
            },
            "created_at": datetime.now()
        }
        
        self.kid_zone_system[name] = zone_config
        logger.info(f"[3D GRAPHICS] Kids zone added: {name} with {activities}")
        return {"status": "success", "zone": zone_config}
    
    def track_user_location(self, live: bool = True, trigger_events_nearby: bool = True):
        """Track user location and trigger nearby events"""
        tracking_config = {
            "live": live,
            "trigger_events_nearby": trigger_events_nearby,
            "update_frequency": 0.1,  # 10 times per second
            "features": {
                "real_time_tracking": live,
                "proximity_events": trigger_events_nearby,
                "location_history": True,
                "heat_map": True
            },
            "triggers": {
                "near_shop": 5.0,  # meters
                "near_mission": 3.0,
                "near_npc": 4.0,
                "near_coin_drop": 2.0
            },
            "started_at": datetime.now()
        }
        
        self.location_tracking["config"] = tracking_config
        logger.info(f"[3D GRAPHICS] Location tracking enabled: live={live}, events={trigger_events_nearby}")
        return {"status": "success", "tracking": tracking_config}
    
    def show_mall_map_overlay(self, highlight: List[str]):
        """Show mall map overlay with highlighted features"""
        map_config = {
            "highlight": highlight,
            "features": {
                "offers": "offers" in highlight,
                "missions": "missions" in highlight,
                "coin_drop": "coin_drop" in highlight,
                "shops": "shops" in highlight,
                "npcs": "npcs" in highlight
            },
            "display": {
                "overlay_mode": True,
                "interactive": True,
                "zoom_level": 1.0,
                "rotation": 0.0
            },
            "markers": self._generate_map_markers(highlight),
            "shown_at": datetime.now()
        }
        
        self.location_tracking["map_overlay"] = map_config
        logger.info(f"[3D GRAPHICS] Mall map overlay shown with highlights: {highlight}")
        return {"status": "success", "map": map_config}
    
    def _get_zone_position(self, zone: str) -> Dict:
        """Get position for a specific zone"""
        zones = self.environment_3d.get("mall_interior", {}).get("zones", {})
        return zones.get(zone, {"x": 0, "y": 0, "z": 0})
    
    def _parse_mission_target(self, condition: str) -> int:
        """Parse mission target from condition"""
        if "3" in condition:
            return 3
        elif "1" in condition:
            return 1
        else:
            return 1
    
    def _parse_mission_requirements(self, condition: str) -> Dict:
        """Parse mission requirements from condition"""
        requirements = {}
        
        if "receipt" in condition.lower():
            requirements["action"] = "scan_receipt"
        elif "arcade" in condition.lower():
            requirements["action"] = "play_arcade"
        elif "visit" in condition.lower():
            requirements["action"] = "visit_location"
        
        return requirements
    
    def _parse_reward_string(self, reward: str) -> Dict:
        """Parse reward string to extract coins and other rewards"""
        coins = 0
        if "coins" in reward.lower():
            import re
            coin_match = re.search(r'(\d+)\s*coins?', reward.lower())
            if coin_match:
                coins = int(coin_match.group(1))
        
        return {"coins": coins, "xp": coins * 2}
    
    def _generate_effect_particles(self, effect_type: str, payload: Dict) -> List[Dict]:
        """Generate particle effects for visual effects"""
        particles = []
        
        if effect_type == "coin_shower":
            amount = payload.get("amount", 10)
            color = payload.get("color", "gold")
            for i in range(amount):
                particles.append({
                    "type": "coin",
                    "color": color,
                    "position": {"x": i * 0.5, "y": 5, "z": 0},
                    "velocity": {"x": 0, "y": -2, "z": 0}
                })
        
        return particles
    
    def _get_lighting_preset(self, mode: str) -> Dict:
        """Get lighting preset for different modes"""
        presets = {
            "day_mode": {"intensity": 1.0, "color": [1.0, 1.0, 1.0]},
            "night_mode": {"intensity": 0.3, "color": [0.2, 0.3, 0.8]},
            "sunset_mode": {"intensity": 0.7, "color": [1.0, 0.6, 0.3]},
            "celebration_mode": {"intensity": 1.2, "color": [1.0, 1.0, 1.0]}
        }
        return presets.get(mode, presets["day_mode"])
    
    def _get_directional_light(self, mode: str) -> Dict:
        """Get directional light settings for different modes"""
        lights = {
            "day_mode": {"direction": [0, 1, 0], "intensity": 1.0},
            "night_mode": {"direction": [0, -1, 0], "intensity": 0.2},
            "sunset_mode": {"direction": [0.5, 0.5, 0], "intensity": 0.8},
            "celebration_mode": {"direction": [0, 1, 0], "intensity": 1.5}
        }
        return lights.get(mode, lights["day_mode"])
    
    def _generate_path_points(self, start: str, end: str, waypoints: List[str]) -> List[Dict]:
        """Generate path points for walking path"""
        points = []
        
        # Start point
        start_pos = self._get_zone_position(start)
        points.append(start_pos)
        
        # Waypoints
        for waypoint in waypoints:
            waypoint_pos = self._get_zone_position(waypoint)
            points.append(waypoint_pos)
        
        # End point
        end_pos = self._get_zone_position(end)
        points.append(end_pos)
        
        return points
    
    def _generate_map_markers(self, highlight: List[str]) -> List[Dict]:
        """Generate map markers for highlighted features"""
        markers = []
        
        for feature in highlight:
            if feature == "offers":
                markers.append({"type": "offer", "position": {"x": 0, "y": 0, "z": 0}, "icon": "🔥"})
            elif feature == "missions":
                markers.append({"type": "mission", "position": {"x": 50, "y": 0, "z": 0}, "icon": "🎯"})
            elif feature == "coin_drop":
                markers.append({"type": "coin", "position": {"x": 100, "y": 0, "z": 0}, "icon": "🪙"})
        
        return markers
    
    def _generate_mall_vertices(self) -> List[Dict]:
        """Generate mall interior vertices"""
        return [
            # Main atrium
            {"x": -50, "y": 0, "z": -50}, {"x": 50, "y": 0, "z": -50},
            {"x": 50, "y": 20, "z": -50}, {"x": -50, "y": 20, "z": -50},
            # Store fronts
            {"x": -40, "y": 0, "z": -30}, {"x": -20, "y": 0, "z": -30},
            {"x": 20, "y": 0, "z": -30}, {"x": 40, "y": 0, "z": -30},
            # Escalators
            {"x": -10, "y": 0, "z": 0}, {"x": 10, "y": 0, "z": 0},
            {"x": -10, "y": 10, "z": 0}, {"x": 10, "y": 10, "z": 0}
        ]
    
    def _generate_mall_textures(self) -> Dict:
        """Generate mall textures"""
        return {
            "floor": "marble_tiles.png",
            "walls": "modern_wallpaper.png",
            "ceiling": "acoustic_panels.png",
            "glass": "storefront_glass.png",
            "metal": "escalator_metal.png"
        }
    
    def _generate_mall_animations(self) -> List[Dict]:
        """Generate mall animations"""
        return [
            {
                "name": "escalator_motion",
                "type": "continuous",
                "duration": 5.0,
                "loop": True
            },
            {
                "name": "fountain_water",
                "type": "particle",
                "duration": 2.0,
                "loop": True
            },
            {
                "name": "lighting_cycle",
                "type": "color_transition",
                "duration": 30.0,
                "loop": True
            }
        ]

class VisualEffects:
    """Visual effects system for gamification"""
    
    def __init__(self, graphics_engine: GraphicsEngine):
        self.graphics_engine = graphics_engine
        self.active_effects = []
        self.effect_templates = self._load_effect_templates()
    
    def trigger_coin_drop(self, position: Dict, amount: int):
        """Trigger animated coin drop effect"""
        effect = {
            "type": "coin_drop",
            "position": position,
            "amount": amount,
            "duration": 2.0,
            "particles": self._generate_coin_particles(amount),
            "sound": "coin_collect.wav"
        }
        
        self.active_effects.append(effect)
        logger.info(f"[VISUAL EFFECT] Coin drop: {amount} coins at {position}")
        return effect
    
    def trigger_level_up(self, user_id: str, new_level: int):
        """Trigger level up celebration effect"""
        effect = {
            "type": "level_up",
            "user_id": user_id,
            "level": new_level,
            "duration": 3.0,
            "particles": self._generate_celebration_particles(),
            "sound": "level_up_fanfare.wav",
            "screen_flash": True
        }
        
        self.active_effects.append(effect)
        logger.info(f"[VISUAL EFFECT] Level up: User {user_id} reached level {new_level}")
        return effect
    
    def trigger_mission_complete(self, mission_name: str, reward: int):
        """Trigger mission completion effect"""
        effect = {
            "type": "mission_complete",
            "mission": mission_name,
            "reward": reward,
            "duration": 2.5,
            "particles": self._generate_achievement_particles(),
            "sound": "mission_complete.wav",
            "badge_animation": True
        }
        
        self.active_effects.append(effect)
        logger.info(f"[VISUAL EFFECT] Mission complete: {mission_name}")
        return effect
    
    def trigger_receipt_submitted(self, store_name: str, coins_earned: int):
        """Trigger receipt submission effect"""
        effect = {
            "type": "receipt_submitted",
            "store": store_name,
            "coins": coins_earned,
            "duration": 1.5,
            "particles": self._generate_receipt_particles(),
            "sound": "receipt_scan.wav",
            "store_highlight": True
        }
        
        self.active_effects.append(effect)
        logger.info(f"[VISUAL EFFECT] Receipt submitted: {store_name}")
        return effect
    
    def _generate_coin_particles(self, amount: int) -> List[Dict]:
        """Generate coin particle effects"""
        particles = []
        for i in range(min(amount, 20)):  # Max 20 particles
            particles.append({
                "id": f"coin_{i}",
                "position": {"x": random.uniform(-2, 2), "y": 0, "z": random.uniform(-2, 2)},
                "velocity": {"x": random.uniform(-1, 1), "y": 2, "z": random.uniform(-1, 1)},
                "color": {"r": 1.0, "g": 0.8, "b": 0.0},
                "size": random.uniform(0.1, 0.3)
            })
        return particles
    
    def _generate_celebration_particles(self) -> List[Dict]:
        """Generate celebration particle effects"""
        particles = []
        colors = [
            {"r": 1.0, "g": 0.0, "b": 0.0},  # Red
            {"r": 0.0, "g": 1.0, "b": 0.0},  # Green
            {"r": 0.0, "g": 0.0, "b": 1.0},  # Blue
            {"r": 1.0, "g": 1.0, "b": 0.0},  # Yellow
            {"r": 1.0, "g": 0.0, "b": 1.0}   # Magenta
        ]
        
        for i in range(50):
            particles.append({
                "id": f"celebration_{i}",
                "position": {"x": random.uniform(-10, 10), "y": random.uniform(0, 10), "z": random.uniform(-10, 10)},
                "velocity": {"x": random.uniform(-3, 3), "y": random.uniform(1, 5), "z": random.uniform(-3, 3)},
                "color": random.choice(colors),
                "size": random.uniform(0.2, 0.8)
            })
        return particles
    
    def _generate_achievement_particles(self) -> List[Dict]:
        """Generate achievement particle effects"""
        particles = []
        for i in range(30):
            particles.append({
                "id": f"achievement_{i}",
                "position": {"x": random.uniform(-5, 5), "y": random.uniform(0, 8), "z": random.uniform(-5, 5)},
                "velocity": {"x": random.uniform(-2, 2), "y": random.uniform(0.5, 3), "z": random.uniform(-2, 2)},
                "color": {"r": 1.0, "g": 0.6, "b": 0.0},  # Orange
                "size": random.uniform(0.1, 0.4)
            })
        return particles
    
    def _generate_receipt_particles(self) -> List[Dict]:
        """Generate receipt submission particle effects"""
        particles = []
        for i in range(15):
            particles.append({
                "id": f"receipt_{i}",
                "position": {"x": random.uniform(-1, 1), "y": random.uniform(0, 3), "z": random.uniform(-1, 1)},
                "velocity": {"x": random.uniform(-0.5, 0.5), "y": random.uniform(1, 2), "z": random.uniform(-0.5, 0.5)},
                "color": {"r": 0.2, "g": 0.8, "b": 0.2},  # Green
                "size": random.uniform(0.05, 0.2)
            })
        return particles
    
    def _load_effect_templates(self) -> Dict:
        """Load effect templates"""
        return {
            "coin_drop": {
                "particle_count": 20,
                "duration": 2.0,
                "sound": "coin_collect.wav"
            },
            "level_up": {
                "particle_count": 50,
                "duration": 3.0,
                "sound": "level_up_fanfare.wav"
            },
            "mission_complete": {
                "particle_count": 30,
                "duration": 2.5,
                "sound": "mission_complete.wav"
            },
            "receipt_submitted": {
                "particle_count": 15,
                "duration": 1.5,
                "sound": "receipt_scan.wav"
            }
        }

class MallEnvironment:
    """3D Mall Environment Management"""
    
    def __init__(self, graphics_engine: GraphicsEngine):
        self.graphics_engine = graphics_engine
        self.stores = self._initialize_stores()
        self.interactive_zones = self._initialize_interactive_zones()
        self.ambient_effects = self._initialize_ambient_effects()
    
    def _initialize_stores(self) -> Dict:
        """Initialize mall stores with 3D positions"""
        return {
            "deerfields_fashion": {
                "name": "Deerfields Fashion",
                "position": {"x": -30, "y": 0, "z": -20},
                "size": {"width": 20, "height": 8, "depth": 15},
                "category": "clothing",
                "texture": "fashion_store.png",
                "lighting": {"intensity": 1.2, "color": {"r": 1.0, "g": 0.9, "b": 0.8}}
            },
            "deerfields_electronics": {
                "name": "Deerfields Electronics",
                "position": {"x": 30, "y": 0, "z": -20},
                "size": {"width": 25, "height": 8, "depth": 20},
                "category": "electronics",
                "texture": "electronics_store.png",
                "lighting": {"intensity": 1.0, "color": {"r": 0.8, "g": 0.9, "b": 1.0}}
            },
            "deerfields_cafe": {
                "name": "Deerfields Café",
                "position": {"x": 0, "y": 0, "z": 30},
                "size": {"width": 15, "height": 6, "depth": 12},
                "category": "food",
                "texture": "cafe_store.png",
                "lighting": {"intensity": 0.8, "color": {"r": 1.0, "g": 0.8, "b": 0.6}}
            }
        }
    
    def _initialize_interactive_zones(self) -> List[Dict]:
        """Initialize interactive zones in the mall"""
        return [
            {
                "name": "main_atrium",
                "position": {"x": 0, "y": 0, "z": 0},
                "size": {"width": 40, "height": 20, "depth": 40},
                "type": "social_area",
                "effects": ["ambient_music", "fountain_water", "people_movement"]
            },
            {
                "name": "escalator_area",
                "position": {"x": 0, "y": 0, "z": 10},
                "size": {"width": 8, "height": 15, "depth": 6},
                "type": "transport",
                "effects": ["escalator_motion", "mechanical_sound"]
            },
            {
                "name": "food_court",
                "position": {"x": -20, "y": 0, "z": 20},
                "size": {"width": 30, "height": 8, "depth": 25},
                "type": "dining",
                "effects": ["food_aromas", "conversation_sounds", "kitchen_noise"]
            }
        ]
    
    def _initialize_ambient_effects(self) -> List[Dict]:
        """Initialize ambient environmental effects"""
        return [
            {
                "name": "ambient_music",
                "type": "audio",
                "file": "mall_ambient.mp3",
                "volume": 0.3,
                "loop": True
            },
            {
                "name": "fountain_water",
                "type": "particle",
                "position": {"x": 0, "y": 1, "z": 0},
                "particle_count": 100,
                "color": {"r": 0.7, "g": 0.9, "b": 1.0}
            },
            {
                "name": "people_movement",
                "type": "animation",
                "npc_count": 20,
                "movement_pattern": "random_walk"
            }
        ]
    
    def get_store_position(self, store_name: str) -> Optional[Dict]:
        """Get 3D position of a store"""
        store = self.stores.get(store_name.lower().replace(" ", "_"))
        return store["position"] if store else None
    
    def highlight_store(self, store_name: str, duration: float = 2.0):
        """Highlight a store with visual effects"""
        store = self.stores.get(store_name.lower().replace(" ", "_"))
        if store:
            effect = {
                "type": "store_highlight",
                "store": store_name,
                "position": store["position"],
                "duration": duration,
                "lighting_intensity": 2.0,
                "glow_color": {"r": 1.0, "g": 1.0, "b": 0.0}
            }
            logger.info(f"[3D ENVIRONMENT] Highlighting store: {store_name}")
            return effect
        return None

class GraphicsController:
    """Main controller for 3D graphics integration"""
    
    def __init__(self):
        self.graphics_engine = GraphicsEngine()
        self.visual_effects = VisualEffects(self.graphics_engine)
        self.mall_environment = MallEnvironment(self.graphics_engine)
        self.is_initialized = False
    
    def initialize_3d_system(self):
        """Initialize the complete 3D graphics system"""
        # Enable 3D graphics
        self.graphics_engine.enable_3d_graphics(mode="realistic")
        
        # Set high quality graphics
        self.graphics_engine.set_graphics_quality(level="ultra")
        
        # Load mall 3D model
        self.graphics_engine.load_3d_model("deerfields_mall.glb", resolution="high", lighting="realistic")
        
        # Set realistic lighting
        self.graphics_engine.set_lighting(preset="indoor_daylight", shadows=True)
        
        # Enable smooth player motion
        self.graphics_engine.set_player_motion(smooth_physics=True)
        
        self.is_initialized = True
        logger.info("[3D GRAPHICS] Complete 3D system initialized successfully!")
        return {"status": "success", "message": "3D graphics system ready"}
    
    def trigger_gamification_effect(self, effect_type: str, **kwargs):
        """Trigger gamification visual effects"""
        if not self.is_initialized:
            self.initialize_3d_system()
        
        effects_map = {
            "coin_drop": self.visual_effects.trigger_coin_drop,
            "level_up": self.visual_effects.trigger_level_up,
            "mission_complete": self.visual_effects.trigger_mission_complete,
            "receipt_submitted": self.visual_effects.trigger_receipt_submitted
        }
        
        if effect_type in effects_map:
            return effects_map[effect_type](**kwargs)
        else:
            logger.info(f"[3D GRAPHICS] Unknown effect type: {effect_type}")
            return None
    
    def get_mall_environment_data(self):
        """Get complete mall environment data"""
        return {
            "stores": self.mall_environment.stores,
            "interactive_zones": self.mall_environment.interactive_zones,
            "ambient_effects": self.mall_environment.ambient_effects,
            "graphics_settings": {
                "mode": self.graphics_engine.graphics_mode,
                "quality": self.graphics_engine.quality_level,
                "lighting": self.graphics_engine.lighting_preset,
                "shadows": self.graphics_engine.shadows_enabled
            }
        }

# Global graphics controller instance
graphics_controller = GraphicsController()

# Global safe system initializer for dependency management
safe_system = SafeSystemInitializer()

# Convenience functions for easy integration
def enable_3d_graphics(mode="realistic"):
    """Enable 3D graphics with specified mode"""
    return graphics_controller.graphics_engine.enable_3d_graphics(mode)

def set_graphics_quality(level="ultra"):
    """Set graphics quality level"""
    return graphics_controller.graphics_engine.set_graphics_quality(level)

def load_3d_model(model_name="deerfields_mall.glb", resolution="high", lighting="realistic"):
    """Load 3D model with specified settings"""
    return graphics_controller.graphics_engine.load_3d_model(model_name, resolution, lighting)

def set_lighting(preset="indoor_daylight", shadows=True):
    """Set lighting configuration"""
    return graphics_controller.graphics_engine.set_lighting(preset, shadows)

def set_player_motion(smooth_physics=True):
    """Configure player motion physics"""
    return graphics_controller.graphics_engine.set_player_motion(smooth_physics)

def initialize_3d_system():
    """Initialize the complete 3D graphics system"""
    return graphics_controller.initialize_3d_system()

def trigger_visual_effect(effect_type: str, **kwargs):
    """Trigger visual effects for gamification"""
    return graphics_controller.trigger_gamification_effect(effect_type, **kwargs)

def get_safe_module(module_name: str):
    """Safely get module with None fallback"""
    return safe_system.get_module(module_name)

# Player Character Functions
def create_player_character(name="Visitor", avatar_style="modern"):
    """Create player character with specified style"""
    return graphics_controller.graphics_engine.create_player_character(name, avatar_style)

def add_player_animations(animation_list):
    """Add animations to player character"""
    return graphics_controller.graphics_engine.add_player_animations(animation_list)

def set_movement_zone(area="mall_interior", movement_type="freewalk"):
    """Set movement zone and type for player"""
    return graphics_controller.graphics_engine.set_movement_zone(area, movement_type)

def enable_third_person_camera(smooth_tracking=True):
    """Enable third-person camera with smooth tracking"""
    return graphics_controller.graphics_engine.enable_third_person_camera(smooth_tracking)

def move_player(direction, speed=1.0):
    """Move player character in specified direction"""
    return graphics_controller.graphics_engine.move_player(direction, speed)

def play_animation(animation_name):
    """Play specific animation for player character"""
    return graphics_controller.graphics_engine.play_animation(animation_name)

# Interactive Zone Functions
def create_interactive_zone(name, location, reward_type="coin"):
    """Create interactive mission zone with rewards"""
    return graphics_controller.graphics_engine.create_interactive_zone(name, location, reward_type)

def trigger_reward_effect(type="coin_sparkle", amount=10):
    """Trigger reward effects with visual feedback"""
    return graphics_controller.graphics_engine.trigger_reward_effect(type, amount)

def load_minigame(name, location, cooldown="2h"):
    """Load minigame at specific location"""
    return graphics_controller.graphics_engine.load_minigame(name, location, cooldown)

def lock_game_to_wifi(ssid="Deerfields_Free_WiFi"):
    """Lock game to specific WiFi network"""
    return graphics_controller.graphics_engine.lock_game_to_wifi(ssid)

def set_outside_warning(message_en, message_ar):
    """Set warning messages for outside connections"""
    return graphics_controller.graphics_engine.set_outside_warning(message_en, message_ar)

def check_wifi_connection():
    """Check if connected to mall WiFi"""
    return graphics_controller.graphics_engine.check_wifi_connection()

def trigger_zone_interaction(zone_name, player_position):
    """Trigger interaction with mission zone"""
    return graphics_controller.graphics_engine.trigger_zone_interaction(zone_name, player_position)

def start_minigame(minigame_name, player_position):
    """Start minigame if player is in location"""
    return graphics_controller.graphics_engine.start_minigame(minigame_name, player_position)

# UI System Functions
def set_ui_language_support(languages):
    """Set UI language support for bilingual interface"""
    return graphics_controller.graphics_engine.set_ui_language_support(languages)

def load_main_menu(options, font="Dubai"):
    """Load main menu with specified options"""
    return graphics_controller.graphics_engine.load_main_menu(options, font)

def add_top_bar(coins_visible=True, language_toggle=True):
    """Add top bar with coins display and language toggle"""
    return graphics_controller.graphics_engine.add_top_bar(coins_visible, language_toggle)

def switch_language(language):
    """Switch UI language"""
    return graphics_controller.graphics_engine.switch_language(language)

def get_translation(key, language=None):
    """Get translation for specific key"""
    return graphics_controller.graphics_engine.get_translation(key, language)

def render_main_menu():
    """Render main menu with current language"""
    return graphics_controller.graphics_engine.render_main_menu()

def render_top_bar(coins=0, xp=0):
    """Render top bar with current values"""
    return graphics_controller.graphics_engine.render_top_bar(coins, xp)

def update_coin_display(new_amount):
    """Update coin display in top bar"""
    return graphics_controller.graphics_engine.update_coin_display(new_amount)

def update_xp_display(new_amount):
    """Update XP display in top bar"""
    return graphics_controller.graphics_engine.update_xp_display(new_amount)

# Incentive System Functions
def enable_login_streak_rewards(days_required=5, bonus_coins=20):
    """Enable login streak rewards for continuous presence"""
    return graphics_controller.graphics_engine.enable_login_streak_rewards(days_required, bonus_coins)

def play_sound(sound_file):
    """Play sound effect for rewards and interactions"""
    return graphics_controller.graphics_engine.play_sound(sound_file)

def create_daily_quest(title, reward=15):
    """Create daily quest with specific reward"""
    return graphics_controller.graphics_engine.create_daily_quest(title, reward)

def integrate_with_brand(brand_name, feature):
    """Integrate with luxury brands for exclusive features"""
    return graphics_controller.graphics_engine.integrate_with_brand(brand_name, feature)

def record_login(user_id):
    """Record user login for streak tracking"""
    return graphics_controller.graphics_engine.record_login(user_id)

def complete_quest(quest_id, user_id):
    """Complete quest and award rewards"""
    return graphics_controller.graphics_engine.complete_quest(quest_id, user_id)

def update_quest_progress(quest_id, progress=1):
    """Update quest progress"""
    return graphics_controller.graphics_engine.update_quest_progress(quest_id, progress)

def get_active_quests():
    """Get all active quests"""
    return graphics_controller.graphics_engine.get_active_quests()

def get_brand_offers(brand_name=None):
    """Get brand offers and integrations"""
    return graphics_controller.graphics_engine.get_brand_offers(brand_name)

# Invite System Functions
def generate_invite_link(user_id):
    """Generate invite link for user if inside mall WiFi"""
    return graphics_controller.graphics_engine.generate_invite_link(user_id)

def is_inside_mall(wifi_ssid="Deerfields_Free_WiFi"):
    """Check if user is inside mall based on WiFi connection"""
    return graphics_controller.graphics_engine.is_inside_mall(wifi_ssid)

def track_invite_click(user_id, referrer_id):
    """Track invite link click and award rewards"""
    return graphics_controller.graphics_engine.track_invite_click(user_id, referrer_id)

def get_invite_stats(user_id):
    """Get invite statistics for user"""
    return graphics_controller.graphics_engine.get_invite_stats(user_id)

def create_user(user_id, name, email=None):
    """Create user for invite system"""
    return graphics_controller.graphics_engine.create_user(user_id, name, email)

def get_user(user_id):
    """Get user information"""
    return graphics_controller.graphics_engine.get_user(user_id)

def update_user_stats(user_id, coins=0, xp=0):
    """Update user statistics"""
    return graphics_controller.graphics_engine.update_user_stats(user_id, coins, xp)

# 3D Gaming Environment Functions
def load_environment(model_file, lighting="realistic", resolution="ultra"):
    """Load 3D mall interior environment"""
    return graphics_controller.graphics_engine.load_environment(model_file, lighting, resolution)

def set_camera(mode="third_person", smooth=True, collision=True):
    """Set camera mode and properties"""
    return graphics_controller.graphics_engine.set_camera(mode, smooth, collision)

def create_avatar(name, style="arab_emirati", outfit="kandura", speed=1.5):
    """Create player avatar with Emirati style"""
    return graphics_controller.graphics_engine.create_avatar(name, style, outfit, speed)

def attach_companion(player_name, companion_type="falcon_drone"):
    """Attach companion to player avatar"""
    return graphics_controller.graphics_engine.attach_companion(player_name, companion_type)

def add_shop(location, brand, interactive=True, offer=""):
    """Add realistic shop with brand and offers"""
    return graphics_controller.graphics_engine.add_shop(location, brand, interactive, offer)

def create_mission(title, reward, condition, location=None, time_limit=None):
    """Create realistic mission inside mall"""
    return graphics_controller.graphics_engine.create_mission(title, reward, condition, location, time_limit)

def trigger_visual_effect(effect_type, payload=None):
    """Trigger visual effects for rewards and interactions"""
    return graphics_controller.graphics_engine.trigger_visual_effect(effect_type, payload)

def set_environment_lighting(mode, reflections=True, firework_show=False):
    """Set environment lighting for day/night and special events"""
    return graphics_controller.graphics_engine.set_environment_lighting(mode, reflections, firework_show)

def add_banner(text, language="ar", location="entrance"):
    """Add banner for special events and celebrations"""
    return graphics_controller.graphics_engine.add_banner(text, language, location)

def add_ai_npc(name, role, dialogue):
    """Add AI NPC for player guidance"""
    return graphics_controller.graphics_engine.add_ai_npc(name, role, dialogue)

def define_walk_path(start, end, waypoints):
    """Define realistic walking path through mall"""
    return graphics_controller.graphics_engine.define_walk_path(start, end, waypoints)

def add_game_zone(name, activities, age_limit=12):
    """Add kids play zone with age-appropriate activities"""
    return graphics_controller.graphics_engine.add_game_zone(name, activities, age_limit)

def track_user_location(live=True, trigger_events_nearby=True):
    """Track user location and trigger nearby events"""
    return graphics_controller.graphics_engine.track_user_location(live, trigger_events_nearby)

def show_mall_map_overlay(highlight):
    """Show mall map overlay with highlighted features"""
    return graphics_controller.graphics_engine.show_mall_map_overlay(highlight) 