# File used to initialise, and reset database if needed #
# Import libraries #
import sqlite3

# Connect to local database and set up cursor for execution of SQL #
db = sqlite3.connect("database.db")
cur = db.cursor()

# Table Creations #

# Accounts Table #
SQL = """CREATE TABLE IF NOT EXISTS Accounts (
            account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_type VARCHAR(16) NOT NULL,
            account_email VARCHAR(64),
            type_id INTEGER NOT NULL
        );"""

cur.execute(SQL)

# Employees Table #
SQL = """CREATE TABLE IF NOT EXISTS Employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name VARCHAR(32) NOT NULL,
            employee_email VARCHAR(64) NOT NULL,
            employee_password VARCHAR(64) NOT NULL
        );"""

cur.execute(SQL)

# Managers Table #
SQL = """CREATE TABLE IF NOT EXISTS Managers (
            manager_id INTEGER PRIMARY KEY AUTOINCREMENT,
            manager_name VARCHAR(32) NOT NULL,
            manager_email VARCHAR(64) NOT NULL,
            manager_password VARCHAR(64) NOT NULL
        );"""

cur.execute(SQL)

# BusinessOwner Table #
SQL = """CREATE TABLE IF NOT EXISTS BusinessOwner (
            owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_name VARCHAR(32) NOT NULL,
            owner_email VARCHAR(64) NOT NULL,
            owner_password VARCHAR(64) NOT NULL
        );"""

cur.execute(SQL)

# Shifts Table #
SQL = """CREATE TABLE IF NOT EXISTS Shifts (
            shift_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            date DATE NOT NULL,
            starttime TIME NOT NULL,
            endtime TIME NOT NULL,
            accepted INTEGER NOT NULL
        );"""

cur.execute(SQL)

# Business Info Table #
SQL = """CREATE TABLE IF NOT EXISTS Business (
            business_name VARCHAR(32)
        )"""
cur.execute(SQL)

# Shift template Table #
SQL = """CREATE TABLE IF NOT EXISTS ShiftTemplate (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day INTEGER NOT NULL,
            starttime TEXT NOT NULL,
            endtime TEXT NOT NULL,
            preffered_employee INTEGER
        );"""
cur.execute(SQL)

# Group Message Table
SQL = """CREATE TABLE IF NOT EXISTS GroupMessages (
            group_message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            reply_id INTEGER,
            message VARCHAR(255) NOT NULL
        );"""
cur.execute(SQL)

# Direct Message Table
SQL = """CREATE TABLE IF NOT EXISTS DirectMessages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            message VARCHAR(255) NOT NULL
        );"""
cur.execute(SQL)

# Reply Message Table
SQL = """CREATE TABLE IF NOT EXISTS ReplyMessage (
            reply_id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER NOT NULL,
            message VARCHAR(255) NOT NULL
        );"""
cur.execute(SQL)

# Holiday Request Table
SQL = """CREATE TABLE IF NOT EXISTS HolidayRequest (
            holiday_request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            startdate DATE NOT NULL,
            enddate DATE NOT NULL,
            reason VARCHAR(128),
            accepted BOOL
        );"""
cur.execute(SQL)

# Sales Table
SQL = """CREATE TABLE IF NOT EXISTS Sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            employee_id INTEGER NOT NULL,
            date DATE NOT NULL,
            amount INTEGER NOT NULL
        );"""
cur.execute(SQL)

# Products table
SQL = """CREATE TABLE IF NOT EXISTS Products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name VARCHAR(64) NOT NULL,
            amount_stocked INTEGER,
            perish_date DATE,
            min_amount INTEGER
        );"""
cur.execute(SQL)

# Employee Pay Table
SQL = """CREATE TABLE IF NOT EXISTS PayRates (
            salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            hourly_rate DECIMAL NOT NULL
        );"""
cur.execute(SQL)

# Product Cost Table
SQL = """CREATE TABLE IF NOT EXISTS ProductCosts (
            product_id INTEGER NOT NULL,
            cost DECIMAL NOT NULL
        );"""
cur.execute(SQL)

# Calendar Table
SQL = """CREATE TABLE IF NOT EXISTS Calendar (
            calendar_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name VARCHAR(255) NOT NULL,
            date DATE NOT NULL
        );"""
cur.execute(SQL)

db.commit()
db.close()