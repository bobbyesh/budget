from month import Month, Monthly
from consttimes import START_MONTH


class Income(Monthly):
    def __init__(self, month, initial_incomes, changes):
        super().__init__(month)
        self.month = month
        self.changes = changes
        self.current_incomes = initial_incomes

    @property
    def current_income(self):
        return sum(self.current_incomes.values())

    def monthly(self):
        return self.current_income

    def update_current_incomes(self):
        for income_id, change in self.changes.items():
            for month, new_income in change.items():
                if month == self.month:
                    self.current_incomes[income_id] = new_income

    def increment_month(self):
        self.month = self.month.next()
        self.update_current_incomes()


def test():
    changes = {
        Month(2, 2019): 4350,
        Month(5, 2020): 7900,
    }

    income = Income(month=START_MONTH, initial_incomes={0: 4050, 1: 1700}, changes={0: changes})
    for _ in range(40):
        income.increment_month()
        print('month', income.month)
        print(income.monthly())


if __name__ == '__main__':
    test()