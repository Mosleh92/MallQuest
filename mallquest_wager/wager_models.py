from datetime import datetime

from sqlalchemy import Column, String, Float, Integer, DateTime, JSON, ForeignKey

from database import Base


class WagerMatch(Base):
    """Represents a wager match with map and safe-zone details.

    The ``safe_zones`` JSON column stores the shrink timeline as a list of
    stages. Each stage includes:

    * ``radius`` – current safe-zone radius
    * ``shrink_duration`` – seconds taken to reach the next stage
    * ``damage_per_tick`` – damage applied outside the zone each tick

    Small matches (20 players or fewer) use shorter durations and smaller radii
    while large matches start wider, shrink more gradually, and inflict higher
    damage per tick as the match progresses.
    """

    __tablename__ = "wager_matches"

    match_id = Column(String, primary_key=True)
    stake = Column(Float, default=0.0)
    pot = Column(Float, default=0.0)
    status = Column(String, default="pending")
    map_data = Column(JSON)
    safe_zones = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WagerPlayer(Base):
    """Tracks players participating in wager matches."""

    __tablename__ = "wager_players"

    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(String, ForeignKey("wager_matches.match_id"))
    user_id = Column(String, ForeignKey("users.user_id"))
    stake = Column(Float, default=0.0)
    status = Column(String, default="joined")
    created_at = Column(DateTime, default=datetime.utcnow)


class VoucherCatalog(Base):
    """Catalog of vouchers available in the system."""

    __tablename__ = "voucher_catalog"

    voucher_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    value = Column(Float, default=0.0)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
