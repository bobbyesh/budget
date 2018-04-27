from consttimes import START_TIME, START_MONTH, END_TIME, END_MONTH_YEAR
from month import Month
from income import Income
from housing import HomeOwned, Rental
from expense import Expenses


INIT_SAVINGS = 1000


def get_expenses(current_time):
    home = Rental(1350, current_time)
    fixed = {Expenses.AUTO_INSURANCE: 72, Expenses.FOOD: 967, Expenses.GAS: 80, Expenses.OTHER: 500,
             Expenses.BUFFER: 300, }
    return Expenses(month=current_time, housing=home, fixed=fixed)


def get_income(current_time):
    changes = {
        0: {
            Month(2, 2019): 4350,
            Month(5, 2020): 7900,
        },
    }

    return Income(month=current_time, initial_incomes={0: 4050, 1: 1700}, changes=changes)


def main():
    # Init total savings
    current_total = INIT_SAVINGS

    # Init current time
    current_time = Month(4, 2018)

    # Initialize income and expenses
    income = get_income(current_time)
    expenses = get_expenses(current_time)

    # Accumulate savings
    while expenses.month < Month(5, 2018):
        monthly_net = income.monthly() - expenses.monthly()
        current_total += monthly_net
        expenses.increment_month()
        income.increment_month()

    print("By {} your savings will be {}".format(expenses.month, current_total))


main()
