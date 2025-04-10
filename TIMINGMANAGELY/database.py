import sqlite3 as sql
def CONNECT():
    return sql.connect("database.db")

def EXECUTE(SQL, values=(), getResult=False):
    db = CONNECT()
    cur = db.cursor()
    cur.execute(SQL, values)
    if getResult:
        result = cur.fetchall()
    else:
        result = None

    db.commit()
    db.close()
    return result