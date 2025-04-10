import sqlite3
from datetime import time

# Connect to local database and set up cursor for execution of SQL #
db = sqlite3.connect("database.db")
cur = db.cursor()
SQL = """DROP TABLE IF EXISTS Products"""
cur.execute(SQL)
db.commit()
db.close()