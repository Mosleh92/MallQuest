#!/usr/bin/env python3
"""Database layer using SQLAlchemy with PostgreSQL DSN and sharding support."""
from __future__ import annotations

import os
import hashlib
 codex/add-last_purchase_at-to-user-model
import uuid
from datetime import datetime
=======
from datetime import datetime, timedelta
 main
from typing import Any, Dict, Optional, List

from sqlalchemy import create_engine, Column, String, Integer, Float, JSON, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import make_url

Base = declarative_base()


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


 codex/add-purchasehistory-model-and-api
class PurchaseHistory(Base):
    __tablename__ = "purchase_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    store_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    upload_type = Column(String, nullable=False)
    receipt_url = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
=======
class MallEntry(Base):
    __tablename__ = "mall_entries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    location = Column(String)
    device_info = Column(JSON)
    latitude = Column(Float)
    longitude = Column(Float)
 main


class MallDatabase:
    """Database manager using SQLAlchemy with shard routing."""

    def __init__(self, dsn: Optional[str] = None, shard_count: Optional[int] = None, shard_strategy: Optional[str] = None):
        """Initialize the database layer.

        Parameters
        ----------
        dsn: str, optional
            Base SQLAlchemy DSN. If omitted, uses ``DATABASE_URL`` env var and
            falls back to SQLite.
        shard_count: int, optional
            Number of database shards. Defaults to ``SHARD_COUNT`` env var or 1.
        shard_strategy: str, optional
            Strategy name used for shard mapping. Currently only ``"hash"`` is
            supported. Defaults to ``SHARD_STRATEGY`` env var or ``"hash"``.
        """
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

        # provide connection to first shard for backward compatibility
        self.conn = self.engines[0].connect()

    def _dsn_for_shard(self, shard_id: int) -> str:
        url = make_url(self.dsn)
        if url.database:
            url = url.set(database=f"{url.database}_shard{shard_id}")
        return str(url)

    def _shard_for_key(self, key: str) -> int:
        """Return shard index for the given key based on configured strategy."""
        if self.shard_strategy == "hash":
            digest = hashlib.sha256(key.encode()).hexdigest()
            return int(digest, 16) % self.shard_count
        raise ValueError(f"Unsupported shard strategy: {self.shard_strategy}")

    def _session_for_key(self, key: str) -> Session:
        index = self._shard_for_key(key)
        return self.sessions[index]()

    # CRUD helpers
    def add_user(self, data: Dict[str, Any]) -> bool:
        session = self._session_for_key(data["user_id"])
        try:
            user = User(**data)
            session.add(user)
            session.commit()
            return True
        except Exception:
            session.rollback()
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
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()

    def add_receipt(self, data: Dict[str, Any]) -> bool:
        session = self._session_for_key(data["user_id"])
        try:
            receipt = Receipt(**data)
            session.add(receipt)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()

    def add_purchase_record(
        self,
        user_id: str,
        amount: float,
        store: str,
        category: Optional[str] = None,
        currency: str = "AED",
        items: Optional[Any] = None,
    ) -> bool:
        """Add a purchase record and update user's last purchase timestamp."""
        session = self._session_for_key(user_id)
        try:
            receipt = Receipt(
                receipt_id=str(uuid.uuid4()),
                user_id=user_id,
                store=store,
                category=category,
                amount=amount,
                currency=currency,
                status="completed",
                items=items,
                created_at=datetime.utcnow(),
            )
            session.add(receipt)
            user = session.get(User, user_id)
            if user:
                user.last_purchase_at = datetime.utcnow()
                user.total_spent = (user.total_spent or 0.0) + amount
            session.commit()
            return True
        except Exception:
            session.rollback()
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

 codex/add-purchasehistory-model-and-api
    def add_purchase_record(self, data: Dict[str, Any]) -> bool:
        session = self._session_for_key(data["user_id"])
        try:
            record = PurchaseHistory(**data)
            session.add(record)
=======
    def log_mall_entry(
        self,
        user_id: str,
        location: str,
        device_info: Dict[str, Any],
        coords: Dict[str, float],
    ) -> bool:
        """Insert a mall entry and update the user's last entry timestamp."""

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
 main
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()

 codex/add-purchasehistory-model-and-api
    def get_purchase_stats(self, range: str) -> Dict[str, Dict[str, float]]:
        if range == "daily":
            start = datetime.utcnow() - timedelta(days=1)
        elif range == "weekly":
            start = datetime.utcnow() - timedelta(weeks=1)
        elif range == "monthly":
            start = datetime.utcnow() - timedelta(days=30)
        else:
            start = None

        stats: Dict[str, Dict[str, float]] = {}
        for maker in self.sessions:
            session = maker()
            try:
                query = session.query(
                    PurchaseHistory.store_id,
                    func.count().label("count"),
                    func.sum(PurchaseHistory.amount).label("total"),
                )
                if start:
                    query = query.filter(PurchaseHistory.timestamp >= start)
                query = query.group_by(PurchaseHistory.store_id)
                for store_id, count, total in query.all():
                    if store_id not in stats:
                        stats[store_id] = {"count": 0, "total": 0.0}
                    stats[store_id]["count"] += count
                    stats[store_id]["total"] += float(total or 0.0)
            finally:
                session.close()
        return stats

=======
 main
    def close(self) -> None:
        for engine in self.engines:
            engine.dispose()
