import random
import pytest

from coin_duel import CoinDuelManager
from wheel_of_fortune import WheelOfFortune
from database import MallDatabase
from mallquest_wager import wager_system


class DummyUser:
    def __init__(self, user_id):
        self.user_id = user_id
        self.coins = 0
        self.rewards = []


class DummyMallSystem:
    def __init__(self):
        # use in-memory database to isolate state
        self.db = MallDatabase("sqlite:///:memory:")
        self.events = []
        self.users = {
            "alice": DummyUser("alice"),
            "bob": DummyUser("bob"),
        }
        # create users in database
        self.db.add_user({"user_id": "alice", "name": "Alice", "email": "alice@example.com", "coins": 0})
        self.db.add_user({"user_id": "bob", "name": "Bob", "email": "bob@example.com", "coins": 0})

    def log_event(self, event_type, details):
        self.events.append((event_type, details))

    def handle_coin_duel_result(self, duel_id, winner_id, loser_id, scores):
        reward = 50
        winner = self.users[winner_id]
        winner.coins += reward
        row = self.db.get_user(winner_id)
        self.db.update_user(winner_id, {"coins": row["coins"] + reward})
        self.log_event(
            "coin_duel_completed",
            {
                "duel_id": duel_id,
                "winner": winner_id,
                "loser": loser_id,
                "scores": scores,
                "reward": reward,
            },
        )
        return {"winner": winner_id, "loser": loser_id, "reward": reward}

    def get_user(self, user_id):
        return self.users.get(user_id)

    def close(self):
        self.db.close()


@pytest.fixture
def mall_system():
    mall = DummyMallSystem()
    try:
        yield mall
    finally:
        mall.close()


def test_match_creation(mall_system):
    manager = CoinDuelManager(mall_system)
    duel_id = manager.start_duel("alice", "bob")
    assert duel_id in manager.active_duels
    duel = manager.get_duel(duel_id)
    assert set(duel["players"]) == {"alice", "bob"}
    assert any(e[0] == "coin_duel_started" and e[1]["duel_id"] == duel_id for e in mall_system.events)


def test_joining_rejects_non_player(mall_system):
    manager = CoinDuelManager(mall_system)
    duel_id = manager.start_duel("alice", "bob")
    assert manager.update_score(duel_id, "alice", 10) is True
    assert manager.update_score(duel_id, "charlie", 5) is False


def test_coin_transfer_on_conclude(mall_system):
    manager = CoinDuelManager(mall_system)
    duel_id = manager.start_duel("alice", "bob")
    manager.update_score(duel_id, "alice", 10)
    manager.update_score(duel_id, "bob", 5)
    result = manager.conclude_duel(duel_id)
    assert result["winner"] == "alice"
    row = mall_system.db.get_user("alice")
    assert row["coins"] == 50


def test_wheel_spin_probability(mall_system):
    wheel = WheelOfFortune(mall_system)
    wheel.configure_prize("Gold", 0.7, 1000, "coins", 10)
    wheel.configure_prize("Silver", 0.3, 1000, "coins", 5)
    random.seed(0)
    results = [wheel.spin("alice")["prize"] for _ in range(1000)]
    gold_ratio = results.count("Gold") / len(results)
    assert 0.65 <= gold_ratio <= 0.75


def test_safe_zone_timeline_scaling():
    small = wager_system.generate_safe_zone_timeline(10)
    large = wager_system.generate_safe_zone_timeline(40)
    # large matches should start with a wider radius and higher end damage
    assert small[0]["radius"] < large[0]["radius"]
    assert small[-1]["damage_per_tick"] < large[-1]["damage_per_tick"]
    assert len(large) >= len(small)


def test_create_match_populates_safe_zone():
    match = wager_system.create_match("Test", 5, expected_players=30)
    assert match.safe_zone_timeline
    assert match.safe_zone_timeline[0]["radius"] > match.safe_zone_timeline[-1]["radius"]
