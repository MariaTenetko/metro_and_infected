import pandas as pd
import glob

file_names = glob.glob("../Table/hw_session*.csv")

for file_name in file_names:
    sessions_df = pd.read_csv(file_name)
    for _, session in sessions_df.iterrows():
        start_timestamp = session["start_ts"]
        stop_timestamp = session["end_ts"]
        duration = stop_timestamp - start_timestamp
        if duration % 180 != 0:
            print(session)
