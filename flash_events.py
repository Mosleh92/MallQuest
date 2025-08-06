from __future__ import annotations

"""Flash event management for time-bound events and AR zone definitions.

This module provides classes to manage AR zones and flash events that are
active only for limited periods of time. It also tracks participant progress
within these events.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Tuple, Optional


@dataclass
class ARZone:
    """Definition for an augmented reality zone within the mall."""

    name: str
    coordinates: Tuple[float, float]
    radius: float


@dataclass
class FlashEvent:
    """Represents a time-bound event tied to one or more AR zones."""

    name: str
    start: datetime
    end: datetime
    zones: List[str]
    multiplier: float = 1.0
    active: bool = False
    participants: Dict[str, int] = field(default_factory=dict)


class FlashEventManager:
    """Manage flash events and AR zones."""

    def __init__(self) -> None:
        self.events: Dict[str, FlashEvent] = {}
        self.zones: Dict[str, ARZone] = {}

    # --- AR Zone Management -------------------------------------------------
    def define_zone(self, zone_id: str, coordinates: Tuple[float, float], radius: float) -> None:
        """Define or update an AR zone."""
        self.zones[zone_id] = ARZone(zone_id, coordinates, radius)

    # --- Event Scheduling ---------------------------------------------------
    def schedule_event(
        self,
        name: str,
        start: datetime,
        end: datetime,
        zone_ids: List[str],
        multiplier: float = 1.0,
    ) -> None:
        """Schedule a new flash event."""
        self.events[name] = FlashEvent(name, start, end, zone_ids, multiplier)

    # --- Activation Logic ---------------------------------------------------
    def activate_events(self, current_time: Optional[datetime] = None) -> List[FlashEvent]:
        """Activate or deactivate events based on the current time.

        Returns a list of currently active events.
        """
        now = current_time or datetime.now()
        active: List[FlashEvent] = []
        for event in self.events.values():
            event.active = event.start <= now <= event.end
            if event.active:
                active.append(event)
        return active

    def deactivate_event(self, name: str) -> None:
        """Forcefully deactivate an event."""
        if name in self.events:
            self.events[name].active = False

    # --- Participant Tracking ----------------------------------------------
    def record_participation(self, event_name: str, participant_id: str, progress: int = 1) -> bool:
        """Record progress for a participant in an active event."""
        event = self.events.get(event_name)
        if event and event.active:
            event.participants[participant_id] = event.participants.get(participant_id, 0) + progress
            return True
        return False

    def get_participant_progress(self, event_name: str, participant_id: str) -> int:
        """Retrieve a participant's progress for a specific event."""
        event = self.events.get(event_name)
        if not event:
            return 0
        return event.participants.get(participant_id, 0)


class FlashEventAdminInterface:
    """Simple administrative interface for managing flash events and zones."""

    def __init__(self, manager: FlashEventManager) -> None:
        self.manager = manager

    def define_zone(self, zone_id: str, coordinates: Tuple[float, float], radius: float) -> None:
        self.manager.define_zone(zone_id, coordinates, radius)

    def schedule_event(
        self,
        name: str,
        start: datetime,
        end: datetime,
        zone_ids: List[str],
        multiplier: float = 1.0,
    ) -> None:
        self.manager.schedule_event(name, start, end, zone_ids, multiplier)
