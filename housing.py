import datetime
from month import Month


class Housing:
    def __init__(self, movein: Month, *args, **kwargs):
        self.month = movein

    def increment_month(self):
        self.month = self.month.next()
        return self.month

    def monthly(self):
        raise NotImplementedError("Must implement monthly for Housing subclass")


class HomeOwned(Housing):
    AVG_PROPERTY_TAX = 1000

    AVG_APPRECIATION = 5.0 / 100 # Avg annual apprecation for home in Austin, TX
    AVG_MONTHLY_PMI = 200
    HOA = 100
    INSURANCE = 1000 / 12
    UTILITIES = 300

    def __init__(self, value, downpayment, purchased_on: Month, interest=4.3, years=30):
        super().__init__(purchased_on)
        self.original_value = value
        self.downpayment = downpayment
        self.loan = value - downpayment
        self.interest = interest / 100 / 12
        self.years = years
        self.payments = years * 12
        self.purchased_on = purchased_on
        self.final_date = purchased_on + datetime.timedelta(30 * 12 * years)

    def monthly(self):
        if self.month > self.final_date:
            return 0

        return self.mortgage + self.other_expenses()

    @property
    def mortgage(self):
        payment = self.loan * (self.interest * (1 + self.interest) ** self.payments) / ((1 + self.interest) ** self.payments - 1)
        return round(payment, 2)

    @property
    def mortgage_total(self):
        return 30 * self.years * self.mortgage

    def other_expenses(self):
        repairs = (self.original_value * 0.01) / 12 # One percent per year
        taxes = HomeOwned.AVG_PROPERTY_TAX / 12 # Average for Austin, TX
        pmi = self.PMI()
        return HomeOwned.HOA + repairs + taxes + pmi + HomeOwned.UTILITIES + HomeOwned.INSURANCE

    def PMI(self):
        ratio = self.balance() / self.original_value
        return 0 if ratio >= .20 else HomeOwned.AVG_MONTHLY_PMI

    def equity(self):
        return self.original_value - self.balance()

    def amount_paid(self):
        delta = self.month.datetime - self.purchased_on.datetime
        months = delta.days // 30
        paid = months * self.mortgage
        return paid if paid < self.mortgage_total else self.mortgage_total

    def current_value(self):
        years_passed = (self.month - self.purchased_on).days / 30 / 12
        if years_passed >= 30:
            return 0

        value = self.original_value
        for _ in range(int(years_passed)):
            value *= (1 + HomeOwned.AVG_APPRECIATION)

        return value

    def balance(self):
        payments = self.payments_made()
        fv_original = (self.original_value - self.downpayment) * ((1 + self.interest) ** payments)
        fv_annuity = self.mortgage * (((1 + self.interest) ** payments - 1) / self.interest)
        return fv_original - fv_annuity

    def payments_made(self):
        return (self.month - self.purchased_on).days / 30


class Rental(Housing):
    UTILITIES = 250
    INSURANCE = 33

    def __init__(self, rent, movein):
        super().__init__(movein)
        self.rent = rent

    def monthly(self):
        return self.rent + Rental.UTILITIES + Rental.INSURANCE


if __name__ == '__main__':
    r = Rental(rent=1050, movein=Month(9, 2018))
    print('rental monthly', r.monthly())