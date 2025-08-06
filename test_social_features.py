"""Tests for the SocialFeatures module."""

from social_features import SocialFeatures


def test_complete_social_system_structure():
    features = SocialFeatures().complete_social_system()
    assert "chat" in features
    assert "social_graph" in features
    assert "sharing" in features

    assert features["chat"]["team_chat"] == "Real-time team communication"
    assert features["social_graph"]["friends"] == "Add/invite system"
    assert features["sharing"]["achievements"] == "Social media integration"
