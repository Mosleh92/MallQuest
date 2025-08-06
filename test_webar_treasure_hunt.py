from unittest.mock import patch

from mall_gamification_system import MallGamificationSystem, User


def test_webar_treasure_daily_limit_and_rewards():
    system = MallGamificationSystem()
    user_id = 'tester'
    system.create_user(user_id)

    with patch('webar_treasure_hunt.random.randint', return_value=10):
        # first three attempts succeed
        for _ in range(3):
            result = system.participate_treasure_hunt(user_id)
            assert result['status'] == 'success'
            assert result['coins'] == 10
            assert 'animation' in result and 'sound' in result

        # fourth attempt hits daily cap
        result = system.participate_treasure_hunt(user_id)
        assert result['status'] == 'limit_reached'
        assert result['remaining'] == 0

    # User coins and missions should reflect rewards
    assert system.users[user_id].coins >= 30
    missions = [m for m in system.users[user_id].missions if m['type'] == 'ar_treasure_hunt']
    assert missions
