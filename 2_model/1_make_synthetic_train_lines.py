import pandas as pd
from datetime import datetime
from transliterate import translit

line_numbers = range(1, 18)
first_train_number = 1
directions = ["there", "back"]

stations_file = "../Dict/json_stations.json"
stations_df = pd.read_json(stations_file)

# Референс:
# line_id,train_id,station_id,timestamp,dt
# 1,1,40,1598939431,2020-09-01 05:50:31

# Самая ранняя дата во всех файлах: ./train_trek17.csv:17,187,61,1598939403,2020-09-01 05:50:03
first_timestamp = 1598925600 # Tue Sep 01 2020 05:00:00 GMT+0300 (Москва, стандартное время)

# Самая поздняя дата во всех файлах: ./train_trek14.csv:14,238,224,1600076137,2020-09-14 09:35:37
last_timestamp = 1600065360 # Mon Sep 14 2020 09:36:00 GMT+0300 (Москва, стандартное время)

section_time = 3 * 60 # 3 minutes

def generate_line_trips(line_number, direction):
    line_df = stations_df[
        stations_df["id_line"] == line_number
    ]

    line_stations = list(line_df["id_station"].values)
    if direction == "back":
        line_stations.reverse()
    line_name = translit(line_df["Line"].values[0], "ru", reversed=True)

    train_number = first_train_number
    timestamp = first_timestamp
    next_train_shift = 0

    with open(f"line{line_number}_{line_name}_{direction}.csv", "w", encoding="utf-8") as output_file:
        output_file.write("line_id,train_id,station_id,timestamp,dt\n")
        while timestamp <= last_timestamp:
            timestamp = first_timestamp + section_time * next_train_shift
            for station_id in line_stations:
                date_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S %z')
                record = f"{line_number},{line_number:02}-{train_number:04},{station_id},{timestamp},{date_time}"
                timestamp += section_time
                output_file.write(record)
                output_file.write("\n")

            train_number += 1
            next_train_shift += 1

for direction in directions:
    for line_number in line_numbers:
        generate_line_trips(line_number, direction)