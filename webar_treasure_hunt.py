"""WebAR Treasure Hunt utilities.

The module provides basic hooks for an AR-based mini game including
randomised box generation, simple animation/sound triggers and per-user
participation limits.  The implementation is intentionally lightweight so it
can be used in tests or environments without a full AR stack.
"""

from __future__ import annotations

from datetime import datetime
import random
import uuid
from typing import Dict, Optional


class WebARTreasureHunt:
    """Manage WebAR treasure hunt interactions."""

    def __init__(self, daily_limit: int = 3) -> None:
        #: Maximum number of attempts allowed per user per day
        self.daily_limit = daily_limit
        #: Simple in-memory log of user participation
        self.participation_log: Dict[str, Dict[str, int | datetime]] = {}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _get_log(self, user_id: str) -> Dict[str, int | datetime]:
        """Return (and initialise) today's participation log for ``user_id``."""

        today = datetime.now().date()
        log = self.participation_log.get(user_id)
        if not log or log["date"] != today:
            log = {"date": today, "count": 0}
            self.participation_log[user_id] = log
        return log

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def can_participate(self, user_id: str) -> bool:
        """Return ``True`` if the user still has attempts left today."""

        log = self._get_log(user_id)
        return log["count"] < self.daily_limit

    def get_remaining_attempts(self, user_id: str) -> int:
        """Return how many attempts the user has left for the day."""

        log = self._get_log(user_id)
        return max(0, self.daily_limit - log["count"])

    def generate_ar_box(self) -> Dict[str, object]:
        """Generate AR box coordinates and identifier."""

        return {
            "box_id": str(uuid.uuid4()),
            "position": {
                "x": random.uniform(-1.0, 1.0),
                "y": random.uniform(-1.0, 1.0),
                "z": random.uniform(-1.0, 1.0),
            },
        }

    def trigger_animation(self, box_id: str) -> Dict[str, str]:
        """Return payload describing an animation for the given ``box_id``."""

        return {"animation": "spawn_box", "box_id": box_id}

    def play_sound(self, sound: str) -> Dict[str, str]:
        """Return payload describing a sound to be played on the client."""

        return {"sound": sound}

    def participate(self, user_id: str) -> Dict[str, object]:
        """Attempt to participate in the treasure hunt.

        Returns a structure describing the outcome along with animation and
        sound payloads for the front-end to use.  If the user has exceeded the
        daily participation limit a ``limit_reached`` status is returned.
        """

        log = self._get_log(user_id)
        if log["count"] >= self.daily_limit:
            return {
                "status": "limit_reached",
                "message": "Daily limit reached",
                "remaining": 0,
            }

        log["count"] += 1
        box = self.generate_ar_box()
        animation = self.trigger_animation(box["box_id"])
        sound = self.play_sound("treasure_open")
        coins = random.randint(5, 20)
        return {
            "status": "success",
            "coins": coins,
            "box": box,
            "animation": animation,
            "sound": sound,
            "remaining": self.get_remaining_attempts(user_id),
        }

