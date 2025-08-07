"""Central logging configuration for MallQuest.

This module sets up a JSON based logger that can be shared across the
application. Log level can be controlled with the ``LOG_LEVEL`` environment
variable.
"""

from __future__ import annotations

import json
import logging
import os


class JsonFormatter(logging.Formatter):
    """Simple JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:  # noqa: D401
        log_record = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)


def configure_logging() -> None:
    """Configure root logger with JSON formatting."""

    level = os.getenv("LOG_LEVEL", "INFO").upper()
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level)
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Return a module-level logger."""

    return logging.getLogger(name)


# Configure logging on import for convenience
configure_logging()


