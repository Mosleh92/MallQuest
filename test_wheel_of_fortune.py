import random
import logging

from wheel_of_fortune import WheelOfFortune


class DummyUser:
    def __init__(self):
        self.coins = 0
        self.rewards = []


class DummyMall:
    def __init__(self):
        self.users = {'tester': DummyUser()}

    def get_user(self, user_id):
        return self.users.get(user_id)


def test_wheel_spin_awards_coins():
    mall = DummyMall()
    wheel = WheelOfFortune(mall)
    wheel.configure_prize('Five Coins', 1.0, 1, 'coins', 5)
    random.seed(0)
    result = wheel.spin('tester')
    assert result['success'] is True
    assert mall.users['tester'].coins == 5
    assert wheel.prizes['Five Coins']['inventory'] == 0
    assert wheel.get_audit_log()


def test_wheel_spin_logs_event(caplog):
    mall = DummyMall()
    wheel = WheelOfFortune(mall)
    wheel.configure_prize('Five Coins', 1.0, 1, 'coins', 5)
    random.seed(0)
    with caplog.at_level(logging.INFO):
        wheel.spin('tester')
    assert any('[WheelOfFortune] spin' in record.getMessage() for record in caplog.records)
