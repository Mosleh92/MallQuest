from unified_progress import UnifiedProgress


def test_award_and_spend_coins():
    progress = UnifiedProgress()
    progress.award(coins=50, xp=20)
    assert progress.coins.amount == 50
    assert progress.xp == 20

    # spending works when enough balance
    assert progress.coins.spend(30) is True
    assert progress.coins.amount == 20

    # spending more than available fails
    assert progress.coins.spend(25) is False
    assert progress.coins.amount == 20


def test_add_achievement():
    progress = UnifiedProgress()
    progress.add_achievement("finder")
    progress.add_achievement("finder")
    progress.add_achievement("explorer")
    assert progress.achievements == {"finder": 2, "explorer": 1}
