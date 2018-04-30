import typing
from collections import namedtuple

from debt import Debt, GraduatedPaymentLoan
from expense import NonHousingExpenses
from housing import Rental
from income import Income
from month import Month


class SimulationResult(namedtuple('SimulationResults', ['months', 'income', 'net', 'savings', 'expenses'])):
    def __str__(self):
        return 'SimulationResults<{} to {}>'.format(self.months[0], self.months[-1])


class Simulator:
    INCOME = 'Income'
    NET = 'Net'
    SAVINGS = 'Savings'
    EXPENSES = 'Expenses'
    MONTHS = 'Months'

    def __init__(self, date: Month, duration: int, incomes: typing.List[Income], debts: typing.List[Debt],
                 non_housing_expenses: NonHousingExpenses, housing, initial_savings: int):
        self.month = date
        self.debts = debts
        self.non_housing_expenses = non_housing_expenses
        self.housing = housing
        self.duration = duration
        self.incomes = incomes
        self.initial_savings = initial_savings
        self.result = SimulationResult(months=[], income=[], net=[], savings=[], expenses=[])
        self.sync()

    def sync(self):
        """Sets all monthly debts/incomes to the simulator's current date"""

        for debt in self.debts:
            debt.month = self.month

        for income in self.incomes:
            income.month = self.month

        self.housing.month = self.month

    def run(self) -> None:
        for _ in range(self.duration * 12):
            expenses = sum(self.non_housing_expenses) + \
                       sum(debt.monthly() for debt in self.debts) + self.housing.monthly()
            income = sum(income.monthly() for income in self.incomes)
            net = income - expenses
            self.store(net, expenses, income)
            self.month.next()

        self.calculate_savings()

    def store(self, net, expenses, income):
        self.result.net.append(net)
        self.result.months.append(self.month.copy())
        self.result.expenses.append(expenses)
        self.result.income.append(income)

    def calculate_savings(self):
        savings = self.initial_savings
        for net in self.result.net:
            savings += net
            self.result.savings.append(savings)


def main():
    date = Month(5, 2018)
    debts = [
        GraduatedPaymentLoan(original_amount=50000, payment=160, increase=10),
        Debt(original_amount=8700, payment=271, fees=10),
        Debt(original_amount=7500, payment=303),
    ]

    incomes = [
        Income(net_income=4050),
        Income(net_income=1700),
    ]

    non_housing_expenses = NonHousingExpenses(auto_insurance=72, food=967, gas=80, other=500)
    housing = Rental(rent=1350)
    simulator = Simulator(date=date, debts=debts, non_housing_expenses=non_housing_expenses, housing=housing,
                          duration=3, incomes=incomes, initial_savings=16000)
    simulator.run()


if __name__ == '__main__':
    main()
