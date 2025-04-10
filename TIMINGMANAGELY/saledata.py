import sqlite3
from datetime import time

# Connect to local database and set up cursor for execution of SQL #
db = sqlite3.connect("database.db")
cur = db.cursor()

SQL = """INSERT INTO Products (product_name, amount_stocked, perish_date, min_amount)
            VALUES (?, ?, ?, ?)"""
products = [("Product 1", 45, None, 10),
            ("Product 2", 12, "2025-04-01", None),
            ("Product 2", 20, "2025-05-01", None),
            ("Product 3", 100, None, 50)]

for product in products:
    cur.execute(SQL, product)

SQL = """INSERT INTO Sales (product_id, employee_id, date, amount)
            VALUES (?, ?, ?, ?)"""
sales = [(1, 1, "2025-03-24", 10),
         (1, 1, "2025-03-25", 2),
         (2, 3, "2025-03-25", 5),
         (4, 2, "2025-03-26", 12)]

for sale in sales:
    cur.execute(SQL, sale)

SQL = """INSERT INTO ProductCosts (product_id, cost)
            VALUES (?, ?)"""
costs = [(1, 10.99),
            (2, 12.99),
            (3, 12.99),
            (4, 3.99)]

for cost in costs:
    cur.execute(SQL, cost)

db.commit()
db.close()