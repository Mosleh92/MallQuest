"""Social credit tracking."""

from __future__ import annotations

from typing import Dict


class SocialCreditSystem:
    """Track user behaviour and compute a social credit score."""

    def __init__(self) -> None:
        self.scores: Dict[str, int] = {}

    def track_behavior(self, user_id: str, positive: bool) -> int:
        """Adjust score for positive or negative behaviour."""
        delta = 5 if positive else -5
        self.scores[user_id] = self.scores.get(user_id, 100) + delta
        return self.scores[user_id]

    def credit_based_rewards(self, user_id: str) -> Dict[str, str]:
        score = self.scores.get(user_id, 100)
        if score >= 120:
            return {"discount": "10%"}
        if score < 80:
            return {"restriction": "Limited access"}
        return {}
