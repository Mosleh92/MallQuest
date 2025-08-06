"""Simple seasonal events module."""

from __future__ import annotations

from datetime import datetime
from typing import Dict


class SeasonalEvents:
    """Provide descriptions for seasonal events."""

    def ramadan_special(self) -> Dict[str, str]:
        return {
            "name": "Ramadan Rush",
            "mission": "Buy something sweet before Iftar",
            "bonus_window": "18:00-20:00",
        }

    def national_day_celebration(self) -> Dict[str, str]:
        return {
            "name": "National Day Celebration",
            "mission": "Wear the UAE flag colours with a group",
            "reward": "Team coin bonus",
        }

    def black_friday_mayhem(self) -> Dict[str, str]:
        return {
            "name": "Black Friday Mayhem",
            "mission": "Hourly shopping challenges for 24h",
            "grand_prize": "Combined coin jackpot",
        }
