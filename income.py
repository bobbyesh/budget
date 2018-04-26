from datetime import datetime, timedelta
from monthyear import MonthYear
from consttimes import START_TIME, END_TIME, END_MONTH_YEAR

income1_start = 4050
income1_changes = {
    MonthYear.from_datetime(START_TIME): income1_start,
    MonthYear.from_datetime(datetime(2019, 2, 1)): 4350,
    MonthYear.from_datetime(datetime(2020, 5, 1)): 7900,
}

income2_start = 1700
income2_changes = {
    MonthYear.from_datetime(START_TIME): income2_start,
}

INCOME1 = 'INCOME1'
INCOME2 = 'INCOME2'


def initialize_income():
    incomes = {
        INCOME1: dict(),
        INCOME2: dict()
    }

    temp = MonthYear.from_datetime(START_TIME)
    prev_income1, prev_income2 = income1_start, income2_start

    while temp.datetime < END_MONTH_YEAR.datetime:
        if temp in income1_changes:
            incomes[INCOME1][temp] = income1_changes[temp]
        else:
            incomes[INCOME1][temp] = prev_income1

        if temp in income2_changes:
            incomes[INCOME2][temp] = income2_changes[temp]
        else:
            incomes[INCOME2][temp] = prev_income2

        temp = temp.next()

    return incomes


class Global:
    income = initialize_income()
    assert len(income[INCOME1]) ==  len(income[INCOME2])


def income(monthyear):
    """Returns income.  income(1, my) returns income 1 for monthyear `my`, income(2, my) will return income 2"""
    return Global.income[INCOME1][monthyear] + Global.income[INCOME2][monthyear]


if __name__ == '__main__':
    print(Global.income)
