"""User segmentation utilities."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import os

from redis import Redis
from rq import Queue

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


# Configure task queue
redis_conn = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
queue = Queue("segmentation", connection=redis_conn)


def update_segmentation_cache_job() -> None:
    """Background job that refreshes the segmentation cache and reschedules itself."""
    db = MallDatabase()
    update_segmentation_cache(db)
    try:
        queue.enqueue_in(timedelta(days=1), update_segmentation_cache_job)
    except Exception:  # pragma: no cover - Redis may be unavailable during tests
        pass


def get_users_by_segment(segment: str) -> List[Dict[str, Any]]:
    """Return cached users for a given segment."""
    return SEGMENTATION_CACHE.get(segment, [])


 codex/update-database-configuration-to-postgresql
def schedule_daily_update() -> None:
    """Kick off the daily segmentation cache refresh job."""
    try:
        queue.enqueue(update_segmentation_cache_job)
    except Exception:  # pragma: no cover - Redis may be unavailable during tests
        pass
=======
def schedule_daily_update(db: MallDatabase) -> None:
    """Schedule daily segmentation refresh and notification dispatch."""

    def _job() -> None:
        update_segmentation_cache(db)
        threading.Timer(24 * 60 * 60, _job).start()

    _job()
 main


__all__ = [
    "classify_user",
    "update_segmentation_cache",
    "get_users_by_segment",
    "schedule_daily_update",
    "update_segmentation_cache_job",
]

