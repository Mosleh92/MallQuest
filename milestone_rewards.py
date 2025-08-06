"""Milestone reward tracking and claiming logic.

This module provides a small utility class that keeps track of user
progress towards predefined milestones.  The class can work purely in
memory or persist progress in a SQLite database so that reward state is
maintained across application restarts.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set
import sqlite3
import json


class MilestoneRewards:
    """Track player progress and allow claiming of milestone rewards.

    Parameters
    ----------
    db_path:
        Optional path to a SQLite database file used to persist user
        progress. When ``None`` (the default) all information is kept in
        memory only.
    """

    def __init__(self, db_path: Optional[str] = None) -> None:
        # Predefined milestone tiers
        self.milestones: List[Dict] = [
            {"id": "bronze", "threshold": 100, "reward": {"coins": 50}},
            {"id": "silver", "threshold": 500, "reward": {"coins": 300}},
            {"id": "gold", "threshold": 1000, "reward": {"coins": 800}},
        ]

        self.conn: Optional[sqlite3.Connection] = None
        if db_path:
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS milestone_progress (
                    user_id TEXT PRIMARY KEY,
                    progress INTEGER NOT NULL,
                    claimed TEXT NOT NULL
                )
                """
            )
            self.conn.commit()
            self.user_progress = None  # type: ignore[assignment]
        else:
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

        data = self._get_user_data(user_id)
        if progress > data["progress"]:
            data["progress"] = progress
            self._save_user_data(user_id, data)

    def get_available_milestones(self, user_id: str) -> List[Dict]:
        """Return milestones achieved but not yet claimed."""

        data = self._get_user_data(user_id)
        available: List[Dict] = []
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
        otherwise returns ``None``.
        """

        data = self._get_user_data(user_id)
        for milestone in self.milestones:
            if milestone["id"] == milestone_id:
                if data["progress"] >= milestone["threshold"] and milestone_id not in data["claimed"]:
                    data["claimed"].add(milestone_id)
                    self._save_user_data(user_id, data)
                    return milestone["reward"]
                break
        return None

    # ------------------------------------------------------------
    # Internal helpers for persistence
    # ------------------------------------------------------------
    def _get_user_data(self, user_id: str) -> Dict[str, Set[str]]:
        """Fetch or initialise stored progress for ``user_id``."""

        if self.conn:
            cur = self.conn.execute(
                "SELECT progress, claimed FROM milestone_progress WHERE user_id = ?",
                (user_id,),
            )
            row = cur.fetchone()
            if row:
                claimed = set(json.loads(row[1])) if row[1] else set()
                return {"progress": row[0], "claimed": claimed}

            data = {"progress": 0, "claimed": set()}
            self._save_user_data(user_id, data)
            return data

        # In-memory fallback
        return self.user_progress.setdefault(user_id, {"progress": 0, "claimed": set()})

    def _save_user_data(self, user_id: str, data: Dict) -> None:
        """Persist user milestone data."""

        if self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO milestone_progress (user_id, progress, claimed) VALUES (?, ?, ?)",
                (user_id, data["progress"], json.dumps(list(data["claimed"]))),
            )
            self.conn.commit()
        else:
            self.user_progress[user_id] = data

