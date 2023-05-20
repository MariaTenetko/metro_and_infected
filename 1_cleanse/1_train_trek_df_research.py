import pandas as pd

intervals_between_stations = []
start_time = 0

fil_trek_df = pd.read_csv("../Table/train_trek17.csv")
for _, row in fil_trek_df.iterrows():
    if row["station_id"] in [72, 304]:
        start_time = row["timestamp"]

    if row["station_id"] in [73, 303]:
        interval = row["timestamp"] - start_time
        intervals_between_stations.append(interval)

print(
    "Среднее значение интервала между Выставочной и Международной: "
    f"{sum(intervals_between_stations) / len(intervals_between_stations)}"
)

intervals_between_stations = []
start_time = 0

fil_trek_df = pd.read_csv("../Table/train_trek1.csv")
for _, row in fil_trek_df.iterrows():
    if row["station_id"] in [17, 56]:
        start_time = row["timestamp"]

    if row["station_id"] in [16, 57]:
        interval = row["timestamp"] - start_time
        intervals_between_stations.append(interval)

print(
    "Среднее значение интервала между Крылатским и Строгино: "
    f"{sum(intervals_between_stations) / len(intervals_between_stations)}"
)

