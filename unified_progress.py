"""Utilities for tracking player progress across MallQuest games.

This module introduces a lightweight ``UnifiedProgress`` dataclass that
combines coin management via :class:`MallCoin` with experience points and
achievements.  It does not replace the existing user model but provides a
simple container that future game modules can share.
"""

from dataclasses import dataclass, field
from typing import Dict

from mallcoin import MallCoin


@dataclass
class UnifiedProgress:
    """Aggregate progress container used by multiple games."""

    coins: MallCoin = field(default_factory=MallCoin)
    xp: int = 0
    achievements: Dict[str, int] = field(default_factory=dict)

    def award(self, coins: int = 0, xp: int = 0) -> None:
        """Grant coins and experience points to the player."""
        self.coins.add(coins)
        if xp > 0:
            self.xp += int(xp)

    def add_achievement(self, name: str) -> None:
        """Record a named achievement.

        Achievements are counted so repeated awards can be tracked.
        """
        self.achievements[name] = self.achievements.get(name, 0) + 1
