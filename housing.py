import datetime
from month import Month, Monthly
from collections import OrderedDict


class HomeOwned(Monthly):
    AVG_PROPERTY_TAX = 1000

    AVG_APPRECIATION = 5.0 / 100 # Avg annual apprecation for home in Austin, TX
    AVG_MONTHLY_PMI = 200
    HOA = 100
    INSURANCE = 1000 / 12
    UTILITIES = 300

    def __init__(self, value, downpayment, origination_date: Month,interest=4.3, years=30):
        super().__init__()
        self.original_value = value
        self.repairs = (self.original_value * 0.01) / 12
        self.downpayment = downpayment
        self.loan = value - downpayment
        self.interest = interest / 100 / 12
        self.years = years
        self.payments = years * 12
        self.purchased_on = origination_date
        self.final_date = origination_date + datetime.timedelta(30 * 12 * years)
        self.property_tax = HomeOwned.AVG_PROPERTY_TAX / 12

    def monthly(self):
        if self.month > self.final_date:
            return 0

        return self.mortgage + self.calculate_other_expenses()

    @property
    def mortgage(self):
        payment = self.loan * (self.interest * (1 + self.interest) ** self.payments) / ((1 + self.interest) ** self.payments - 1)
        return round(payment, 2)

    @property
    def mortgage_total(self):
        return 30 * self.years * self.mortgage

    def calculate_other_expenses(self):
        pmi = self.PMI()
        return HomeOwned.HOA + self.repairs + self.property_tax + pmi + HomeOwned.UTILITIES + HomeOwned.INSURANCE

    def other_monthly_expenses(self):
        ret = OrderedDict()
        ret['Property Tax'] = self.property_tax
        ret['PMI'] = HomeOwned.AVG_MONTHLY_PMI
        ret['HOA fees'] = HomeOwned.HOA
        ret['Insurance'] = HomeOwned.INSURANCE
        ret['Utilities'] = HomeOwned.UTILITIES
        ret['Repairs'] = self.repairs
        return ret

    def stats(self):
        ret = OrderedDict()
        ret['Mortgage'] = self.mortgage
        ret['Down Payment'] = self.downpayment
        ret['Interest Rate'] = self.interest
        ret['Home Value'] = self.original_value
        return ret

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


class Rental(Monthly):
    category = 'Rental'
    UTILITIES = 250
    INSURANCE = 33

    def __init__(self, rent):
        super().__init__()
        self.rent = rent

    def monthly(self):
        return self.rent + Rental.UTILITIES + Rental.INSURANCE

    def other_monthly_expenses(self):
        ret = OrderedDict()
        ret['Insurance'] = self.INSURANCE
        ret['Utilities'] = self.UTILITIES
        return ret

    def stats(self):
        ret = OrderedDict()
        ret['Rent'] = self.rent
        return ret


if __name__ == '__main__':
    r = Rental(rent=1050)
    print('rental monthly', r.monthly())
