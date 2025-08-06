"""Tests for the SuccessMetrics utility."""

from success_metrics import SuccessMetrics


def test_key_metrics_structure():
    metrics = SuccessMetrics().key_metrics()
    assert "user_metrics" in metrics
    assert "business_metrics" in metrics
    assert "mall_metrics" in metrics

    assert metrics["user_metrics"]["DAU"] == "Target: 10K in month 3"
    assert metrics["business_metrics"]["arpu"] == "Average Revenue Per User: $5"
    assert metrics["mall_metrics"]["foot_traffic_increase"] == "+20%"
