"""Influence score calculation and rewards."""

from __future__ import annotations

from typing import Dict


class InfluenceSystem:
    """Compute a simple influence score."""

    def calculate_influence(self, user_id: str, followers: int, copied_styles: int, purchases_inspired: int) -> int:
        score = followers * 2 + copied_styles * 5 + purchases_inspired
        return score

    def influencer_rewards(self, user_id: str, influence_score: int) -> Dict[str, str]:
        rewards = {}
        if influence_score > 100:
            rewards["early_access"] = "Unlocked"
        if influence_score > 200:
            rewards["bonus_coins"] = "Awarded"
        return rewards
