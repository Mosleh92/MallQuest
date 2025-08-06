from datetime import datetime
import uuid


class CoinDuelManager:
    """Manage coin duel matchmaking and scoring."""

    def __init__(self, mall_system):
        self.mall_system = mall_system
        self.active_duels = {}

    def start_duel(self, challenger_id: str, opponent_id: str) -> str:
        """Create a new duel between two users and return duel ID."""
        duel_id = str(uuid.uuid4())
        self.active_duels[duel_id] = {
            'players': [challenger_id, opponent_id],
            'scores': {challenger_id: 0, opponent_id: 0},
            'start_time': datetime.utcnow()
        }
        self.mall_system.log_event('coin_duel_started', {
            'duel_id': duel_id,
            'players': [challenger_id, opponent_id]
        })
        return duel_id

    def update_score(self, duel_id: str, user_id: str, score: int) -> bool:
        """Update score for a player in an active duel."""
        duel = self.active_duels.get(duel_id)
        if not duel or user_id not in duel['players']:
            return False
        duel['scores'][user_id] = score
        return True

    def conclude_duel(self, duel_id: str):
        """Finish duel, determine winner, allocate rewards, and log event."""
        duel = self.active_duels.pop(duel_id, None)
        if not duel:
            return None
        scores = duel['scores']
        winner_id = max(scores, key=scores.get)
        loser_id = min(scores, key=scores.get)
        self.mall_system.handle_coin_duel_result(duel_id, winner_id, loser_id, scores)
        return {'duel_id': duel_id, 'winner': winner_id, 'scores': scores}

    def get_duel(self, duel_id: str):
        """Retrieve duel information."""
        return self.active_duels.get(duel_id)

    def get_user_duels(self, user_id: str):
        """Return active duels involving the specified user."""
        result = []
        for d_id, duel in self.active_duels.items():
            if user_id in duel['players']:
                result.append({'duel_id': d_id, **duel})
        return result
