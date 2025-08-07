from dataclasses import dataclass

@dataclass
class MallCoin:
    """Simple representation of MallQuest's unified currency.

    This dataclass centralises basic operations for earning and spending
    coins across the different MallQuest games. It is intentionally
    lightweight so that existing systems that track integer coins can
    gradually migrate to this unified interface.
    """

    amount: int = 0

    def add(self, value: int) -> None:
        """Add coins to the balance.

        Negative values are ignored to avoid accidental deductions.
        """
        if value > 0:
            self.amount += int(value)

    def spend(self, value: int) -> bool:
        """Attempt to spend coins from the balance.

        Returns ``True`` if the balance contained enough coins and the
        deduction was performed, otherwise ``False``.
        """
        value = int(value)
        if value <= 0 or value > self.amount:
            return False
        self.amount -= value
        return True
