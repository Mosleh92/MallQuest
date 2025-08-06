from typing import Dict, List, Optional

class MilestoneRewards:
    """Simple milestone reward tracker using in-memory storage.

    Milestones are defined by a progress threshold and a reward. The
    progress value is typically the player's total XP but can represent
    any cumulative metric.
    """

    def __init__(self) -> None:
        # Predefined milestone tiers
        self.milestones: List[Dict] = [
            {"id": "bronze", "threshold": 100, "reward": {"coins": 50}},
            {"id": "silver", "threshold": 500, "reward": {"coins": 300}},
            {"id": "gold", "threshold": 1000, "reward": {"coins": 800}},
        ]

        # user_id -> {"progress": int, "claimed": set(str)}
        self.user_progress: Dict[str, Dict] = {}

    # ------------------------------------------------------------
    # Progress management
    # ------------------------------------------------------------
    def update_progress(self, user_id: str, progress: int) -> None:
        """Update stored progress for a user.

        The highest progress seen for the user is stored. This method can be
        called whenever the user's XP or relevant metric changes.
        """
        data = self.user_progress.setdefault(user_id, {"progress": 0, "claimed": set()})
        if progress > data["progress"]:
            data["progress"] = progress

    def get_available_milestones(self, user_id: str) -> List[Dict]:
        """Return milestones achieved but not yet claimed."""
        data = self.user_progress.get(user_id, {"progress": 0, "claimed": set()})
        available = []
        for milestone in self.milestones:
            if data["progress"] >= milestone["threshold"] and milestone["id"] not in data["claimed"]:
                available.append(milestone)
        return available

    # ------------------------------------------------------------
    # Claim logic
    # ------------------------------------------------------------
    def claim_milestone(self, user_id: str, milestone_id: str) -> Optional[Dict]:
        """Claim a milestone reward for the user.

        Returns the reward dict if the milestone is valid and unclaimed,
        otherwise returns None.
        """
        data = self.user_progress.setdefault(user_id, {"progress": 0, "claimed": set()})

        for milestone in self.milestones:
            if milestone["id"] == milestone_id:
                if data["progress"] >= milestone["threshold"] and milestone_id not in data["claimed"]:
                    data["claimed"].add(milestone_id)
                    return milestone["reward"]
                break
        return None

