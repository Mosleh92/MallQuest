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
from typing import Dict, Set, List

from database import MallDatabase, User


# Global database instance used by the wager system
_db = MallDatabase()


@dataclass
class WagerMatch:
    """Simple in-memory representation of a wager match."""

    match_id: str
    name: str
    stake_each: int
    pot: int = 0
    members: Dict[str, str] = field(default_factory=dict)  # user_id -> squad_id
    eliminated: Set[str] = field(default_factory=set)
    active: bool = True


# Registry for active matches
_MATCHES: Dict[str, WagerMatch] = {}


def create_match(name: str, stake_each: int) -> WagerMatch:
    """Create a new :class:`WagerMatch` and register it."""
    match = WagerMatch(match_id=uuid.uuid4().hex, name=name, stake_each=stake_each)
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
