from debt import debt
from monthyear import MonthYear


class Expenses:
    def __init__(self):
        self.housing = object()

    def on(self, monthyear):
        return debt(monthyear) + \
               self.housing.on(monthyear) + \
               self.other_expenses(monthyear)

    def other_expenses(self, monthyear):
        return 0
