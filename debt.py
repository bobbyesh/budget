from month import Month, Monthly


class Debt(Monthly):
    def __init__(self, original_amount, payment, fees=0):
        super().__init__()
        self.original_amount = original_amount
        self.payment = payment
        self.fees = fees

    def monthly(self) -> float:
        if self.owed() == 0:
            return 0

        return self.get_payment() + self.fees

    def get_payment(self):
        return self.payment

    def paid(self) -> float:
        """Returns the amount already paid."""
        delta = self.month - self.start_month
        months_paid = delta.days / 30
        paid = months_paid * self.payment
        return round(min(paid, self.original_amount), 2)

    def owed(self) -> float:
        """Returns the amount owed."""
        return round(self.original_amount - self.paid(), 2)


class GraduatedPaymentLoan(Debt):
    def __init__(self, increase, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.increase = increase

    def get_payment(self):
        intervals = (self.month - self.start_month).days // 365
        return self.payment + (intervals * self.increase)


if __name__ == '__main__':
    t = Month(4, 2018)
    d = Debt(original_amount=2000, payment=100)
    d.month = t
    assert d.monthly() == 100

    car = Debt(original_amount=8700, payment=271, fees=10)
    car.month = t
    assert car.monthly() == 281

    student = GraduatedPaymentLoan(original_amount=50000, payment=160, increase=10)
    student.month = t
    assert student.monthly() == 160

    for _ in range(13):
        t.next()

    print(t)

    assert student.monthly() == 170, 'student.monthly() == %d, not 170' % student.monthly()
    print("Tests passed...")
