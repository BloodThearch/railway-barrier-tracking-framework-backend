import pandas as pd
from datetime import datetime, time
import config


def checkGateStatus():
    h = 6
    with open(config.BARRIER_STATUS_FILE_PATH, 'r') as file:
        file_content = file.read()
        h = int(file_content)
        
    current_date = datetime(2023, 12, 17, h, 20, 3).strftime('%Y-%m-%d')
    current_time = datetime(2023, 12, 17, h, 20, 3).strftime('%H:%M:%S')

    file_path = config.PRED_XLSX_PATH
    df = pd.read_excel(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    new_df = pd.DataFrame({
        'Datetime at which crossing were closed': df.apply(lambda row: pd.to_datetime(f"{row['Date']} {row['Time at which crossing were closed']}"), axis=1),
        'Datetime at which crossing were opened': df.apply(lambda row: pd.to_datetime(f"{row['Date']} {row['Time at which crossing were opened']}"), axis=1),
        'Datetime the crossing was closed': df.apply(lambda row: pd.to_datetime(f"{row['Date']} {row['Time the crossing was closed']}"), axis=1),
        'Train Number': df['Train Number']
    })
    new_df['Date'] = new_df['Datetime at which crossing were closed'].dt.strftime('%Y-%m-%d')

    return _check_crossing_status(current_date, current_time, new_df)

def _check_crossing_status(input_date, input_time, df):
    filtered_df = df[df['Date'] == input_date]
    datetime_input = datetime.strptime(f"{input_date} {input_time}", "%Y-%m-%d %H:%M:%S")

    for index, row in filtered_df.iterrows():
        time_closed=row['Datetime at which crossing were closed']
        time_opened=row['Datetime at which crossing were opened']
        if time_closed <= datetime_input <= time_opened:
            return 0
    return 1
