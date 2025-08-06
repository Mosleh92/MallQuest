from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Dict, Set, List, TypedDict

from database import MallDatabase, User


# Global database instance used by the wager system
_db = MallDatabase()


class SafeZoneStage(TypedDict):
    """Single stage of safe-zone progression."""

    radius: float
    shrink_duration: float
    damage_per_tick: float


def generate_safe_zone_timeline(player_count: int) -> List[SafeZoneStage]:
    """Generate safe-zone stages based on expected ``player_count``.

    Small matches (20 or fewer players) shrink faster with lighter damage,
    while large matches start with a wider radius, shrink more gradually, and
    inflict higher damage outside the zone. Each stage defines the ``radius`` of
    the safe area, how long it takes to shrink to the next stage
    (``shrink_duration`` in seconds), and the ``damage_per_tick`` dealt to
    players outside the zone.
    """

    if player_count <= 20:  # small match
        base_radius = 500.0
        base_duration = 45.0
        damage = 1.0
        stages = 4
    else:  # large match
        base_radius = 1000.0
        base_duration = 90.0
        damage = 1.5
        stages = 5

    radius = base_radius
    duration = base_duration
    timeline: List[SafeZoneStage] = []
    for _ in range(stages):
        timeline.append(
            {
                "radius": radius,
                "shrink_duration": duration,
                "damage_per_tick": damage,
            }
        )
        radius *= 0.6
        duration *= 0.8
        damage *= 1.5

    return timeline


@dataclass
class WagerMatch:
    """Simple in-memory representation of a wager match.

    Attributes
    ----------
    safe_zone_timeline:
        List of stages showing how the safe zone shrinks. Large matches generate
        more stages with bigger starting radii and higher damage per tick.
    """

    match_id: str
    name: str
    stake_each: int
    pot: int = 0
    members: Dict[str, str] = field(default_factory=dict)  # user_id -> squad_id
    eliminated: Set[str] = field(default_factory=set)
    active: bool = True
    safe_zone_timeline: List[SafeZoneStage] = field(default_factory=list)


# Registry for active matches
_MATCHES: Dict[str, WagerMatch] = {}


def create_match(name: str, stake_each: int, expected_players: int = 0) -> WagerMatch:
    """Create a new :class:`WagerMatch` and register it.

    ``expected_players`` determines safe-zone scaling: small (<=20) vs. large
    matches (>20).
    """
    match = WagerMatch(
        match_id=uuid.uuid4().hex,
        name=name,
        stake_each=stake_each,
        safe_zone_timeline=generate_safe_zone_timeline(expected_players),
    )
    _MATCHES[match.match_id] = match
    return match


def join_match(user_id: str, match_id: str, squad_id: str) -> bool:
    """Join an existing match by staking coins.

    Coins are deducted from the user's balance using a database transaction. The
    deducted amount is added to the match's pot.
    """
    match = _MATCHES.get(match_id)
    if not match or not match.active:
        return False

    session = _db._session_for_key(user_id)
    try:
        user = session.get(User, user_id)
        if not user or user.coins < match.stake_each:
            session.rollback()
            return False
        user.coins -= match.stake_each
        session.commit()
        match.members[user_id] = squad_id
        match.pot += match.stake_each
        return True
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()


def record_kill(winner_id: str, loser_id: str, match_id: str) -> bool:
    """Record a kill and transfer coins from loser to winner."""
    match = _MATCHES.get(match_id)
    if not match or not match.active:
        return False
    if winner_id not in match.members or loser_id not in match.members:
        return False

    # sessions grouped by shard to ensure atomic commits
    sessions: Dict[int, any] = {}
    for uid in {winner_id, loser_id}:
        shard = _db._shard_for_key(uid)
        if shard not in sessions:
            sessions[shard] = _db.sessions[shard]()

    try:
        winner_session = sessions[_db._shard_for_key(winner_id)]
        loser_session = sessions[_db._shard_for_key(loser_id)]
        winner = winner_session.get(User, winner_id)
        loser = loser_session.get(User, loser_id)
        if not winner or not loser or loser.coins < match.stake_each:
            for s in sessions.values():
                s.rollback()
            return False
        loser.coins -= match.stake_each
        winner.coins += match.stake_each
        for s in sessions.values():
            s.commit()
        match.eliminated.add(loser_id)
        return True
    except Exception:
        for s in sessions.values():
            s.rollback()
        return False
    finally:
        for s in sessions.values():
            s.close()


def finish_match(match_id: str) -> Dict[str, int]:
    """Finish a match and distribute the remaining pot among survivors."""
    match = _MATCHES.get(match_id)
    if not match or not match.active:
        return {}

    survivors: List[str] = [uid for uid in match.members if uid not in match.eliminated]
    if not survivors or match.pot <= 0:
        match.active = False
        return {}

    share = match.pot // len(survivors)
    sessions: Dict[int, any] = {}
    for uid in survivors:
        shard = _db._shard_for_key(uid)
        if shard not in sessions:
            sessions[shard] = _db.sessions[shard]()

    try:
        for uid in survivors:
            sess = sessions[_db._shard_for_key(uid)]
            user = sess.get(User, uid)
            if user:
                user.coins += share
        for s in sessions.values():
            s.commit()
        match.active = False
        match.pot = 0
        return {uid: share for uid in survivors}
    except Exception:
        for s in sessions.values():
            s.rollback()
        return {}
    finally:
        for s in sessions.values():
            s.close()
