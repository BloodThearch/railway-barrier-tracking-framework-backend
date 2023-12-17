import os

CWD = os.getcwd() # Current working directory

# Database variables
DATABASE_DIR_PATH = os.path.join(CWD, 'db')
ACCOUNTS_DB_PATH = os.path.join(DATABASE_DIR_PATH, 'accounts.db')
PRED_XLSX_PATH = os.path.join(DATABASE_DIR_PATH, "combined_forecast.xlsx")

# Barrier Status File Path
BARRIER_STATUS_FILE_PATH = os.path.join(CWD, 'barrierStatus.txt')