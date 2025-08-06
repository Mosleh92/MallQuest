"""AI personal shopper utilities."""

from __future__ import annotations

import random
from typing import Dict, List


class AIPersonalShopper:
    """Provide basic AI-powered shopping suggestions."""

    def analyze_style(self, user_id: str, previous_purchases: List[str]) -> Dict[str, int]:
        """Return frequency count of purchased items."""
        style = {}
        for item in previous_purchases:
            style[item] = style.get(item, 0) + 1
        return style

    def suggest_combos(self, budget: int, occasion: str) -> Dict[str, int]:
        """Suggest a simple outfit combination within a budget."""
        items = {
            "shoes": random.randint(50, 200),
            "bag": random.randint(50, 200),
            "top": random.randint(50, 200),
        }
        total = sum(items.values())
        if total > budget:
            scale = budget / total
            for key in items:
                items[key] = int(items[key] * scale)
        return items

    def style_challenge(self, user1: str, user2: str) -> Dict[str, str]:
        """Propose two different styles for a challenge."""
        styles = ["sporty", "casual", "formal", "luxury"]
        return {user1: random.choice(styles), user2: random.choice(styles)}
