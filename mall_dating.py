"""Mall style dating helpers."""

from __future__ import annotations

import random
from typing import Dict, List, Tuple


class MallDating:
    """Provide simple matching and date challenges."""

    def style_matching(self, user_id: str, preferences: List[str]) -> Tuple[str, int]:
        match = random.choice(preferences) if preferences else "casual"
        score = random.randint(0, 100)
        return match, score

    def shopping_dates(self, user1: str, user2: str, budget: int) -> Dict[str, int]:
        each_budget = budget // 2
        return {user1: each_budget, user2: each_budget}

    def couple_rewards(self, couple_id: str) -> Dict[str, str]:
        return {"reward": "Couple discount activated", "couple_id": couple_id}
