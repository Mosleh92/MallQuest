"""Simplified Mall Olympics events."""

from __future__ import annotations

import random
from typing import Dict, List


class MallOlympics:
    """Provide simple competition mechanics."""

    def speed_shopping_race(self, participants: List[str]) -> str:
        return random.choice(participants)

    def bargain_hunting_championship(self, participants: List[str]) -> str:
        return random.choice(participants)

    def fashion_design_contest(self, participants: List[str]) -> str:
        return random.choice(participants)

    def team_synchronization(self, teams: Dict[str, List[str]]) -> str:
        return random.choice(list(teams.keys()))
