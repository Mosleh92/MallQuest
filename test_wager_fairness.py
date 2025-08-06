import pytest

from mallquest_wager import wager_system
from database import MallDatabase


@pytest.fixture()
def fresh_system():
    """Provide a fresh in-memory database and clear match registry."""
    wager_system._db = MallDatabase("sqlite:///:memory:")
    wager_system._MATCHES.clear()
    # Seed users with varying coin balances
    wager_system._db.add_user({"user_id": "u1", "name": "U1", "email": "u1@example.com", "coins": 200})
    wager_system._db.add_user({"user_id": "u2", "name": "U2", "email": "u2@example.com", "coins": 500})
    wager_system._db.add_user({"user_id": "u3", "name": "U3", "email": "u3@example.com", "coins": 500})
    wager_system._db.add_user({"user_id": "u4", "name": "U4", "email": "u4@example.com", "coins": 500})
    yield
    wager_system._db.close()
    wager_system._MATCHES.clear()


def test_anti_whale_and_dynamic_stake(fresh_system):
    match = wager_system.create_match("fair", stake_each=50, max_pot=1000, max_player_fraction=0.1)
    assert wager_system.join_match("u1", match.match_id, "s1") is True
    # u1 only contributes 10% of their balance -> 20 coins
    assert match.pot == 20
    assert wager_system.join_match("u2", match.match_id, "s1") is True
    # u2 can contribute full base stake
    assert match.pot == 70


def test_pot_cap(fresh_system):
    match = wager_system.create_match("cap", stake_each=50, max_pot=60, max_player_fraction=1.0)
    assert wager_system.join_match("u2", match.match_id, "s1") is True
    assert match.pot == 50
    assert wager_system.join_match("u3", match.match_id, "s1") is True
    # Remaining pot space limits the next stake to 10
    assert match.pot == 60
    # further players cannot join once max pot is reached
    assert not wager_system.join_match("u4", match.match_id, "s1")
