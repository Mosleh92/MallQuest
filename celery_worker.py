"""Celery worker and tasks for MallQuest."""

import os

from celery import Celery


celery_app = Celery(
    "mallquest",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
)


@celery_app.task
def process_receipt(data):
    """Placeholder task to process an uploaded receipt."""
    return {"status": "processed", "data": data}


@celery_app.task
def expire_old_coins():
    """Placeholder task to expire old coins."""
    return "expired"


__all__ = ["celery_app", "process_receipt", "expire_old_coins"]

