import logging

from mall_gamification_system import MallGamificationSystem


def test_process_receipt_emits_log(caplog):
    system = MallGamificationSystem()
    system.create_user("tester", "en")
    with caplog.at_level(logging.INFO):
        system.process_receipt("tester", 100.0, "Deerfields Fashion")
    assert any(
        "Reward assigned to tester" in record.getMessage()
        for record in caplog.records
    )

