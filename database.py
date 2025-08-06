#!/usr/bin/env python3
"""Database layer using SQLAlchemy with PostgreSQL DSN and sharding support."""
from __future__ import annotations

import os
import hashlib
from datetime import datetime
from typing import Any, Dict, Optional, List

from sqlalchemy import create_engine, Column, String, Integer, Float, JSON, DateTime
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
    coins = Column(Integer, default=0)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    vip_tier = Column(String, default="Bronze")
    vip_points = Column(Integer, default=0)
    total_spent = Column(Float, default=0.0)
    language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


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


class MallDatabase:
    """Database manager using SQLAlchemy with shard routing."""

    def __init__(self, dsn: Optional[str] = None, shard_count: int = 1):
        self.dsn = dsn or os.getenv("DATABASE_URL", "sqlite:///mall_gamification.db")
        self.shard_count = shard_count
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
        digest = hashlib.sha256(key.encode()).hexdigest()
        return int(digest, 16) % self.shard_count

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

    def get_user_receipts(self, user_id: str) -> List[Dict[str, Any]]:
        session = self._session_for_key(user_id)
        try:
            rows = session.query(Receipt).filter_by(user_id=user_id).all()
            return [{c.name: getattr(r, c.name) for c in r.__table__.columns} for r in rows]
        finally:
            session.close()

    def close(self) -> None:
        for engine in self.engines:
            engine.dispose()
