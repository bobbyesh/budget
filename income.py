from monthyear import MonthYear, Monthly
from consttimes import START_MONTH_YEAR

class Income(Monthly):
    def __init__(self, monthyear, changes):
        super().__init__(monthyear)
        self.monthyear = monthyear
        self.changes = changes
        self.current_income = sum(change[monthyear] for change in changes)

    def increment_month(self):
        incomes = []
        for change in self.changes:
            times = list(sorted(change.keys()))
            for time in times:
                if time > self.monthyear:
                    incomes.append(change[time])
                    break

        self.current_income = sum(incomes)
        self.monthyear = self.monthyear.next()


if __name__ == '__main__':
    changes1 = {
        START_MONTH_YEAR: 4050,
        MonthYear(2, 2019): 4350,
        MonthYear(5, 2020): 7900,
    }

    changes2 = {
        START_MONTH_YEAR: 1700,
    }

    income = Income(monthyear=START_MONTH_YEAR, changes=[changes1, changes2])
    for _ in range(20):
        income.increment_month()