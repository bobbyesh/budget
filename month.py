import datetime as dt


class Monthly:
    def __init__(self, month, *args, **kwargs):
        self.month = month

    def increment_month(self):
        self.month = self.month.next()
        return self.month


class Month:
    def __init__(self, month, year):
        self.month = month
        self.year = year
        self.datetime = dt.datetime(year, month, 1)

    def __str__(self):
        return self.datetime.strftime('%b %Y')

    def __repr__(self):
        return str(self)

    @staticmethod
    def from_datetime(d):
        return Month(d.month, d.year)

    def __eq__(self, other):
        return self.month == other.month and self.year == other.year

    def __add__(self, other):
        new = self.datetime + other
        return Month.from_datetime(new)

    def __sub__(self, other):
        return self.datetime - other.datetime

    def __lt__(self, other):
        return self.datetime < other.datetime

    def __le__(self, other):
        return self.datetime <= other.datetime

    def __gt__(self, other):
        return self.datetime > other.datetime

    def __ge__(self, other):
        return self.datetime >= other.datetime

    def next(self):
        temp = self.datetime + dt.timedelta(days=30)

        month = temp.month
        year = temp.year
        if month == self.month:
            if month == 12:
                year += 1
                month = 1
            else:
                month += 1

        temp = dt.datetime(year, month, 1)
        return Month.from_datetime(temp)

    def __hash__(self):
        return hash(frozenset((self.month, self.year, self.datetime)))
