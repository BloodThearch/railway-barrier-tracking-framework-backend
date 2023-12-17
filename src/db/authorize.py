import sqlite3
from sqlite3 import Error
import config

def checkAccount(data):
    try:
        conn = sqlite3.connect(config.ACCOUNTS_DB_PATH)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) as C FROM accounts WHERE username = ? AND password = ?', 
                  (data['username'], data['password']))
        # check if count is > 0
        rows = c.fetchall()
        row = rows[0]
        print(row[0])
        if row[0] == 0:
            return 0
    except Error as e:
        print(e)
        return -1
    finally:
        conn.close()
    return 1