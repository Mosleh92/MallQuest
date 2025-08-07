"""In-memory game state and helpers for MallQuest."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import math


@dataclass
class Player:
    """Simple player state."""

    player_id: str
    position: Tuple[float, float] = (0.0, 0.0)
    coins: int = 0


@dataclass
class Battle:
    """Basic battle representation."""

    battle_id: str
    players: List[str] = field(default_factory=list)


# Global state containers
players: Dict[str, Player] = {}
coins: Dict[int, Tuple[float, float]] = {
    1: (0.0, 0.0),
    2: (5.0, 5.0),
    3: (-3.0, 7.0),
}
battles: Dict[str, Battle] = {}
quests: List[Dict[str, str]] = [
    {"id": "collect_3", "name": "Collect 3 coins"},
    {"id": "first_battle", "name": "Join your first battle"},
]


def update_location(player_id: str, x: float, y: float) -> Player:
    """Update or create a player's location."""

    player = players.setdefault(player_id, Player(player_id))
    player.position = (x, y)
    return player


def get_nearby_coins(x: float, y: float, radius: float = 10.0) -> List[Dict[str, float]]:
    """Return coins within ``radius`` of a point."""

    results: List[Dict[str, float]] = []
    for coin_id, (cx, cy) in coins.items():
        if math.hypot(cx - x, cy - y) <= radius:
            results.append({"id": coin_id, "x": cx, "y": cy})
    return results


def collect_coin(player_id: str, coin_id: int) -> bool:
    """Collect a coin if it exists."""

    if coin_id not in coins:
        return False
    players.setdefault(player_id, Player(player_id)).coins += 1
    del coins[coin_id]
    return True


def join_battle(player_id: str, battle_id: str = "default") -> Battle:
    """Add ``player_id`` to a battle and return it."""

    battle = battles.setdefault(battle_id, Battle(battle_id))
    if player_id not in battle.players:
        battle.players.append(player_id)
    return battle


def list_quests() -> List[Dict[str, str]]:
    """Return available quests."""

    return quests


def campaign_list() -> List[Dict[str, str]]:
    """Return a static list of CRM campaigns."""

    return [
        {"id": "summer", "name": "Summer Sale", "active": True},
        {"id": "loyalty", "name": "Loyalty Bonus", "active": False},
    ]


def analytics_summary() -> Dict[str, int]:
    """Return simple analytics based on the in-memory state."""

    return {
        "players": len(players),
        "coins_collected": sum(p.coins for p in players.values()),
        "active_battles": len(battles),
    }
