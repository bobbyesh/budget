from datetime import datetime
from month import Month

START_TIME = datetime(2018, 4, 1)
END_TIME = datetime(2020, 12, 1)

START_MONTH = Month(4, 2018)
END_MONTH_YEAR = Month.from_datetime(END_TIME)
