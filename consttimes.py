from datetime import datetime
from monthyear import MonthYear

START_TIME = datetime(2018, 4, 1)
END_TIME = datetime(2020, 12, 1)

START_MONTH_YEAR = MonthYear.from_datetime(START_TIME)
END_MONTH_YEAR = MonthYear.from_datetime(END_TIME)
