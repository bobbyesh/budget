import typing

from month import Month, Monthly
from consttimes import START_MONTH


class Income(Monthly):
    def __init__(self, month: Month, net_income: typing.Union[float, int],
                 changes: typing.Tuple[Month, typing.SupportsInt] = None):
        super().__init__(month)
        self.month = month.copy()
        self.changes = changes if changes is not None else [tuple()]
        self.net_income = net_income

    def monthly(self):
        return self.net_income

    def update_current_incomes(self):
        for month, new_income in self.changes:
            if month == self.month:
                self.net_income = new_income

    def increment_month(self):
        self.month.next()
        self.update_current_incomes()


def test():
    changes = [
        (Month(2, 2019), 4350),
        (Month(5, 2020), 7900),
    ]

    income = Income(month=START_MONTH, net_income=4050, changes=changes)
    for _ in range(40):
        income.increment_month()
        print('month', income.month)
        print(income.monthly())


if __name__ == '__main__':
    test()
