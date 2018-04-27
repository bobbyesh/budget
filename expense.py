from debt import debt
from month import Month


class Expenses:
    AUTO_INSURANCE = 'Auto Insurance'
    FOOD = 'Food'
    GAS = 'Gas'
    OTHER = 'Kaitlin Other'
    BUFFER = 'Buffer'

    def __init__(self, month: Month, housing, fixed):
        self.month = month
        self.housing = housing
        self.fixed = fixed

    def increment_month(self) -> Month:
        self.month = self.month.next()
        self.housing.increment_month()
        return self.month

    def monthly(self) -> int:
        return self.housing.monthly() + self.fixed_total() + debt(self.month)

    def fixed_total(self) -> int:
        return sum(self.fixed.values())
