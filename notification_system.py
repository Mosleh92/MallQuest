#!/usr/bin/env python3
"""
Notification System for Deerfields Mall Gamification System
Informs players about new tasks, missions, and important events
"""

import random
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from database import db

class NotificationSystem:
    """Advanced notification system with different types and priorities"""
    
    def __init__(self):
        self.notification_types = {
            "mission": {
                "name": "New Mission",
                "icon": "🎯",
                "color": "#2196F3",
                "priority": "high",
                "auto_dismiss": False,
                "sound": "mission_notification"
            },
            "reward": {
                "name": "Reward Earned",
                "icon": "🎁",
                "color": "#4CAF50",
                "priority": "medium",
                "auto_dismiss": True,
                "sound": "reward_notification"
            },
            "level_up": {
                "name": "Level Up",
                "icon": "⭐",
                "color": "#FF9800",
                "priority": "high",
                "auto_dismiss": False,
                "sound": "level_up_notification"
            },
            "event": {
                "name": "Special Event",
                "icon": "🎉",
                "color": "#E91E63",
                "priority": "high",
                "auto_dismiss": False,
                "sound": "event_notification"
            },
            "reminder": {
                "name": "Reminder",
                "icon": "⏰",
                "color": "#9C27B0",
                "priority": "medium",
                "auto_dismiss": True,
                "sound": "reminder_notification"
            },
            "achievement": {
                "name": "Achievement Unlocked",
                "icon": "🏆",
                "color": "#FFD700",
                "priority": "high",
                "auto_dismiss": False,
                "sound": "achievement_notification"
            },
            "deer_care": {
                "name": "Deer Care",
                "icon": "🦌",
                "color": "#8BC34A",
                "priority": "medium",
                "auto_dismiss": True,
                "sound": "deer_care_notification"
            },
            "empire": {
                "name": "Empire Update",
                "icon": "🏛️",
                "color": "#607D8B",
                "priority": "medium",
                "auto_dismiss": True,
                "sound": "empire_notification"
            },
            "security": {
                "name": "Security Alert",
                "icon": "🔒",
                "color": "#F44336",
                "priority": "critical",
                "auto_dismiss": False,
                "sound": "security_notification"
            },
            "system": {
                "name": "System Message",
                "icon": "⚙️",
                "color": "#795548",
                "priority": "low",
                "auto_dismiss": True,
                "sound": "system_notification"
            }
        }
        
        self.notification_templates = {
            "new_daily_mission": {
                "type": "mission",
                "title": "New Daily Mission Available!",
                "message": "A new daily mission has been generated for you. Check it out!",
                "action": "view_missions",
                "data": {}
            },
            "new_weekly_mission": {
                "type": "mission",
                "title": "New Weekly Mission Available!",
                "message": "A challenging weekly mission awaits you. Can you complete it?",
                "action": "view_missions",
                "data": {}
            },
            "mission_completed": {
                "type": "reward",
                "title": "Mission Completed!",
                "message": "Congratulations! You've completed a mission and earned rewards!",
                "action": "claim_rewards",
                "data": {}
            },
            "level_up": {
                "type": "level_up",
                "title": "Level Up!",
                "message": "Congratulations! You've reached a new level!",
                "action": "view_profile",
                "data": {}
            },
            "vip_upgrade": {
                "type": "achievement",
                "title": "VIP Tier Upgraded!",
                "message": "You've been promoted to a higher VIP tier!",
                "action": "view_vip_benefits",
                "data": {}
            },
            "streak_milestone": {
                "type": "achievement",
                "title": "Login Streak Milestone!",
                "message": "You've reached a new login streak milestone!",
                "action": "view_streaks",
                "data": {}
            },
            "deer_hungry": {
                "type": "deer_care",
                "title": "Your Deer is Hungry!",
                "message": "Your deer companion needs to be fed soon.",
                "action": "feed_deer",
                "data": {}
            },
            "deer_entertainment": {
                "type": "deer_care",
                "title": "Deer Entertainment Time!",
                "message": "Your deer would love some entertainment and playtime.",
                "action": "entertain_deer",
                "data": {}
            },
            "empire_income_ready": {
                "type": "empire",
                "title": "Empire Income Ready!",
                "message": "Your empire facilities have generated income. Collect it now!",
                "action": "collect_income",
                "data": {}
            },
            "facility_upgrade_available": {
                "type": "empire",
                "title": "Facility Upgrade Available!",
                "message": "One of your facilities can be upgraded for better performance.",
                "action": "view_empire",
                "data": {}
            },
            "special_event_starting": {
                "type": "event",
                "title": "Special Event Starting!",
                "message": "A special event is about to begin. Don't miss out!",
                "action": "view_events",
                "data": {}
            },
            "receipt_verified": {
                "type": "reward",
                "title": "Receipt Verified!",
                "message": "Your receipt has been verified and coins have been added!",
                "action": "view_receipts",
                "data": {}
            },
            "suspicious_activity": {
                "type": "security",
                "title": "Security Alert",
                "message": "Suspicious activity detected. Please review your recent actions.",
                "action": "view_security",
                "data": {}
            },
            "friend_request": {
                "type": "system",
                "title": "New Friend Request",
                "message": "You have received a new friend request.",
                "action": "view_friends",
                "data": {}
            },
            "daily_login_reminder": {
                "type": "reminder",
                "title": "Daily Login Reminder",
                "message": "Don't forget to log in today to maintain your streak!",
                "action": "login",
                "data": {}
            }
        }
    
    def create_notification(self, user_id: str, template_key: str, custom_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new notification for a user"""
        try:
            if template_key not in self.notification_templates:
                return {"status": "error", "message": "Invalid notification template"}
            
            template = self.notification_templates[template_key]
            notification_type = self.notification_types[template["type"]]
            
            # Merge custom data with template data
            data = template["data"].copy()
            if custom_data:
                data.update(custom_data)
            
            notification = {
                "notification_id": f"notif_{user_id}_{int(time.time())}_{random.randint(1000, 9999)}",
                "user_id": user_id,
                "type": template["type"],
                "title": template["title"],
                "message": template["message"],
                "action": template["action"],
                "data": data,
                "priority": notification_type["priority"],
                "icon": notification_type["icon"],
                "color": notification_type["color"],
                "auto_dismiss": notification_type["auto_dismiss"],
                "sound": notification_type["sound"],
                "read": False,
                "dismissed": False,
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(days=7)).isoformat()  # Notifications expire after 7 days
            }
            
            # Save to database
            if DATABASE_AVAILABLE:
                db.save_notification(notification)
            else:
                # Fallback to memory storage
                if not hasattr(self, 'notification_storage'):
                    self.notification_storage = {}
                if user_id not in self.notification_storage:
                    self.notification_storage[user_id] = []
                self.notification_storage[user_id].append(notification)
            
            print(f"📢 Created {template['type']} notification for {user_id}: {template['title']}")
            return {"status": "success", "notification": notification}
            
        except Exception as e:
            return {"status": "error", "message": f"Error creating notification: {str(e)}"}
    
    def get_user_notifications(self, user_id: str, include_read: bool = False, limit: int = 50) -> Dict[str, Any]:
        """Get notifications for a user"""
        try:
            if DATABASE_AVAILABLE:
                notifications = db.get_user_notifications(user_id, include_read, limit)
            else:
                # Fallback to memory storage
                if hasattr(self, 'notification_storage') and user_id in self.notification_storage:
                    notifications = self.notification_storage[user_id]
                    if not include_read:
                        notifications = [n for n in notifications if not n["read"]]
                    notifications = sorted(notifications, key=lambda x: x["created_at"], reverse=True)[:limit]
                else:
                    notifications = []
            
            # Count by priority
            priority_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
            unread_count = 0
            
            for notification in notifications:
                priority_counts[notification["priority"]] += 1
                if not notification["read"]:
                    unread_count += 1
            
            return {
                "status": "success",
                "notifications": notifications,
                "unread_count": unread_count,
                "priority_counts": priority_counts,
                "total_count": len(notifications)
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error getting notifications: {str(e)}"}
    
    def mark_as_read(self, user_id: str, notification_id: str) -> Dict[str, Any]:
        """Mark a notification as read"""
        try:
            if DATABASE_AVAILABLE:
                success = db.mark_notification_read(notification_id)
            else:
                # Fallback to memory storage
                success = False
                if hasattr(self, 'notification_storage') and user_id in self.notification_storage:
                    for notification in self.notification_storage[user_id]:
                        if notification["notification_id"] == notification_id:
                            notification["read"] = True
                            success = True
                            break
            
            if success:
                print(f"📖 Marked notification {notification_id} as read")
                return {"status": "success", "message": "Notification marked as read"}
            else:
                return {"status": "error", "message": "Notification not found"}
                
        except Exception as e:
            return {"status": "error", "message": f"Error marking notification as read: {str(e)}"}
    
    def dismiss_notification(self, user_id: str, notification_id: str) -> Dict[str, Any]:
        """Dismiss a notification"""
        try:
            if DATABASE_AVAILABLE:
                success = db.dismiss_notification(notification_id)
            else:
                # Fallback to memory storage
                success = False
                if hasattr(self, 'notification_storage') and user_id in self.notification_storage:
                    for notification in self.notification_storage[user_id]:
                        if notification["notification_id"] == notification_id:
                            notification["dismissed"] = True
                            success = True
                            break
            
            if success:
                print(f"❌ Dismissed notification {notification_id}")
                return {"status": "success", "message": "Notification dismissed"}
            else:
                return {"status": "error", "message": "Notification not found"}
                
        except Exception as e:
            return {"status": "error", "message": f"Error dismissing notification: {str(e)}"}
    
    def mark_all_as_read(self, user_id: str) -> Dict[str, Any]:
        """Mark all notifications as read for a user"""
        try:
            if DATABASE_AVAILABLE:
                count = db.mark_all_notifications_read(user_id)
            else:
                # Fallback to memory storage
                count = 0
                if hasattr(self, 'notification_storage') and user_id in self.notification_storage:
                    for notification in self.notification_storage[user_id]:
                        if not notification["read"]:
                            notification["read"] = True
                            count += 1
            
            print(f"📖 Marked {count} notifications as read for {user_id}")
            return {"status": "success", "count": count, "message": f"Marked {count} notifications as read"}
            
        except Exception as e:
            return {"status": "error", "message": f"Error marking notifications as read: {str(e)}"}
    
    def clear_expired_notifications(self) -> Dict[str, Any]:
        """Clear expired notifications from the system"""
        try:
            now = datetime.now()
            cleared_count = 0
            
            if DATABASE_AVAILABLE:
                cleared_count = db.clear_expired_notifications(now.isoformat())
            else:
                # Fallback to memory storage
                if hasattr(self, 'notification_storage'):
                    for user_id in list(self.notification_storage.keys()):
                        original_count = len(self.notification_storage[user_id])
                        self.notification_storage[user_id] = [
                            n for n in self.notification_storage[user_id]
                            if datetime.fromisoformat(n["expires_at"]) > now
                        ]
                        cleared_count += original_count - len(self.notification_storage[user_id])
            
            print(f"🗑️ Cleared {cleared_count} expired notifications")
            return {"status": "success", "cleared_count": cleared_count}
            
        except Exception as e:
            return {"status": "error", "message": f"Error clearing expired notifications: {str(e)}"}
    
    def create_custom_notification(self, user_id: str, notification_type: str, title: str, message: str, 
                                 action: str = None, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a custom notification with user-defined content"""
        try:
            if notification_type not in self.notification_types:
                return {"status": "error", "message": "Invalid notification type"}
            
            notification_type_info = self.notification_types[notification_type]
            
            notification = {
                "notification_id": f"notif_{user_id}_{int(time.time())}_{random.randint(1000, 9999)}",
                "user_id": user_id,
                "type": notification_type,
                "title": title,
                "message": message,
                "action": action,
                "data": data or {},
                "priority": notification_type_info["priority"],
                "icon": notification_type_info["icon"],
                "color": notification_type_info["color"],
                "auto_dismiss": notification_type_info["auto_dismiss"],
                "sound": notification_type_info["sound"],
                "read": False,
                "dismissed": False,
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(days=7)).isoformat()
            }
            
            # Save to database
            if DATABASE_AVAILABLE:
                db.save_notification(notification)
            else:
                # Fallback to memory storage
                if not hasattr(self, 'notification_storage'):
                    self.notification_storage = {}
                if user_id not in self.notification_storage:
                    self.notification_storage[user_id] = []
                self.notification_storage[user_id].append(notification)
            
            print(f"📢 Created custom {notification_type} notification for {user_id}: {title}")
            return {"status": "success", "notification": notification}
            
        except Exception as e:
            return {"status": "error", "message": f"Error creating custom notification: {str(e)}"}
    
    def get_notification_settings(self, user_id: str) -> Dict[str, Any]:
        """Get user's notification preferences"""
        try:
            # Default settings
            default_settings = {
                "enabled": True,
                "sound_enabled": True,
                "vibration_enabled": True,
                "types": {
                    "mission": True,
                    "reward": True,
                    "level_up": True,
                    "event": True,
                    "reminder": True,
                    "achievement": True,
                    "deer_care": True,
                    "empire": True,
                    "security": True,
                    "system": False
                },
                "quiet_hours": {
                    "enabled": False,
                    "start": "22:00",
                    "end": "08:00"
                }
            }
            
            if DATABASE_AVAILABLE:
                settings = db.get_notification_settings(user_id)
                if not settings:
                    settings = default_settings
            else:
                # Fallback to memory storage
                if hasattr(self, 'settings_storage') and user_id in self.settings_storage:
                    settings = self.settings_storage[user_id]
                else:
                    settings = default_settings
            
            return {"status": "success", "settings": settings}
            
        except Exception as e:
            return {"status": "error", "message": f"Error getting notification settings: {str(e)}"}
    
    def update_notification_settings(self, user_id: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Update user's notification preferences"""
        try:
            if DATABASE_AVAILABLE:
                success = db.update_notification_settings(user_id, settings)
            else:
                # Fallback to memory storage
                if not hasattr(self, 'settings_storage'):
                    self.settings_storage = {}
                self.settings_storage[user_id] = settings
                success = True
            
            if success:
                print(f"⚙️ Updated notification settings for {user_id}")
                return {"status": "success", "message": "Notification settings updated"}
            else:
                return {"status": "error", "message": "Failed to update notification settings"}
                
        except Exception as e:
            return {"status": "error", "message": f"Error updating notification settings: {str(e)}"}
    
    def get_notification_statistics(self, user_id: str) -> Dict[str, Any]:
        """Get notification statistics for a user"""
        try:
            if DATABASE_AVAILABLE:
                stats = db.get_notification_statistics(user_id)
            else:
                # Fallback to memory storage
                stats = {
                    "total_notifications": 0,
                    "read_notifications": 0,
                    "dismissed_notifications": 0,
                    "notifications_by_type": {},
                    "notifications_by_priority": {"critical": 0, "high": 0, "medium": 0, "low": 0}
                }
                
                if hasattr(self, 'notification_storage') and user_id in self.notification_storage:
                    notifications = self.notification_storage[user_id]
                    stats["total_notifications"] = len(notifications)
                    stats["read_notifications"] = sum(1 for n in notifications if n["read"])
                    stats["dismissed_notifications"] = sum(1 for n in notifications if n["dismissed"])
                    
                    # Count by type
                    for notification in notifications:
                        notif_type = notification["type"]
                        stats["notifications_by_type"][notif_type] = stats["notifications_by_type"].get(notif_type, 0) + 1
                        stats["notifications_by_priority"][notification["priority"]] += 1
            
            return {"status": "success", "statistics": stats}
            
        except Exception as e:
            return {"status": "error", "message": f"Error getting notification statistics: {str(e)}"}

# Initialize database availability
try:
    from database import db
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    print("[NOTIFICATION SYSTEM] Database module not available, using in-memory storage")

# Create global instance
notification_system = NotificationSystem() 