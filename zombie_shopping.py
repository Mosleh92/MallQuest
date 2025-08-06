"""Zombie shopping apocalypse events."""

from __future__ import annotations

from typing import List, Dict


class ZombieMode:
    """Provide tasks for zombie apocalypse mode."""

    def start_apocalypse(self) -> str:
        return "Zombies have invaded the mall! Find supplies to survive."

    def survival_challenges(self, players: List[str]) -> Dict[str, str]:
        tasks = {
            "energy-bars": "Buy 10 energy bars",
            "home-goods": "Purchase items to build a shelter",
        }
        return {player: tasks for player in players}
