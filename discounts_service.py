import os
import time
from typing import Any, Dict, List, Optional

import requests


DEFAULT_PROMOTIONS: List[Dict[str, Any]] = [
    {
        "title": "Buy 1 Get 1 Free",
        "description": "On select items at participating stores.",
        "valid_until": "2025-12-31",
    },
    {
        "title": "Free Parking Weekend",
        "description": "Enjoy free parking every weekend this month.",
        "valid_until": "2025-12-31",
    },
]


class DiscountsService:
    """Service to retrieve and cache current mall promotions."""

    def __init__(self, api_url: Optional[str] = None, cache_ttl: int = 300) -> None:
        """Initialize the service.

        Args:
            api_url: Optional URL to fetch promotions from.
            cache_ttl: Time in seconds before cached data expires.
        """
        self.api_url = api_url or os.getenv("MALL_PROMOTIONS_URL")
        self.cache_ttl = cache_ttl
        self._cache: List[Dict[str, Any]] = []
        self._expires_at = 0.0

    def _fetch_promotions(self) -> List[Dict[str, Any]]:
        """Fetch promotions from the API or return defaults."""
        if not self.api_url:
            return DEFAULT_PROMOTIONS

        response = requests.get(self.api_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and "promotions" in data:
            return data["promotions"]  # type: ignore[return-value]
        return data  # type: ignore[return-value]

    def get_discounts(self) -> List[Dict[str, Any]]:
        """Return cached promotions, refreshing as needed."""
        now = time.time()
        if now >= self._expires_at:
            try:
                self._cache = self._fetch_promotions()
            except Exception:
                if not self._cache:
                    self._cache = DEFAULT_PROMOTIONS
            self._expires_at = now + self.cache_ttl
        return self._cache


# Create a default instance for convenience
discounts_service = DiscountsService()

