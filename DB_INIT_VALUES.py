# File used to add initial values to the database #
# Import libraries #
import sqlite3
from datetime import time

# Connect to local database and set up cursor for execution of SQL #
db = sqlite3.connect("database.db")
cur = db.cursor()

# Add employees to employee table #
SQL = """INSERT INTO Employees (employee_name, employee_email, employee_password)
            VALUES (?, ?, ?);"""
EmployeeList = [["Employee 1", "employee1@mail.com", "Employee1Password"],
                ["Employee 2", "employee2@mail.com", "Employee2Password"],
                ["Employee 3", "employee3@mail.com", "Employee3Password"]]
for employee in EmployeeList:
    cur.execute(SQL, (employee[0], employee[1], employee[2]))

# Add managers to manager table
SQL = """INSERT INTO Managers (manager_name, manager_email, manager_password)
            VALUES (?, ?, ?);"""
ManagerList = [["Manager 1", "manager1@mail.com", "Manager1Password"],
                ["Manager 2", "manager2@mail.com", "Manager2Password"]]

for manager in ManagerList:
    cur.execute(SQL, (manager[0], manager[1], manager[2]))


# Add owner to owner table
SQL = """INSERT INTO BusinessOwner (owner_name, owner_email, owner_password)
            VALUES (?, ?, ?);"""
OwnerList = [["Owner", "owner@mail.com", "OwnerPassword"]]

for owner in OwnerList:
    cur.execute(SQL, (owner[0], owner[1], owner[2]))

# Add business info #
cur.execute("INSERT INTO Business (business_name) VALUES (?)", ("Test Small Business!",))

# Add accounts to account table #
SQL = """INSERT INTO Accounts (account_type, account_email, type_id)
            VALUES (?, ?, ?);"""
AccountList = [ ["owner", "owner@mail.com", "1"],
                ["manager", "manager1@mail.com", "1"],
                ["manager", "manager2@mail.com", "2"],
                ["employee", "employee1@mail.com", "1"],
                ["employee", "employee2@mail.com", "2"],
                ["employee", "employee3@mail.com", "3"]]

for account in AccountList:
    cur.execute(SQL, (account[0], account[1], account[2]))



# Add products #
SQL = """INSERT INTO Products (product_name, amount_stocked, perish_date, min_amount)
            VALUES (?, ?, ?, ?)"""
products = [("Product 1", 45, None, 10),
            ("Product 2", 12, "2025-04-01", None),
            ("Product 2", 20, "2025-05-01", None),
            ("Product 3", 100, None, 50)]

for product in products:
    cur.execute(SQL, product)

# Add sales #
SQL = """INSERT INTO Sales (product_id, employee_id, date, amount)
            VALUES (?, ?, ?, ?)"""
sales = [(1, 1, "2025-03-24", 10),
         (1, 1, "2025-03-25", 2),
         (2, 3, "2025-03-25", 5),
         (4, 2, "2025-03-26", 12)]

for sale in sales:
    cur.execute(SQL, sale)


# Add product costs #
SQL = """INSERT INTO ProductCosts (product_id, cost)
            VALUES (?, ?)"""
costs = [(1, 10.99),
            (2, 12.99),
            (3, 12.99),
            (4, 3.99)]

for cost in costs:
    cur.execute(SQL, cost)


# Add employee pay rates #
SQL = """INSERT INTO PayRates (employee_id, hourly_rate)
            VALUES (?, ?);"""
payList = [[1, 10.55],
             [2, 12.37],
             [3, 11.50]]

for pay in payList:
    cur.execute(SQL, (pay[0], pay[1]))

db.commit()
db.close()

