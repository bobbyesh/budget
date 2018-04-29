import jinja2

from debt import GraduatedPaymentLoan, Debt
from month import Month
from income import Income
from housing import HomeOwned, Rental
from expense import Expenses


def bymonth(anylist: list):
    for i in range(0, len(anylist), 12):
        yield anylist[i:i + 12]


class Const:
    INCOME = 'Income'
    NET = 'Net'
    SAVINGS = 'Savings'
    EXPENSES = 'Expenses'
    MONTHS = 'Months'


housing = Rental(rent=1350, move_in=Month(5, 2018))


def run_simulation(years=3, initial_savings=1000):
    current_month = housing.month
    student = GraduatedPaymentLoan(start_month=current_month, original_amount=50000, payment=160, increase=10)
    car = Debt(start_month=current_month, original_amount=8700, payment=271, fees=10)
    ring = Debt(start_month=current_month, original_amount=7500, payment=303)

    incomes = [
        Income(month=current_month, net_income=4050, changes=None),
        Income(month=current_month, net_income=1600, changes=None)
    ]

    fixed_expenses = {
        Expenses.AUTO_INSURANCE: 72,
        Expenses.FOOD: 967,
        Expenses.GAS: 80,
        Expenses.OTHER: 500,
    }

    results = {
        Const.INCOME: [],
        Const.NET: [],
        Const.SAVINGS: [],
        Const.EXPENSES: [],
        Const.MONTHS: [],
    }

    fixed_ = sum(fixed_expenses.values())
    for _ in range(years * 12):
        expenses = fixed_ + housing.monthly() + student.monthly() + car.monthly() + ring.monthly()
        income = sum(income.monthly() for income in incomes)
        net = income - expenses

        results[Const.NET].append(net)
        results[Const.MONTHS].append(current_month.copy())
        results[Const.EXPENSES].append(expenses)
        results[Const.INCOME].append(income)

        current_month.next()

    savings = initial_savings
    for net in results[Const.NET]:
        savings += net
        results[Const.SAVINGS].append(savings)

    return results


def projection_tables(months, expenses, incomes, nets, savings):
    month_chunks = list(bymonth(months))
    expenses_chunks = list(bymonth(expenses))
    income_chunks = list(bymonth(incomes))
    net_chunks = list(bymonth(nets))
    savings_chunks = list(bymonth(savings))

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
    simulation_results = run_simulation()
    proj_tables = projection_tables(months=simulation_results[Const.MONTHS],
                                    expenses=simulation_results[Const.EXPENSES],
                                    incomes=simulation_results[Const.INCOME],
                                    savings=simulation_results[Const.SAVINGS],
                                    nets=simulation_results[Const.NET])

    with open('./out/index.html', 'w') as f:
        template = get_template()
        html = template.render(projection_tables=proj_tables,
                               housing_other_expenses_table=housing_other_expenses_table(),
                               housing_stats_table=housing_stats_table(),
                               housing=housing)
        f.write(html)
