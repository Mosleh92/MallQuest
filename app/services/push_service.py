import os
import time
import logging
from typing import Optional

import requests

from database import MallDatabase

logger = logging.getLogger(__name__)

FIREBASE_URL = "https://fcm.googleapis.com/fcm/send"
FIREBASE_SERVER_KEY = os.getenv("FIREBASE_SERVER_KEY", "")

_db = MallDatabase()


def _post_message(token: str, message: str) -> bool:
    headers = {
        "Authorization": f"key={FIREBASE_SERVER_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "to": token,
        "notification": {"title": "MallQuest", "body": message},
    }
    response = requests.post(FIREBASE_URL, headers=headers, json=payload, timeout=5)
    data = response.json() if response.content else {}
    return response.status_code == 200 and data.get("success") == 1


def send_push(user_id: str, message: str, retries: int = 3, db_instance: Optional[MallDatabase] = None) -> bool:
    """Send a push notification via Firebase and log delivery."""
    db = db_instance or _db
    token = f"/topics/{user_id}"
    success = False
    for attempt in range(1, retries + 1):
        try:
            success = _post_message(token, message)
            if success:
                break
            logger.warning("Push attempt %s failed for user %s", attempt, user_id)
        except Exception:
            logger.exception("Error sending push to %s on attempt %s", user_id, attempt)
        time.sleep(1)
    db.log_notification(user_id, message, delivered=success)
    if not success:
        logger.error("All attempts failed for user %s", user_id)
    return success


def send_retention_push(days: int = 30, db_instance: Optional[MallDatabase] = None) -> int:
    """Scheduled job to send retention messages to dormant users."""
    db = db_instance or _db
    users = db.get_dormant_users(days)
    message = "We miss you at MallQuest! Come back for a special promo."
    sent = 0
    for user in users:
        if send_push(user["user_id"], message, db_instance=db):
            sent += 1
    return sent
