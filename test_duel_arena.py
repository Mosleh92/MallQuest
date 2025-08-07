import pytest

from duel_arena import DuelArena


class DummyUser:
    def __init__(self, user_id):
        self.user_id = user_id
        self.coins = 0


class DummyMallSystem:
    def __init__(self):
        self.events = []
        self.users = {
            "alice": DummyUser("alice"),
            "bob": DummyUser("bob"),
            "charlie": DummyUser("charlie"),
            "dave": DummyUser("dave"),
        }

    def log_event(self, event_type, details):
        self.events.append((event_type, details))

    def award_coins(self, user_id, amount):
        self.users[user_id].coins += amount


@pytest.fixture
def mall_system():
    return DummyMallSystem()


def test_duel_creation_and_pot(mall_system):
    arena = DuelArena(mall_system)
    duel_id = arena.create_duel(["alice", "bob", "charlie"], stake=10)
    duel = arena.get_duel(duel_id)
    assert duel["pot"] == 30
    assert any(e[0] == "duel_arena_started" and e[1]["duel_id"] == duel_id for e in mall_system.events)


def test_conclude_awards_pot(mall_system):
    arena = DuelArena(mall_system)
    duel_id = arena.create_duel(["alice", "bob"], stake=15)
    result = arena.conclude_duel(duel_id, "bob")
    assert result["pot"] == 30
    assert mall_system.users["bob"].coins == 30
    assert any(e[0] == "duel_arena_completed" and e[1]["duel_id"] == duel_id for e in mall_system.events)


def test_requires_two_to_four_players(mall_system):
    arena = DuelArena(mall_system)
    with pytest.raises(ValueError):
        arena.create_duel(["alice"], stake=5)
    with pytest.raises(ValueError):
        arena.create_duel(["a", "b", "c", "d", "e"], stake=5)
