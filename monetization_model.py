"""Model encapsulating the platform's monetization strategies."""

from typing import Any, Dict


class MonetizationModel:
    """Represents the revenue streams available to the platform."""

    def revenue_streams(self) -> Dict[str, Dict[str, Any]]:
        """Return the platform's revenue streams.

        Returns:
            A nested dictionary describing monetization approaches for
            different partnership types.
        """
        return {
            "b2b_store_partnerships": {
                "sponsored_quests": "$100-1000 per quest",
                "foot_traffic": "$0.50 per unique visitor",
                "purchase_commission": "2-5% of sales",
                "featured_placement": "$500-5000/month",
                "data_insights": "$1000-10000/month",
            },
            "b2c_user_revenue": {
                "vip_subscription": {
                    "price": "$4.99/month",
                    "benefits": "2X coins, no ads, exclusive",
                },
                "coin_purchases": "Direct IAP",
                "cosmetics": "Avatar items",
                "battle_passes": "Seasonal content",
            },
            "b2b_mall_partnership": {
                "licensing": "Revenue share 10-20%",
                "exclusivity": "Premium fees",
                "white_label": "Custom versions",
            },
        }
