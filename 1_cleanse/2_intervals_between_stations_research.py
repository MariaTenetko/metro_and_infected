import pandas as pd
import glob

file_names = glob.glob("../Table/train_trek*.csv")

for file_name in file_names:
    line_number = file_name[19:-4]
    treks_df = pd.read_csv(file_name)

    timestamp_deltas = []
    previous_timestamp = 0

    for _, row in treks_df.iterrows():
        if previous_timestamp == 0:
            previous_timestamp = row["timestamp"]
            continue
        else:
            timestamp_delta = row["timestamp"] - previous_timestamp
            previous_timestamp = row["timestamp"]
            if timestamp_delta > 0:
                # Отсекаем переходы от последней поездки предыдущего поезда к первой поездке следующего поезда
                timestamp_deltas.append(timestamp_delta)

    print(
        f"На линии {line_number} "
        f"минимальный интервал - {min(timestamp_deltas)}, "
        f"максимальный интервал - {max(timestamp_deltas)}, "
        f"средний интервал - {sum(timestamp_deltas) / len(timestamp_deltas)}"
    )

