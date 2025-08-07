"""Minimal NFT/collectible system."""

from __future__ import annotations

import random
import uuid
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Collectible:
    item_id: str
    owner_id: str
    name: str
    rarity: str
    last_sale_price: Optional[int] = None


class DigitalCollectibles:
    """Manage collectible generation and trading."""

    def __init__(self) -> None:
        self.items: Dict[str, Collectible] = {}

    def generate_rare_item(self, owner_id: str) -> Optional[Collectible]:
        """Return a collectible with a 10% chance."""
        if random.random() > 0.1:
            return None
        item_id = str(uuid.uuid4())
        name = random.choice(["Golden Deer Card", "VIP Mall Pass"])
        rarity = random.choice(["rare", "epic"])
        item = Collectible(item_id=item_id, owner_id=owner_id, name=name, rarity=rarity)
        self.items[item_id] = item
        return item

    def marketplace_trade(self, seller: str, buyer: str, item_id: str, price: int) -> None:
        if item_id not in self.items:
            raise KeyError("Item not found")
        item = self.items[item_id]
        if item.owner_id != seller:
            raise PermissionError("Seller does not own item")
        item.owner_id = buyer
        item.last_sale_price = price
