from month import Month
from consttimes import START_MONTH


class Debt:
    def __init__(self, start_month: Month, original_amount, payment, fees=0):
        self.start_month = start_month.copy()
        self.current_month = start_month.copy()
        self.original_amount = original_amount
        self.payment = payment
        self.fees = fees

    def monthly(self) -> float:
        if self.owed() == 0:
            return 0

        return self.payment + self.fees

    def paid(self) -> float:
        """Returns the amount already paid."""
        delta = self.current_month - self.start_month
        months_paid = delta.days / 30
        paid = months_paid * self.payment
        return round(min(paid, self.original_amount), 2)

    def owed(self) -> float:
        """Returns the amount owed."""
        return round(self.original_amount - self.paid(), 2)

    def next(self):
        self.current_month.next()


class GraduatedPaymentLoan(Debt):
    def __init__(self, increase, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.increase = increase

    def next(self):
        super().next()
        if (self.current_month - self.start_month).days % 365 == 0:
            self.payment += self.increase


def payment_timeline(remaining, payment, month):
    ret = dict()
    time = month
    while remaining > 0:
        ret[month] = remaining
        remaining -= payment
        time = time.next()

    return ret

'''
car_expenses = payment_timeline(Const.car, Payment.car)
ring_expenses = payment_timeline(Const.ring, Payment.ring)
'''


def payment(monthyear, starting, payment, increment_interval=12, increment_amount=10, increment=False):
    current_monthyear = START_MONTH
    passed = 0
    remaining = starting

    while current_monthyear <= monthyear:
        if increment:
            if passed != 0 and passed % increment_interval == 0:
                payment += increment_amount

        if remaining > 0:
            remaining -= payment
        else:
            return 0

        passed += 1
        current_monthyear = current_monthyear.next()
    return payment


def student(month):
    return payment(month, starting=Const.student, payment=Payment.student, increment=True, increment_amount=10,
                   increment_interval=12)


def car(monthyear):
    return payment(monthyear, starting=Const.car, payment=Payment.car, increment=False)


def ring(monthyear):
    return payment(monthyear, starting=Const.ring, payment=Payment.ring, increment=False)


def debt(month):
    """Return the debt for the month and year of :arg:`monthyear`"""
    return student(month) + car(month) + ring(month)


class DebtManager:
    def __init__(self, month: Month, debts=None):
        self.month = month
        self.debts = debts if debts is not None else []


if __name__ == '__main__':
    t = Month(4, 2018)
    d = Debt(start_month=t, original_amount=2000, payment=100)
    assert d.monthly() == 100

    for i in range(2000 // 100):
        d.next()
        assert d.owed() == round(d.original_amount - d.paid(), 2), '{} == {}'.format(d.owed(), round(d.original_amount - d.paid(), 2))

    assert d.owed() == 0
    assert d.paid() == d.original_amount

    car = Debt(start_month=t, original_amount=8700, payment=271, fees=10)
    assert car.monthly() == 281

    student = GraduatedPaymentLoan(start_month=t, original_amount=50000, payment=160, increase=10)
    assert student.monthly() == 160

    for _ in range(13):
        student.next()

    assert student.monthly() == 170

    print("Tests passed...")



