"""Utility to provide key success metrics for user engagement, business performance, and mall outcomes."""

class SuccessMetrics:
    """Container for application success metrics across multiple domains."""

    def key_metrics(self):
        """Return structured success metrics for users, business, and mall."""
        return {
            "user_metrics": {
                "DAU": "Target: 10K in month 3",
                "MAU": "Target: 50K in month 6",
                "retention_d1": "Target: 60%",
                "retention_d30": "Target: 25%",
                "session_length": "Target: 15 min",
            },
            "business_metrics": {
                "conversion": "Game → Purchase: 30%",
                "arpu": "Average Revenue Per User: $5",
                "ltv": "Lifetime Value: $50",
                "cac": "Customer Acquisition: <$10",
                "viral_coefficient": "Target: >1.2",
            },
            "mall_metrics": {
                "foot_traffic_increase": "+20%",
                "dwell_time": "+30 minutes",
                "store_visits": "+3 per trip",
                "purchase_frequency": "+25%",
            },
        }
