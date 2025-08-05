import logging
import random
from typing import Dict, Any


class WheelOfFortune:
    """Configurable wheel of fortune with audit logging."""

    def __init__(self, mall_system, prizes: Dict[str, Dict[str, Any]] = None, log_file: str = 'wheel_audit.log'):
        self.mall_system = mall_system
        self.prizes = prizes or {}
        self.logger = logging.getLogger('WheelOfFortune')
        if not self.logger.handlers:
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def configure_prize(self, name: str, probability: float, inventory: int, reward: Dict[str, Any]):
        """Add or update a prize configuration."""
        self.prizes[name] = {
            'probability': probability,
            'inventory': inventory,
            'reward': reward,
        }

    def get_prizes(self) -> Dict[str, Dict[str, Any]]:
        """Return current prize configuration."""
        return self.prizes

    def spin(self, user_id: str) -> Dict[str, Any]:
        """Spin the wheel for a user, award prize, and log the event."""
        available = [(n, d) for n, d in self.prizes.items() if d.get('inventory', 0) > 0]
        if not available:
            return {}

        names = [name for name, _ in available]
        weights = [data.get('probability', 0) for _, data in available]
        chosen = random.choices(names, weights=weights, k=1)[0]
        prize_info = self.prizes[chosen]
        prize_info['inventory'] -= 1

        reward = prize_info.get('reward', {})
        user = self.mall_system.get_user(user_id)
        if user:
            coins = reward.get('coins', 0)
            xp = reward.get('xp', 0)
            item = reward.get('item')
            if coins:
                user.coins += coins
                user.rewards.append(f"Wheel prize: +{coins} coins")
            if xp:
                user.add_xp(xp, 'wheel_spin')
            if item:
                user.inventory.append(item)

        self.logger.info('user=%s prize=%s remaining=%s', user_id, chosen, prize_info['inventory'])

        return {'prize': chosen, 'reward': reward, 'remaining': prize_info['inventory']}
