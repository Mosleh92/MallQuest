#!/usr/bin/env python3
"""Database layer using SQLAlchemy with sharding support.

This module replaces the broken merge state with a clean implementation that
includes basic user and receipt management along with notification logging and
mall entry tracking. It uses SQLAlchemy and a simple hash based sharding
strategy.
"""

from __future__ import annotations

import hashlib
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    create_engine,
    func,
)
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from logger import get_logger


Base = declarative_base()
log = get_logger(__name__)


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    phone = Column(String)
    password_hash = Column(String)
    role = Column(String, default="player")
    coins = Column(Integer, default=0)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    vip_tier = Column(String, default="Bronze")
    vip_points = Column(Integer, default=0)
    total_spent = Column(Float, default=0.0)
    last_purchase_at = Column(DateTime, nullable=True)
    language = Column(String, default="en")
    date_of_birth = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_entry_at = Column(DateTime, nullable=True)


class Receipt(Base):
    __tablename__ = "receipts"

    receipt_id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    store = Column(String, nullable=False)
    category = Column(String)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="AED")
    status = Column(String, default="pending")
    items = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    message = Column(String, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    delivered = Column(Boolean, default=False)


class MallEntry(Base):
    __tablename__ = "mall_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    location = Column(String)
    device_info = Column(JSON)
    latitude = Column(Float)
    longitude = Column(Float)


class MallDatabase:
    """Database manager using SQLAlchemy with shard routing."""

    def __init__(
        self,
        dsn: Optional[str] = None,
        shard_count: Optional[int] = None,
        shard_strategy: Optional[str] = None,
    ) -> None:
        self.dsn = dsn or os.getenv("DATABASE_URL", "sqlite:///mall_gamification.db")
        self.shard_count = shard_count or int(os.getenv("SHARD_COUNT", "1"))
        self.shard_strategy = shard_strategy or os.getenv("SHARD_STRATEGY", "hash")

        self.engines: List[Engine] = []
        self.sessions: List[sessionmaker] = []

        for shard_id in range(self.shard_count):
            shard_dsn = self._dsn_for_shard(shard_id)
            engine = create_engine(shard_dsn)
            self.engines.append(engine)
            self.sessions.append(sessionmaker(bind=engine))
            Base.metadata.create_all(engine)

        # Compatibility: expose first engine connection as ``conn``
        self.conn = self.engines[0].connect()

    # ------------------------------------------------------------------
    # Internal helpers
    def _dsn_for_shard(self, shard_id: int) -> str:
        url = make_url(self.dsn)
        if url.database:
            url = url.set(database=f"{url.database}_shard{shard_id}")
        return str(url)

    def _shard_for_key(self, key: str) -> int:
        if self.shard_strategy == "hash":
            digest = hashlib.sha256(key.encode()).hexdigest()
            return int(digest, 16) % self.shard_count
        raise ValueError(f"Unsupported shard strategy: {self.shard_strategy}")

    def _session_for_key(self, key: str) -> Session:
        index = self._shard_for_key(key)
        return self.sessions[index]()

    # ------------------------------------------------------------------
    # CRUD helpers
    def add_user(self, data: Dict[str, Any]) -> bool:
        session = self._session_for_key(data["user_id"])
        try:
            user = User(**data)
            session.add(user)
            session.commit()
            return True
        except Exception:  # pragma: no cover - log unexpected errors
            session.rollback()
            log.exception("failed to add user %s", data.get("user_id"))
            return False
        finally:
            session.close()

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        session = self._session_for_key(user_id)
        try:
            user = session.get(User, user_id)
            if not user:
                return None
            return {c.name: getattr(user, c.name) for c in user.__table__.columns}
        finally:
            session.close()

    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        session = self._session_for_key(user_id)
        try:
            user = session.get(User, user_id)
            if not user:
                return False
            for key, value in updates.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            session.commit()
            return True
        except Exception:  # pragma: no cover
            session.rollback()
            log.exception("failed to update user %s", user_id)
            return False
        finally:
            session.close()

    def add_receipt(self, data: Dict[str, Any]) -> bool:
        session = self._session_for_key(data["user_id"])
        try:
            receipt = Receipt(**data)
            session.add(receipt)
            user = session.get(User, data["user_id"])
            if user:
                user.last_purchase_at = datetime.utcnow()
                user.total_spent = (user.total_spent or 0.0) + data.get("amount", 0.0)
            session.commit()
            return True
        except Exception:  # pragma: no cover
            session.rollback()
            log.exception("failed to add receipt for user %s", data.get("user_id"))
            return False
        finally:
            session.close()

    def get_user_receipts(self, user_id: str) -> List[Dict[str, Any]]:
        session = self._session_for_key(user_id)
        try:
            rows = session.query(Receipt).filter_by(user_id=user_id).all()
            return [{c.name: getattr(r, c.name) for c in r.__table__.columns} for r in rows]
        finally:
            session.close()

    # ------------------------------------------------------------------
    # Additional helpers
    def log_notification(self, user_id: str, message: str, delivered: bool) -> None:
        session = self._session_for_key(user_id)
        try:
            log_entry = NotificationLog(user_id=user_id, message=message, delivered=delivered)
            session.add(log_entry)
            session.commit()
        except Exception:  # pragma: no cover
            session.rollback()
            log.exception("failed to log notification for user %s", user_id)
        finally:
            session.close()

    def get_dormant_users(self, days: int = 30) -> List[Dict[str, Any]]:
        threshold = datetime.utcnow() - timedelta(days=days)
        result: List[Dict[str, Any]] = []
        for factory in self.sessions:
            session = factory()
            try:
                rows = session.query(User).filter(User.updated_at < threshold).all()
                result.extend({c.name: getattr(row, c.name) for c in row.__table__.columns} for row in rows)
            finally:
                session.close()
        return result

    def log_mall_entry(
        self,
        user_id: str,
        location: str,
        device_info: Dict[str, Any],
        coords: Dict[str, float],
    ) -> bool:
        session = self._session_for_key(user_id)
        try:
            entry = MallEntry(
                user_id=user_id,
                location=location,
                device_info=device_info,
                latitude=coords.get("latitude"),
                longitude=coords.get("longitude"),
            )
            session.add(entry)
            user = session.get(User, user_id)
            if user:
                user.last_entry_at = entry.timestamp
            session.commit()
            return True
        except Exception:  # pragma: no cover
            session.rollback()
            log.exception("failed to log mall entry for user %s", user_id)
            return False
        finally:
            session.close()

    def close(self) -> None:
        for engine in self.engines:
            engine.dispose()

