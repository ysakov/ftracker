import os
import webbrowser
from pyecharts.charts import Pie, Bar, Page
from pyecharts import options as opts
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts  

transactions = []

def get_balance():
    expenses = sum(t["amount"] for t in transactions if t["type"] == "Expense")
    incomes = sum(t["amount"] for t in transactions if t["type"] == "Income")
    withdrawals = sum(t["amount"] for t in transactions if t["type"] == "Withdrawal")
    return incomes - expenses - withdrawals

def add_transaction():
    category = input("Enter category (Food, Rent, Transport, Entertainment, Other): ")
    amount = float(input("Enter amount: "))
    transactions.append({"type": "Expense", "category": category, "amount": amount})
    print(f"✅ Added expense {amount} in {category}.\n")

def add_income():
    source = input("Enter income source (Job, Gift, etc): ")
    amount = float(input("Enter income amount: "))
    transactions.append({"type": "Income", "category": source, "amount": amount})
    print(f"✅ Added income {amount} from {source}.\n")

def withdraw():
    amount = float(input("Enter withdrawal amount: "))
    balance = get_balance()
    if amount > balance:
        print(f"❌ Not enough balance! Your current balance is {balance}.\n")
    else:
        transactions.append({"type": "Withdrawal", "category": "Cash", "amount": amount})
        print(f"✅ Withdrawal of {amount} recorded.\n")

def view_summary():
    expenses = sum(t["amount"] for t in transactions if t["type"] == "Expense")
    incomes = sum(t["amount"] for t in transactions if t["type"] == "Income")
    withdrawals = sum(t["amount"] for t in transactions if t["type"] == "Withdrawal")
    balance = incomes - expenses - withdrawals
    print("\n--- SUMMARY ---")
    print(f"Total Income: {incomes}")
    print(f"Total Expenses: {expenses}")
    print(f"Total Withdrawals: {withdrawals}")
    print(f"Balance: {balance}\n")

def view_balance():
    balance = get_balance()
    print(f"\n💰 Current Balance: {balance}\n")

def build_dashboard():
    expense_data = {}
    for t in transactions:
        if t["type"] == "Expense":
            expense_data[t["category"]] = expense_data.get(t["category"], 0) + t["amount"]

    categories = list(expense_data.keys())
    amounts = list(expense_data.values())
    data_pairs = list(zip(categories, amounts))

    pie = Pie()
    if data_pairs:
        pie.add("", data_pairs, radius=["40%", "70%"])
        pie.set_global_opts(
            title_opts=opts.TitleOpts(title="Expenses by Category", pos_left="center"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_left="left")
        ).set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    else:
        pie.set_global_opts(
            title_opts=opts.TitleOpts(title="No Expenses to Display", pos_left="center")
        )

    bar = Bar()
    if categories:
        bar.add_xaxis(categories).add_yaxis("Amount ($)", amounts, category_gap="40%")
        bar.set_global_opts(
            title_opts=opts.TitleOpts(
                title="Expenses Overview",
                pos_left="center",
                pos_top="2%"
            ),
            xaxis_opts=opts.AxisOpts(name="Category"),
            yaxis_opts=opts.AxisOpts(name="Amount ($)"),
            legend_opts=opts.LegendOpts(
                orient="horizontal",
                pos_bottom="0%",
                pos_left="center"
            )
        ).set_series_opts(label_opts=opts.LabelOpts(position="top", formatter="{c}"))
    else:
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="No Expenses to Display", pos_left="center")
        )

    table = Table()
    headers = ["Type", "Category", "Amount ($)"]
    rows = [[t["type"], t["category"], str(t["amount"])] for t in transactions]
    if rows:
        table.add(headers, rows).set_global_opts(
            title_opts=ComponentTitleOpts(title="Transaction History")
        )
    else:
        table.add(headers, [["-", "-", "-"]]).set_global_opts(
            title_opts=ComponentTitleOpts(title="No Transactions Yet")
        )

    page = Page()
    page.add(pie, bar, table)

    html_file = "expenses_dashboard.html"
    page.render(html_file)

    abs_path = os.path.abspath(html_file)
    file_url = f"file://{abs_path}"

    print(f"\n📊 Dashboard saved to: {abs_path}")
    print(f"Opening in browser: {file_url}\n")
    webbrowser.open(file_url)

def main():
    while True:
        print("=== Finance Tracker ===")
        print("1. Add Expense")
        print("2. Add Income")
        print("3. Withdraw")
        print("4. View Summary")
        print("5. View Balance")
        print("6. Generate Dashboard")
        print("7. Quit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            add_income()
        elif choice == "3":
            withdraw()
        elif choice == "4":
            view_summary()
        elif choice == "5":
            view_balance()
        elif choice == "6":
            build_dashboard()
        elif choice == "7":
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice, try again.\n")

if __name__ == "__main__":
    main()
