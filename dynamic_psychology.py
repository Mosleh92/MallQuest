"""Psychological pricing utilities."""

from __future__ import annotations

from typing import Dict


class PsychologicalPricing:
    """Provide pricing tricks such as FOMO and scarcity."""

    def fomo_pricing(self, user_id: str, item_id: str) -> Dict[str, str]:
        return {"item": item_id, "message": "Limited-time price just for you!"}

    def social_proof_pricing(self) -> Dict[str, str]:
        return {"message": "Many of your friends bought this today"}

    def scarcity_engine(self) -> Dict[str, str]:
        return {"message": "Only a few items left in stock"}
