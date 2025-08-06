 codex/implement-wheel-of-fortune-features
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
=======
import random
from datetime import datetime
from typing import Dict, Any, Optional
import logging



logger = logging.getLogger(__name__)


class WheelOfFortune:
    """Prize wheel with configurable prizes and audit logging."""

    def __init__(self, mall_system):
        self.mall_system = mall_system
        # prize_name -> config
        self.prizes: Dict[str, Dict[str, Any]] = {}
        self.audit_log = []

    # Prize configuration
    def configure_prize(
        self,
        name: str,
        probability: float,
        inventory: int,
        prize_type: str = "coins",
        value: int = 0,
    ) -> None:
        """Add or replace a prize configuration."""
        self.prizes[name] = {
            "probability": float(probability),
            "inventory": int(inventory),
            "type": prize_type,
            "value": value,
        }
        self._log("configure", {"name": name, "probability": probability, "inventory": inventory})

    def update_prize(
        self,
        name: str,
        probability: Optional[float] = None,
        inventory: Optional[int] = None,
    ) -> bool:
        """Update existing prize. Returns True if prize exists and updated."""
        prize = self.prizes.get(name)
        if not prize:
            return False
        if probability is not None:
            prize["probability"] = float(probability)
        if inventory is not None:
            prize["inventory"] = int(inventory)
        self._log("update", {"name": name, "probability": probability, "inventory": inventory})
        return True

    # Spin mechanics
    def spin(self, user_id: str) -> Dict[str, Any]:
        available = {k: v for k, v in self.prizes.items() if v.get("inventory", 0) > 0}
        if not available:
            self._log("spin", {"user_id": user_id, "result": None, "reason": "empty"})
            return {"success": False, "error": "No prizes available"}

        names = list(available.keys())
        weights = [available[n]["probability"] for n in names]
        total_weight = sum(weights)
        if total_weight <= 0:
            self._log("spin", {"user_id": user_id, "result": None, "reason": "invalid_prob"})
            return {"success": False, "error": "Invalid prize probabilities"}

        choice = random.choices(names, weights=weights, k=1)[0]
        prize_cfg = self.prizes[choice]
        prize_cfg["inventory"] -= 1

        distribution_result = self._distribute_prize(user_id, choice, prize_cfg)
        self._log("spin", {"user_id": user_id, "result": choice})
        return {"success": True, "prize": choice, "details": distribution_result}

    def _distribute_prize(self, user_id: str, name: str, cfg: Dict[str, Any]) -> Dict[str, Any]:
        """Grant prize to user using existing reward systems."""
        result: Dict[str, Any] = {"type": cfg.get("type")}
        if cfg.get("type") == "coins":
            user = self.mall_system.get_user(user_id)
            if user:
                amount = int(cfg.get("value", 0))
                user.coins += amount
                user.rewards.append(f"Wheel prize: {name} +{amount} coins")
                result["coins"] = amount
        elif cfg.get("type") == "voucher":
            from voucher_system import voucher_system  # lazy import to avoid DB init if unused
            value = float(cfg.get("value", 0))
            code = voucher_system.issue_voucher(value, user_id, performed_by="wheel_of_fortune")
            result.update({"code": code, "value": value})
        else:
            # Unknown prize types are just logged
            result["info"] = cfg.get("value")
        return result

    # Audit logging
    def _log(self, action: str, details: Dict[str, Any]) -> None:
        entry = {"action": action, "details": details, "timestamp": datetime.utcnow()}
        self.audit_log.append(entry)
        logger.info("[WheelOfFortune] %s - %s", action, details)

    def get_audit_log(self) -> list:
        return list(self.audit_log)

    def list_prizes(self) -> Dict[str, Dict[str, Any]]:
        return {k: v.copy() for k, v in self.prizes.items()}
 main
