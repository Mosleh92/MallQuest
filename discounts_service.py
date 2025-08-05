import time
from typing import List, Dict

import requests


class DiscountsService:
    """Service to fetch and cache current mall promotions."""

    def __init__(self, source_url: str = "https://example.com/mall_promotions.json", ttl: int = 300):
        """
        Initialize the service.

        Args:
            source_url: URL to fetch promotions from.
            ttl: Time-to-live for the cache in seconds.
        """
        self.source_url = source_url
        self.ttl = ttl
        self._cache: List[Dict] = []
        self._last_fetch = 0.0

    def _fetch_from_source(self) -> List[Dict]:
        """Fetch promotions from the remote source.

        Returns a list of promotions. If the request fails, returns a
        default set of promotions so that the discounts page always has
        some content to display.
        """
        try:
            response = requests.get(self.source_url, timeout=5)
            response.raise_for_status()
            data = response.json()
            # Ensure data is in list format
            if isinstance(data, dict):
                data = [data]
            return data
        except Exception:
            # Fallback to default promotions if fetching fails
            return [
                {
                    "title": "Weekend Sale",
                    "details": "Enjoy up to 20% off at participating stores this weekend!",
                },
                {
                    "title": "Food Court Special",
                    "details": "Buy one get one free at select food court outlets.",
                },
            ]

    def get_discounts(self) -> List[Dict]:
        """Return cached promotions, refreshing them when stale."""
        now = time.time()
        if not self._cache or (now - self._last_fetch) > self.ttl:
            self._cache = self._fetch_from_source()
            self._last_fetch = now
        return self._cache
