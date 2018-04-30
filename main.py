import jinja2

from debt import GraduatedPaymentLoan, Debt
from expense import NonHousingExpenses
from housing import Rental
from income import Income
from month import Month
from simulator import Simulator
from utils import bymonth


def projection_tables(months, expenses, incomes, nets, savings):
    month_chunks = bymonth(months)
    expenses_chunks = bymonth(expenses)
    income_chunks = bymonth(incomes)
    net_chunks = bymonth(nets)
    savings_chunks = bymonth(savings)

    tables = []
    for m, e, i, n, s in zip(month_chunks, expenses_chunks, income_chunks, net_chunks, savings_chunks):
        tables.append({
            'headers': [''] + m,
            'rows': [
                ['Expenses'] + e,
                ['Income'] + i,
                ['Net'] + n,
                ['Savings'] + s
            ]
        })

    return tables


def housing_other_expenses_table():
    return {
        'headers': ['Expense', 'Cost'],
        'rows': [
            [key, val] for key, val in housing.other_monthly_expenses().items()
        ],
    }


def housing_stats_table():
    return {
        'headers': ['Rent', housing.rent],
    }


def get_template():
    loader = jinja2.FileSystemLoader(searchpath="./templates")
    env = jinja2.Environment(loader=loader)
    return env.get_template('index.html')


if __name__ == '__main__':
    date = Month(5, 2018)
    debts = [
        GraduatedPaymentLoan(original_amount=50000, payment=160, increase=10),
        Debt(original_amount=8700, payment=271, fees=10),
        Debt(original_amount=7500, payment=303),
    ]

    incomes = [
        Income(net_income=4050),
        Income(net_income=1700),
    ]

    non_housing_expenses = NonHousingExpenses(auto_insurance=72, food=967, gas=80, other=500)
    housing = Rental(rent=1350)
    simulator = Simulator(date=date, debts=debts, non_housing_expenses=non_housing_expenses, housing=housing,
                          duration=3, incomes=incomes, initial_savings=16000)
    simulator.run()

    r = simulator.result
    proj_tables = projection_tables(months=r.months,
                                    expenses=r.expenses,
                                    incomes=r.income,
                                    savings=r.savings,
                                    nets=r.net)

    with open('./out/index.html', 'w') as f:
        template = get_template()
        html = template.render(projection_tables=proj_tables,
                               housing_other_expenses_table=housing_other_expenses_table(),
                               housing_stats_table=housing_stats_table(),
                               housing=housing)
        f.write(html)
