# Сопоставим каждой поездке из hw_session*.csv подходящий номер поезда

import pandas as pd
import glob

sessions_file_names = glob.glob("../Table/hw_session*.csv")
treks_there_file_names = glob.glob("line*_there.csv")
treks_back_file_names = glob.glob("line*_back.csv")
stations_file_name = "../Dict/station.json"


# Собираем данные из всех hw_session*.csv в один большой датафрейм sessions_df

sessions_df = pd.DataFrame()
for sessions_file_name in sessions_file_names:
    line_number = int(sessions_file_name[20:-4])
    line_sessions_df = pd.read_csv(sessions_file_name, parse_dates=["start_dt", "end_dt"])
    line_sessions_df["line_id"] = line_number
    sessions_df = sessions_df.append(line_sessions_df)

# Сконвертируем время datetime в московскую временную зону:

start_dt_utc_time = sessions_df["start_dt"].dt.tz_localize("UTC")
start_dt_moscow_time = start_dt_utc_time.dt.tz_convert("Europe/Moscow")
sessions_df["start_dt"] = start_dt_moscow_time

end_dt_utc_time = sessions_df["end_dt"].dt.tz_localize("UTC")
end_dt_moscow_time = end_dt_utc_time.dt.tz_convert("Europe/Moscow")
sessions_df["end_dt"] = end_dt_moscow_time

print(f"В датафрейме sessions_df {len(sessions_df)} записи")

# Разделяем sessions_df на два датафрейма - "туда" и "обратно":

sessions_there_df = sessions_df.loc[(sessions_df["stst_id"] - sessions_df["stopst_id"] < 0)]
sessions_back_df = sessions_df.loc[(sessions_df["stst_id"] - sessions_df["stopst_id"] > 0)]

print(f"В датафрейме sessions_there_df {len(sessions_there_df)} записи")
print(f"В датафрейме sessions_back_df {len(sessions_back_df)} записи")

# Делаем датафрейм поездов "туда"

treks_there_df = pd.DataFrame()
for treks_file_name in treks_there_file_names:
    line_treks_df = pd.read_csv(treks_file_name, parse_dates=["dt"])
    treks_there_df = treks_there_df.append(line_treks_df)

# Делаем датафрейм поездов "обратно"

treks_back_df = pd.DataFrame()
for treks_file_name in treks_back_file_names:
    line_treks_df = pd.read_csv(treks_file_name, parse_dates=["dt"])
    treks_back_df = treks_back_df.append(line_treks_df)

print(f"В датафрейме treks_there_df {len(treks_there_df)} записи")
print(f"В датафрейме treks_back_df {len(treks_back_df)} записи")


# =============================================================================================================

# Функция достаёт подходящий номер поезда по номеру линии, номеру станции,
# а также по условию, что пассажир появился на станции не раньше 2 мин. 59 секунд до отправления поезда

def get_matching_trek(treks_df, line_id, station_id, timestamp):
    # time_delta - 180 секунд, допустимая погрешность между значениями времени в hw_session и train_trek
    time_delta = 180

    matching_treks = treks_df[
        (treks_df["line_id"] == line_id)
        &
        (treks_df["station_id"] == station_id)
        &
        (treks_df["timestamp"] - timestamp > 0)
        &
        (treks_df["timestamp"] - timestamp < time_delta)
    ]

    return matching_treks

def make_extended_sessions_file(direction, sessions_df, treks_df):
    with open(f"sessions_extended_{direction}.csv", "w", encoding="utf-8") as output_file:
        output_file.write("user_id,stst_id,stopst_id,start_ts,end_ts,start_dt,end_dt,train_id\n")

        for _, session in sessions_df.iterrows():
            user_id = session["user_id"]
            start_station_id = session["stst_id"]
            stop_station_id = session["stopst_id"]
            start_timestamp = session["start_ts"]
            end_timestamp = session["end_ts"]
            start_datetime = session["start_dt"]
            end_datetime = session["end_dt"]
            line_id = session["line_id"]

            start_station_matching_treks = get_matching_trek(treks_df, line_id, start_station_id, start_timestamp)
            train_ids = start_station_matching_treks["train_id"].tolist()

            if len(train_ids) == 0:
                continue

            output_file.write(
                f"{user_id},{start_station_id},{stop_station_id},{start_timestamp},{end_timestamp},"
                f"{start_datetime},{end_datetime},{train_ids[0]}\n"
            )


make_extended_sessions_file("there", sessions_there_df, treks_there_df)
make_extended_sessions_file("back", sessions_back_df, treks_back_df)