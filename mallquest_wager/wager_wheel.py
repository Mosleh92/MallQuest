import random
from datetime import datetime
from typing import Dict, Any

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import Session

import database

# Re-use global SQLAlchemy base and user model
Base = database.Base
User = database.User

# Obtain global database instance or create one
# This keeps compatibility with modules expecting `database.db`
db = getattr(database, "db", None)
if db is None:
    db = database.MallDatabase()
    database.db = db


class VoucherCatalog(Base):
    """Catalog of possible wheel prizes with probabilities and costs."""

    __tablename__ = "voucher_catalog"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    value = Column(Float, nullable=False)
    cost = Column(Integer, nullable=False)  # coins required to attempt this prize


class WagerLog(Base):
    """Log of wheel spins and their resulting prizes."""

    __tablename__ = "wager_wheel_log"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    prize_name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    cost = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# Ensure tables exist in all configured engines
for engine in db.engines:
    Base.metadata.create_all(engine)


def seed_catalog() -> None:
    """Populate default wheel prizes and costs if catalog is empty."""
    session = db.sessions[0]()
    try:
        if session.query(VoucherCatalog).count() == 0:
            defaults = [
                ("Bronze Voucher", 0.6, 5.0, 10),
                ("Silver Voucher", 0.3, 10.0, 20),
                ("Gold Voucher", 0.1, 20.0, 30),
            ]
            for name, weight, value, cost in defaults:
                session.add(
                    VoucherCatalog(name=name, weight=weight, value=value, cost=cost)
                )
            session.commit()
    finally:
        session.close()


def spin_wheel(user_id: str, coins: int) -> Dict[str, Any]:
    """
    Spin the wager wheel for the specified user.

    Parameters
    ----------
    user_id: str
        User performing the spin.
    coins: int
        Number of coins the user is willing to spend. Only prizes whose cost is
        less than or equal to this value are considered.
    """
    session: Session = db._session_for_key(user_id)
    try:
        user = session.get(User, user_id)
        if not user or user.coins < coins:
            return {"success": False, "error": "Insufficient coins"}

        prizes = session.query(VoucherCatalog).filter(VoucherCatalog.cost <= coins).all()
        if not prizes:
            return {"success": False, "error": "No prizes available"}

        weights = [p.weight for p in prizes]
        total_weight = sum(weights)
        if total_weight <= 0:
            return {"success": False, "error": "Invalid prize weights"}

        chosen = random.choices(prizes, weights=weights, k=1)[0]

        # Deduct the cost from user's coins
        user.coins -= chosen.cost

        log = WagerLog(
            user_id=user_id,
            prize_name=chosen.name,
            value=chosen.value,
            cost=chosen.cost,
            created_at=datetime.utcnow(),
        )
        session.add(log)
        session.commit()

        return {
            "success": True,
            "prize": chosen.name,
            "value": chosen.value,
            "cost": chosen.cost,
            "remaining_coins": user.coins,
        }
    finally:
        session.close()
