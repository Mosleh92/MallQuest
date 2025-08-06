"""Simplified real-time betting system for MallQuest."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Bet:
    """Dataclass representing a single bet room."""

    bet_id: str
    creator_id: str
    bet_type: str
    stake_coins: int
    participants: List[str] = field(default_factory=list)
    predictions: Dict[str, str] = field(default_factory=dict)
    resolved: bool = False
    winner_id: Optional[str] = None


class BettingSystem:
    """In-memory betting system used for demonstration purposes."""

    def __init__(self) -> None:
        self._bets: Dict[str, Bet] = {}
        self._balance: Dict[str, int] = {}

    def create_bet_room(self, creator_id: str, bet_type: str, stake_coins: int) -> Bet:
        """Create a new bet room and deduct the stake from the creator."""
        self._balance.setdefault(creator_id, 0)
        if self._balance[creator_id] < stake_coins:
            raise ValueError("Insufficient coins to create bet")
        self._balance[creator_id] -= stake_coins
        bet_id = f"bet-{len(self._bets) + 1}"
        bet = Bet(bet_id=bet_id, creator_id=creator_id, bet_type=bet_type, stake_coins=stake_coins)
        bet.participants.append(creator_id)
        self._bets[bet_id] = bet
        return bet

    def join_bet(self, user_id: str, bet_id: str, prediction: str) -> None:
        """Join an existing bet room with a prediction."""
        if bet_id not in self._bets:
            raise KeyError("Bet not found")
        bet = self._bets[bet_id]
        self._balance.setdefault(user_id, 0)
        if self._balance[user_id] < bet.stake_coins:
            raise ValueError("Insufficient coins to join bet")
        if bet.resolved:
            raise RuntimeError("Bet already resolved")
        self._balance[user_id] -= bet.stake_coins
        bet.participants.append(user_id)
        bet.predictions[user_id] = prediction

    def resolve_bet(self, bet_id: str, actual_result: str) -> Optional[str]:
        """Resolve the bet and distribute winnings equally among winners."""
        if bet_id not in self._bets:
            raise KeyError("Bet not found")
        bet = self._bets[bet_id]
        if bet.resolved:
            return bet.winner_id
        winners = [uid for uid, pred in bet.predictions.items() if pred == actual_result]
        pot = bet.stake_coins * len(bet.participants)
        if winners:
            reward = pot // len(winners)
            for uid in winners:
                self._balance[uid] = self._balance.get(uid, 0) + reward
            bet.winner_id = winners[0] if len(winners) == 1 else None
        else:
            # refund everyone if no one predicted correctly
            for uid in bet.participants:
                self._balance[uid] = self._balance.get(uid, 0) + bet.stake_coins
        bet.resolved = True
        return bet.winner_id

    # Utility methods for tests/demonstration
    def add_coins(self, user_id: str, amount: int) -> None:
        self._balance[user_id] = self._balance.get(user_id, 0) + amount

    def get_balance(self, user_id: str) -> int:
        return self._balance.get(user_id, 0)
