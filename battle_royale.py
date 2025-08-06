"""Simplified shopping battle royale implementation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class BattleState:
    """State for a single battle royale match."""

    game_id: str
    participants: List[str]
    active_players: List[str] = field(default_factory=list)
    eliminated: List[str] = field(default_factory=list)
    prize_pool: int = 0
    finished: bool = False
    winner: Optional[str] = None


class ShoppingBattleRoyale:
    """Simplified in-memory battle royale system."""

    def __init__(self) -> None:
        self._games: Dict[str, BattleState] = {}
        self._balances: Dict[str, int] = {}

    def start_battle(self, participants_list: List[str]) -> BattleState:
        """Start a new battle with up to 20 participants."""
        if len(participants_list) != 20:
            raise ValueError("Battle requires exactly 20 participants")
        game_id = f"battle-{len(self._games) + 1}"
        self._games[game_id] = BattleState(
            game_id=game_id,
            participants=participants_list[:],
            active_players=participants_list[:],
            prize_pool=5000,
        )
        return self._games[game_id]

    def eliminate_slowest(self, game_id: str, challenge_results: Dict[str, int]) -> None:
        """Eliminate the slowest players based on completion time."""
        game = self._games[game_id]
        if game.finished:
            return
        # sort by time ascending; remove last 5
        ranked = sorted(game.active_players, key=lambda u: challenge_results.get(u, float('inf')))
        survivors = ranked[:-5]
        eliminated = ranked[-5:]
        game.active_players = survivors
        game.eliminated.extend(eliminated)
        if len(game.active_players) == 1:
            game.finished = True
            game.winner = game.active_players[0]
            winner = game.winner
            self._balances[winner] = self._balances.get(winner, 0) + game.prize_pool

    # Utility methods
    def get_balance(self, user_id: str) -> int:
        return self._balances.get(user_id, 0)
