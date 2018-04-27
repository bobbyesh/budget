from datetime import datetime, timedelta
from month import Month
from consttimes import START_TIME, START_MONTH, END_TIME, END_MONTH_YEAR

class Const:
    car = 8700
    ring = 7200
    student = 50000

class Payment:
    car = 271
    ring = 303
    student = 160


def car_expenses():
    rem = Const.car
    payment = Payment.car
    time = START_TIME

    ret = [rem]
    while rem > 0:
        ret.append(rem)
        rem -= payment

    return ret

def payment_timeline(remaining, payment):
    time = START_MONTH
    ret = dict()

    while remaining > 0:
        ret[time] = remaining
        remaining -= payment
        time = time.next()

    return ret

car_expenses = payment_timeline(Const.car, Payment.car)
ring_expenses = payment_timeline(Const.ring, Payment.ring)

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

def student(monthyear):
    return payment(monthyear, starting=Const.student, payment=Payment.student, increment=True)

def car(monthyear):
    return payment(monthyear, starting=Const.car, payment=Payment.car, increment=False)

def ring(monthyear):
    return payment(monthyear, starting=Const.ring, payment=Payment.ring, increment=False)

def debt(monthyear):
    """Return the debt for the month and year of :arg:`monthyear`"""
    return student(monthyear) + car(monthyear) + ring(monthyear)


if __name__ == '__main__':
    monthyear = Month.from_datetime(datetime(2018, 6, 1))
    for _ in range(13):
        print(debt(monthyear))
        monthyear = monthyear.next()
