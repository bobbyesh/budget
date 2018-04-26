# Formula for mortgage calculator
# M = L(I(1 + I)**N) / ((1 + I)**N - 1)
# M = Monthly Payment, L = Loan, I = Interest, N = Number of payments, ** = exponent
import datetime
from monthyear import MonthYear

class HomeOwned:
    avg_appreciation = 5.0 / 100 # Avg annual apprecation for home in Austin, TX

    def __init__(self, value, downpayment, purchased_on: MonthYear, interest=4.3, years=30):
        self.value = value
        self.downpayment = downpayment
        self.loan = value - downpayment
        self.interest = interest / 100 / 12
        self.years = years
        self.payments = years * 12
        self.purchased_on = purchased_on
        self.final_date = purchased_on + datetime.timedelta(30 * 12 * years)


    def on(self, monthyear):
        if monthyear > self.final_date:
            return 0

        return self.mortgage + self.other_expenses()

    @property
    def mortgage(self):
        payment = self.loan * (self.interest * (1 + self.interest) ** self.payments) / ((1 + self.interest) ** self.payments - 1)
        return round(payment, 2)

    @property
    def mortgage_total(self):
        return 30 * self.years * self.mortgage

    def other_expenses(self, monthyear):
        HOA = 100
        repairs = (self.value * 0.01) / 12 # One percent per year
        taxes = 1000 # Average for Austin, TX
        pmi = self.PMI(monthyear)

    def equity_by(self, monthyear):
        return self.value - self.paid_by(monthyear)

    def paid_by(self, monthyear):
        delta = monthyear.datetime - self.purchased_on.datetime
        months = delta.days // 30
        paid = months * self.mortgage
        return paid if paid < self.mortgage_total else self.mortgage_total

    def equity_by(self, monthyear):
        return self.value_by(monthyear) - self.remaining_balance(payments=years_passed*12)

    def value_by(self, monthyear):
        years_passed = (monthyear - self.purchased_on).days / 30 / 12
        if years_passed >= 30:
            return 0

        value = self.value
        for _ in range(years_passed):
            value *= (1 + HomeOwned.avg_appreciation)

        return value

    def PMI(self, monthyear):
        ratio = self.balance_by(monthyear) / self.value

    def future_value(self, length):
        # FVn = P[(1+c)n - 1]/c
        return (self.mortgage * (1 + self.interest) * length - 1) / self.interest

    def balance_by(self, monthyear):
        payments = self.payments_by(monthyear)


    def payments_by(self, monthyear):
        return (monthyear - self.purchased_on).days / 30

    def remaining_balance(self, payments):
        fv_original = (self.value - self.downpayment) * ((1 + self.interest) ** payments)
        fv_annuity = self.mortgage * (((1 + self.interest) ** payments - 1) / self.interest)
        return fv_original - fv_annuity

if __name__ == '__main__':
    home = HomeOwned(value=350000, downpayment=35000, purchased_on=MonthYear(4, 2018), interest=4.1)
    print("The monthly mortgage payment is", home.mortgage)
    print("remaining = ", home.remaining_balance(payments=30*12))
