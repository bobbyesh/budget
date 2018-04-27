from debt import debt
from monthyear import MonthYear

class Expenses:
    fixed = {
        'Auto Insurance': 72,
        'Food': 967,
        'Gas': 80,
        'Kaitlin Other': 500,
        'Buffer': 300,
    }


    def __init__(self, monthyear: MonthYear, housing):
        self.monthyear = monthyear
        self.housing = housing

    def increment_month(self) -> MonthYear:
        self.monthyear = self.monthyear.next()
        self.housing.increment_month()
        return self.monthyear

    def monthly(self) -> int:
        return self.housing.monthly() + self.fixed_total() + debt(self.monthyear)

    def fixed_total(self) -> int:
        return sum(Expenses.fixed.values())
