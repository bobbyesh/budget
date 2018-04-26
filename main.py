from datetime import datetime, timedelta
from monthyear import MonthYear
from collections import defaultdict
from consttimes import START_TIME, END_TIME, END_MONTH_YEAR
from income import income

INIT_SAVINGS = 1000

NET_GAIN = 'NET_GAIN'
TOTAL_SAVINGS = 'TOTAL_SAVINGS'

def net_gain(time):
    return income(time) - expense(time)

def main():
    """Starting here"""
    # Init total savings
    current_total = INIT_SAVINGS

    # Init current time
    current_time = MonthYear.from_datetime(START_TIME)

    # While current time is less than the END_MONTH_YEAR
    while current_time < END_MONTH_YEAR:
        # Update current time's income
        Global.net_gains[current_time][NET_GAIN] = net_gain(current_time)

        # Update current time's expenses
        # Calculate current time's net gain (equal difference between income and expenses)
        # Add current time's net gain to previous month's total savings
        # Store net gain in current month stats
        # Increment current time to next month


main()
