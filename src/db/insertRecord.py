import sqlite3
from sqlite3 import Error
import config

# Insert an account into accounts table
# todo: return if email is not unique or username
# todo: return if password does not follow rules
def insertAccount(data):
    try:
        conn = sqlite3.connect(config.ACCOUNTS_DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO accounts (username,email,password) VALUES (?,?,?)',
                  (data['username'], data['email'], data['password']))
    except Error as e:
        conn.rollback()
        print(e)
        return -1
    finally:
        conn.commit()
        conn.close()
    return 1