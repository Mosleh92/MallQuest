"""Service for recording mall presence via Wi-Fi or GPS events."""

from __future__ import annotations

from typing import Any, Dict

from database import MallDatabase


class PresenceService:
    """Capture Wi-Fi/GPS events and store them in the database."""

    def __init__(self, db: MallDatabase):
        self.db = db

    def capture_wifi_event(
        self,
        user_id: str,
        location: str,
        device_info: Dict[str, Any],
        coords: Dict[str, float],
    ) -> bool:
        """Record a Wi-Fi based presence event."""

        return self.db.log_mall_entry(user_id, location, device_info, coords)

    def capture_gps_event(
        self,
        user_id: str,
        coords: Dict[str, float],
        device_info: Dict[str, Any],
    ) -> bool:
        """Record a GPS based presence event."""

        location = "GPS"
        return self.db.log_mall_entry(user_id, location, device_info, coords)

