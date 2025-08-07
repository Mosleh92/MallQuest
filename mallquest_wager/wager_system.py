"""Core game logic for MallQuest wager matches.

Players stake coins to join a match. Eliminating an opponent immediately
transfers their stake to the killer as a **kill reward**. When the match
concludes, any remaining **pot** of staked coins is split evenly among all
surviving members of the winning squad. If players from multiple squads
survive, the pot is divided equally across all survivors to resolve the tie.
Assists are not tracked – only the credited killer receives a kill reward.
"""

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

 codex/add-detailed-safe-zone-timeline
    Attributes
    ----------
    safe_zone_timeline:
        List of stages showing how the safe zone shrinks. Large matches generate
        more stages with bigger starting radii and higher damage per tick.
=======
    The match tracks fairness related parameters including a maximum pot size
    and the maximum fraction a single player may contribute.  These values are
    used by :func:`join_match` when calculating the dynamic stake for a new
    player.
 main
    """

    match_id: str
    name: str
    stake_each: int
    max_pot: int = 1000
    max_player_fraction: float = 0.1  # anti-whale: max 10% of pot per player
    pot: int = 0
    members: Dict[str, str] = field(default_factory=dict)  # user_id -> squad_id
    eliminated: Set[str] = field(default_factory=set)
    active: bool = True
    safe_zone_timeline: List[SafeZoneStage] = field(default_factory=list)


# Registry for active matches
_MATCHES: Dict[str, WagerMatch] = {}


 codex/add-detailed-safe-zone-timeline
def create_match(name: str, stake_each: int, expected_players: int = 0) -> WagerMatch:
    """Create a new :class:`WagerMatch` and register it.

    ``expected_players`` determines safe-zone scaling: small (<=20) vs. large
    matches (>20).
=======
def create_match(name: str, stake_each: int, max_pot: int = 1000, max_player_fraction: float = 0.1) -> WagerMatch:
    """Create and register a new :class:`WagerMatch`.

    Parameters
    ----------
    name:
        Friendly name of the match.
    stake_each:
        Base stake required from each participant before adjustments.
    max_pot:
        Maximum total pot size allowed for this match.
    max_player_fraction:
        Maximum fraction of the pot a single player may contribute.
 main
    """
    match = WagerMatch(
        match_id=uuid.uuid4().hex,
        name=name,
        stake_each=stake_each,
 codex/add-detailed-safe-zone-timeline
        safe_zone_timeline=generate_safe_zone_timeline(expected_players),
=======
        max_pot=max_pot,
        max_player_fraction=max_player_fraction,
 main
    )
    _MATCHES[match.match_id] = match
    return match


def join_match(user_id: str, match_id: str, squad_id: str) -> bool:
    """Join an existing match by staking coins.

    Coins are deducted from the user's balance using a database transaction and
    added to the match's pot.  The amount deducted is **dynamically adjusted**
    according to two rules:

    1. ``match.max_pot`` caps the total size of the pot.
    2. ``match.max_player_fraction`` ensures a single player cannot contribute
       more than a fraction of the maximum pot (anti-whale mechanism).

    The actual stake used is the minimum of the base ``stake_each``, the
    remaining room before reaching ``max_pot`` and the player's allowed share of
    the pot.
    """
    match = _MATCHES.get(match_id)
    if not match or not match.active or match.pot >= match.max_pot:
        return False

    session = _db._session_for_key(user_id)
    try:
        user = session.get(User, user_id)
        if not user:
            session.rollback()
            return False

        # calculate dynamic stake
        stake = min(
            match.stake_each,
            int(user.coins * match.max_player_fraction),
            int(match.max_pot * match.max_player_fraction),
            match.max_pot - match.pot,
        )

        if stake <= 0 or user.coins < stake:
            session.rollback()
            return False

        user.coins -= stake
        session.commit()
        match.members[user_id] = squad_id
        match.pot += stake
        return True
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()


def record_kill(winner_id: str, loser_id: str, match_id: str) -> bool:
    """Record a kill and transfer coins from loser to winner.

    The killer receives the loser's staked amount as an immediate reward. The
    transfer does not affect the match pot. Assists are ignored – only the
    player credited with the kill is rewarded.
    """
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
    """Finish a match and distribute the remaining pot among survivors.

    Each surviving teammate on the winning squad receives an equal share of
    the pot. If members of multiple squads remain, the match ends in a tie and
    the pot is split evenly among all surviving players. Eliminated players and
    assists do not receive any portion of the pot.
    """
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
