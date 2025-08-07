from datetime import datetime
import uuid


class DuelArena:
    """Manage multi-player coin duels where winner takes the pot."""

    def __init__(self, mall_system):
        self.mall_system = mall_system
        self.active_duels = {}

    def create_duel(self, player_ids, stake):
        """Create a duel with 2-4 players staking an equal amount of coins.

        Args:
            player_ids (list[str]): IDs of participating users.
            stake (int): Coins each user stakes.
        Returns:
            str: Unique duel identifier.
        """
        if not 2 <= len(player_ids) <= 4:
            raise ValueError("DuelArena requires 2-4 players")
        duel_id = str(uuid.uuid4())
        self.active_duels[duel_id] = {
            "players": list(player_ids),
            "stake": stake,
            "pot": stake * len(player_ids),
            "start_time": datetime.utcnow(),
        }
        self.mall_system.log_event(
            "duel_arena_started",
            {"duel_id": duel_id, "players": list(player_ids), "stake": stake},
        )
        return duel_id

    def conclude_duel(self, duel_id, winner_id):
        """Finish the duel and allocate the coin pot to the winner."""
        duel = self.active_duels.pop(duel_id, None)
        if not duel or winner_id not in duel["players"]:
            return None
        pot = duel["pot"]
        if hasattr(self.mall_system, "award_coins"):
            self.mall_system.award_coins(winner_id, pot)
        self.mall_system.log_event(
            "duel_arena_completed",
            {"duel_id": duel_id, "winner": winner_id, "pot": pot},
        )
        return {"duel_id": duel_id, "winner": winner_id, "pot": pot}

    def get_duel(self, duel_id):
        """Retrieve active duel information."""
        return self.active_duels.get(duel_id)
