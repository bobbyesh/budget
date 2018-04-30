import typing

from month import Month, Monthly

ChangeType = typing.List[typing.Tuple[Month, typing.SupportsInt]]


class Income(Monthly):
    def __init__(self, net_income: typing.Union[float, int], changes: ChangeType = None):
        super().__init__()
        self.changes = changes if changes is not None else [tuple()]
        self.net_income = net_income

    def monthly(self):
        return self.net_income

    def update_current_incomes(self):
        for month, new_income in self.changes:
            if month == self.month:
                self.net_income = new_income


def test():
    month = Month(4, 2018)
    changes = [
        (Month(2, 2019), 4350),
        (Month(5, 2020), 7900),
    ]

    income = Income(net_income=4050, changes=changes)
    income.month = month
    for _ in range(40):
        print('month', income.month)
        print(income.monthly())
        month.next()


if __name__ == '__main__':
    test()
