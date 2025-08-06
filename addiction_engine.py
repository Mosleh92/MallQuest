"""Behavioural addiction utilities."""

from __future__ import annotations

import random
from typing import Dict


class AddictionEngine:
    """Simplified variable reward and reminder system."""

    def dopamine_schedule(self, user_id: str) -> int:
        """Return a random reward amount."""
        return random.choice([5, 10, 20, 100, 5000])

    def withdrawal_prevention(self, user_id: str) -> str:
        return "Your friends are waiting! Special challenge activated."

    def tolerance_building(self, user_id: str, current_level: int) -> Dict[str, int]:
        return {"required_spend": current_level * 2}
