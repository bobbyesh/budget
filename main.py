from consttimes import START_TIME, START_MONTH_YEAR, END_TIME, END_MONTH_YEAR
from monthyear import MonthYear
from income import income
from housing import HomeOwned, Rental
from expense import Expenses


INIT_SAVINGS = 1000
NET_GAIN = 'NET_GAIN'
TOTAL_SAVINGS = 'TOTAL_SAVINGS'

def main():
    # Init total savings
    current_total = INIT_SAVINGS

    # Init current time
    current_time = START_MONTH_YEAR

    home = Rental(1350, current_time)
    expenses = Expenses(monthyear=current_time, housing=home)

    # While current time is less than the END_MONTH_YEAR
    while expenses.monthyear < END_MONTH_YEAR:
        # Update current time's income
        monthly_net = income(expenses.monthyear) - expenses.monthly()
        current_total += monthly_net
        print(monthly_net)
        if monthly_net > 5000:
            print(expenses.monthyear)
            # import pdb;pdb.set_trace()
            pass

        expenses.increment_month()

    print("By {} your savings will be {}".format(expenses.monthyear, current_total))


main()
