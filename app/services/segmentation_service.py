"""User segmentation utilities."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import threading

from database import MallDatabase, User
from notification_system import NotificationSystem

# Cached segmentation data
SEGMENTATION_CACHE: Dict[str, List[Dict[str, Any]]] = {
    "active": [],
    "dormant": [],
    "lost": [],
}


def classify_user(
    last_entry_at: Optional[datetime], last_purchase_at: Optional[datetime]
) -> str:
    """Classify a user based on their last activity or purchase."""
    now = datetime.utcnow()
    timestamps = [t for t in [last_entry_at, last_purchase_at] if t]
    if not timestamps:
        return "lost"
    last_action = max(timestamps)
    delta = now - last_action
    if delta <= timedelta(days=30):
        return "active"
    if delta <= timedelta(days=90):
        return "dormant"
    return "lost"


def update_segmentation_cache(db: MallDatabase) -> None:
    """Rebuild the segmentation cache from the database and send reminders.

    Users classified as ``dormant`` or ``lost`` will receive a notification via
    :class:`NotificationSystem` encouraging them to return to the mall.
    """
    cache = {"active": [], "dormant": [], "lost": []}
    notifier = NotificationSystem()
    for session_factory in db.sessions:
        session = session_factory()
        try:
            for user in session.query(User).all():
                last_entry = getattr(user, "last_entry_at", None)
                last_purchase = getattr(user, "last_purchase_at", None)
                segment = classify_user(last_entry, last_purchase)
                data = {c.name: getattr(user, c.name) for c in user.__table__.columns}
                cache[segment].append(data)
                if segment in ("dormant", "lost"):
                    user_id = data.get("user_id")
                    if user_id:
                        threading.Thread(
                            target=notifier.create_notification,
                            args=(user_id, "daily_login_reminder"),
                            daemon=True,
                        ).start()
        finally:
            session.close()
    global SEGMENTATION_CACHE
    SEGMENTATION_CACHE = cache


def get_users_by_segment(segment: str) -> List[Dict[str, Any]]:
    """Return cached users for a given segment."""
    return SEGMENTATION_CACHE.get(segment, [])


def schedule_daily_update(db: MallDatabase) -> None:
    """Schedule daily segmentation refresh and notification dispatch."""

    def _job() -> None:
        update_segmentation_cache(db)
        threading.Timer(24 * 60 * 60, _job).start()

    _job()


__all__ = [
    "classify_user",
    "update_segmentation_cache",
    "get_users_by_segment",
    "schedule_daily_update",
]

