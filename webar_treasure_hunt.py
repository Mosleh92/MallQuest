"""WebAR Treasure Hunt module for MallQuest.

Provides AR box generation, animation hooks, sound triggers,
user participation tracking with daily limits.
"""
from datetime import datetime
import random
import uuid


class WebARTreasureHunt:
    """Manage WebAR treasure hunt interactions."""

    def __init__(self, daily_limit: int = 3):
        self.daily_limit = daily_limit
        self.participation_log = {}

    def _get_log(self, user_id: str):
        today = datetime.now().date()
        log = self.participation_log.get(user_id)
        if not log or log["date"] != today:
            log = {"date": today, "count": 0}
            self.participation_log[user_id] = log
        return log

    def can_participate(self, user_id: str) -> bool:
        """Check if the user can participate today."""
        log = self._get_log(user_id)
        return log["count"] < self.daily_limit

    def generate_ar_box(self):
        """Generate AR box coordinates and ID."""
        return {
            "box_id": str(uuid.uuid4()),
            "position": {
                "x": random.uniform(-1.0, 1.0),
                "y": random.uniform(-1.0, 1.0),
                "z": random.uniform(-1.0, 1.0),
            },
        }

    def trigger_animation(self, box_id: str):
        """Hook for AR animation when box appears."""
        return {"animation": "spawn_box", "box_id": box_id}

    def play_sound(self, sound: str):
        """Hook for playing sounds in the UI."""
        return {"sound": sound}

    def participate(self, user_id: str):
        """Attempt to participate in the treasure hunt."""
        log = self._get_log(user_id)
        if log["count"] >= self.daily_limit:
            return {"status": "limit_reached", "message": "Daily limit reached"}

        log["count"] += 1
        box = self.generate_ar_box()
        self.trigger_animation(box["box_id"])
        self.play_sound("treasure_open")
        coins = random.randint(5, 20)
        return {"status": "success", "coins": coins, "box": box}
