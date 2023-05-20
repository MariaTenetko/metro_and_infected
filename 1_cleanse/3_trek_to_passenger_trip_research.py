import pandas as pd
import glob

infected_passengers_file_name = "../infected.xlsx"
sessions_file_names = glob.glob("../Table/hw_session*.csv")
treks_file_names = glob.glob("../Table/train_trek*.csv")
stations_file_name = "../Dict/station.json"

# Собираем данные из всех hw_session*.csv в один большой датафрейм sessions_df

sessions_df = pd.DataFrame()
for sessions_file_name in sessions_file_names:
    line_number = int(sessions_file_name[20:-4])
    line_sessions_df = pd.read_csv(sessions_file_name, parse_dates=["start_dt", "end_dt"])
    line_sessions_df["line_id"] = line_number
    sessions_df = sessions_df.append(line_sessions_df)

print(f"В датафрейме sessions_df {len(sessions_df)} записи")

# Собираем данные из всех train_trek*.csv в один большой датафрейм

treks_df = pd.DataFrame()
for treks_file_name in treks_file_names:
    line_treks_df = pd.read_csv(treks_file_name, parse_dates=["dt"])
    treks_df = treks_df.append(line_treks_df)

print(f"В датафрейме treks_df {len(treks_df)} записи")

# Достаём из датафрейма sessions_df поездки всех пассажиров, которые они сделали после своего инфицирования

infected_trips_df = pd.DataFrame()
infected_passengers_df = pd.read_excel(pd.ExcelFile(infected_passengers_file_name))
for _, passenger in infected_passengers_df.iterrows():
    passenger_infected_trips = sessions_df[
        (sessions_df["user_id"] == passenger["user_id"])
        &
        (sessions_df["start_dt"] > passenger["infected_dt"])
        ]
    infected_trips_df = infected_trips_df.append(passenger_infected_trips)

print(f"В датафрейме infected_trips_df {len(infected_trips_df)} поездок после инфицирования")

# Достаём из файла station.json информацию о преобразованиях номеров станций

stations_df = pd.read_json(stations_file_name)

# =============================================================================================================
# Гипотеза 3: мы можем однозначно связать поездку пассажира в файле hw_session* с поездом в файле train_treks*.

# Для каждой инфицированной поездки из infected_trips_df достанем из treks_df поезда,
# подходящие по признакам номера линии, номера станции, отметки времени

# 1. Достанем поезда, проходившие через станцию примерно в то время, когда заражённый начал свою поезку

def get_matching_trek(line_id, station_id, timestamp):
    # time_delta - 60 секунд, допустимая погрешность между значениями времени в hw_session и train_trek
    time_delta = 60

    matching_treks = treks_df[
        (treks_df["line_id"] == line_id)
        &
        (treks_df["station_id"] == station_id)
        &
        (abs(treks_df["timestamp"] - timestamp) <= time_delta)
        ]

    return matching_treks

no_start_and_stop_matches = 0
only_start_matches = 0
only_stop_matches = 0
both_matches = 0
exact_matches = 0

for _, trip in infected_trips_df.iterrows():
    start_station_id = trip["stst_id"]
    stop_station_id = trip["stopst_id"]
    start_timestamp = trip["start_ts"]
    stop_timestamp = trip["end_ts"]
    start_datetime = trip["start_dt"]
    stop_datetime = trip["end_dt"]
    line_id = trip["line_id"]

    # Если номера станций увеличиваются, значит, поезд идёт "туда".
    # Значит, берём номера станций без изменений, потому что это номера станций "справа" в json-e
    # и эти номера есть и в sessions_df, и в treks_df.

    # Если номера станций уменьшаются, значит, поезд идёт "обратно".
    # Значит, берём номера станций и преобразовываем их в номера станций "слева" в json-е
    # (то есть, в индексы датафрейма),
    # так как нам нужно сопоставить номера станций из одного диапазона
    # с номерами станций из другого диапазона в treks_df

    if start_station_id - stop_station_id > 0:
        start_station = stations_df[
            (stations_df["id_station"] == start_station_id)
        ]

        start_station_id = int(start_station.index.item())

    start_station_matching_treks = get_matching_trek(line_id, start_station_id, start_timestamp)
    start_train_ids = start_station_matching_treks["train_id"].tolist()

    stop_station_matching_treks = get_matching_trek(line_id, stop_station_id, stop_timestamp)
    stop_train_ids = stop_station_matching_treks["train_id"].tolist()

    if len(start_train_ids) == 0 and len(stop_train_ids) == 0:
        no_start_and_stop_matches += 1

    if len(start_train_ids) != 0 and len(stop_train_ids) == 0:
        only_start_matches += 1

    if len(start_train_ids) == 0 and len(stop_train_ids) != 0:
        only_stop_matches += 1

    if len(start_train_ids) != 0 and len(stop_train_ids) != 0:
        both_matches += 1
        if len(set(start_train_ids).intersection(stop_train_ids)) > 0:
            exact_matches += 1

print("---")
print(f"Всего поездок: {len(infected_trips_df)}")
print(f"Поездок, для которых не сопоставился поезд ни в начале, ни в конце маршрута: {no_start_and_stop_matches}")
print(f"Поездок, для которых сопоставился только поезд в начале маршрута: {only_start_matches}")
print(f"Поездок, для которых сопоставился только поезд в конце маршрута: {only_stop_matches}")
print(f"Поездок, для которых сопоставился поезд и в начале, и в конце маршрута: {both_matches},")
print(f"\tиз них номер поезда в начале маршрута совпадает с номером поезда в конце маршрута в {exact_matches} поездках")
