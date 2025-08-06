#!/usr/bin/env python3
"""Social features module for MallQuest.

Provides a summary of the game's social capabilities including chat,
relationships, and sharing options.
"""
from typing import Dict


class SocialFeatures:
    """Defines available social features for players."""

    def complete_social_system(self) -> Dict[str, Dict[str, str]]:
        """Return a dictionary describing the game's social system."""
        return {
            "chat": {
                "team_chat": "Real-time team communication",
                "proximity_chat": "Location-based messaging",
                "voice_chat": "During battles only",
                "emotes": "Quick communication",
            },
            "social_graph": {
                "friends": "Add/invite system",
                "teams": "Persistent groups",
                "clans": "Larger organizations",
                "rivals": "Competition tracking",
            },
            "sharing": {
                "achievements": "Social media integration",
                "replays": "Battle highlights",
                "referrals": "Reward-based invites",
            },
        }
