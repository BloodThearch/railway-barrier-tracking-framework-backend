import sqlite3
from sqlite3 import Error
import config

# Create the accounts table if it does not exist
def createAccountsTable():
    try:
        conn = sqlite3.connect(config.ACCOUNTS_DB_PATH)
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS accounts (username TEXT type UNIQUE, email TEXT type UNIQUE, password TEXT)')
    except Error as e:
        conn.rollback()
        print(e)
        return -1
    finally:
        conn.commit()
        conn.close()
    return 1

