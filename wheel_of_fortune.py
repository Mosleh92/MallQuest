"""Wheel of Fortune module with logging and audit support."""

import logging
import random
from datetime import datetime
from typing import Any, Dict, Optional

import logger as logger_config  # ensure logging is configured


logger = logging.getLogger(__name__)


class WheelOfFortune:
    """Prize wheel with configurable prizes and audit logging."""

    def __init__(self, mall_system):
        self.mall_system = mall_system
        # prize_name -> configuration
        self.prizes: Dict[str, Dict[str, Any]] = {}
        self.audit_log = []

    # Prize configuration -------------------------------------------------
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

    # Spin mechanics ------------------------------------------------------
    def spin(self, user_id: str) -> Dict[str, Any]:
        """Spin the wheel for a user and distribute the prize."""
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
            from voucher_system import voucher_system  # lazy import
            value = float(cfg.get("value", 0))
            code = voucher_system.issue_voucher(value, user_id, performed_by="wheel_of_fortune")
            result.update({"code": code, "value": value})
        else:
            # Unknown prize types are just logged
            result["info"] = cfg.get("value")
        return result

    # Audit logging -------------------------------------------------------
    def _log(self, action: str, details: Dict[str, Any]) -> None:
        entry = {"action": action, "details": details, "timestamp": datetime.utcnow()}
        self.audit_log.append(entry)
        logger.info("[WheelOfFortune] %s - %s", action, details)

    def get_audit_log(self) -> list:
        return list(self.audit_log)

    def list_prizes(self) -> Dict[str, Dict[str, Any]]:
        return {k: v.copy() for k, v in self.prizes.items()}

