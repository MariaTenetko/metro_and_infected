import pandas as pd

sessions_there_file_name = "sessions_extended_there.csv"
sessions_back_file_name = "sessions_extended_back.csv"
infected_trips_there_file_name = "infected_trips_there.csv"
infected_trips_back_file_name = "infected_trips_back.csv"
infected_passengers_file_name = "../infected.xlsx"

sessions_there_df = pd.read_csv(sessions_there_file_name, parse_dates=["start_dt", "end_dt"])
sessions_back_df = pd.read_csv(sessions_back_file_name, parse_dates=["start_dt", "end_dt"])
infected_trips_there_df = pd.read_csv(infected_trips_there_file_name)
infected_trips_back_df = pd.read_csv(infected_trips_back_file_name)

infected_passengers_df = pd.read_excel(pd.ExcelFile(infected_passengers_file_name), parse_dates=["infected_dt"])


# Создаём множество с ID инфицированных пассажиров (значения в нём будут уникальными):

infected_passengers = set(infected_passengers_df["user_id"])
print(f"В множестве infected_passengers {len(infected_passengers)} пассажиров")


# Создаём множество, в которое будем складывать найденные ID пассажиров, контактировавших с заражённым пассажиром
# (значения в нём будут уникальными):

potentially_infected_passengers = set()

# Для каждой инфицированной поездки достаём все поездки, которые соответствуют трём условиям:
# - такой же номер поезда, как в инфицированной поездке;
# - а также:
#    - или пассажир сел в поезд до того, как вышел инфицированный;
#    - или пассажир вышел из поезда после того, как сел инфицированный;
#
# Сохраняем в множество potentially_infected_passengers ID пассажиров из этих поездок,
# затем убираем из множества user_ids тех, кто уже инфицирован

def find_potentially_infected_trips(infected_trips_df, sessions_df):
    potentially_infected_trips_df = pd.DataFrame()

    for _, infected_trip in infected_trips_df.iterrows():
        potentially_infected_trips = sessions_df[
            (sessions_df["train_id"] == infected_trip["train_id"])
            &
            (
                    (sessions_df["stst_id"] < infected_trip["stopst_id"])
                    |
                    (sessions_df["stopst_id"] > infected_trip["stst_id"])
            )
            ]

        for _, trip in potentially_infected_trips.iterrows():
            potentially_infected_passengers.add(trip["user_id"])
            potentially_infected_trips_df = potentially_infected_trips_df.append(trip)

    return(potentially_infected_trips_df)

potentially_infected_trips_there_df = find_potentially_infected_trips(infected_trips_there_df, sessions_there_df)
potentially_infected_trips_back_df = find_potentially_infected_trips(infected_trips_back_df, sessions_back_df)

print(f"\nОбнаружили {len(potentially_infected_trips_there_df)} потенциально заражённых поездок 'туда'")
print(f"\nОбнаружили {len(potentially_infected_trips_back_df)} потенциально заражённых поездок 'обратно'")

def make_potentially_infected_trips_df_file(direction, potentially_infected_trips_df):
    with open(f"potentially_infected_trips_{direction}.csv", "w", encoding="utf-8") as output_file:
        output_file.write("user_id,stst_id,stopst_id,start_ts,end_ts,start_dt,end_dt,train_id\n")
        for _, trip in potentially_infected_trips_df.iterrows():
            user_id = trip["user_id"]
            start_station_id = int(trip["stst_id"])
            stop_station_id = int(trip["stopst_id"])
            start_timestamp = int(trip["start_ts"])
            end_timestamp = int(trip["end_ts"])
            start_datetime = trip["start_dt"]
            end_datetime = trip["end_dt"]
            train_id = trip["train_id"]

            output_file.write(
                f"{user_id},{start_station_id},{stop_station_id},{start_timestamp},{end_timestamp},"
                f"{start_datetime},{end_datetime},{train_id}\n"
            )

make_potentially_infected_trips_df_file("there", potentially_infected_trips_there_df)
make_potentially_infected_trips_df_file("back", potentially_infected_trips_back_df)

potentially_infected_passengers = potentially_infected_passengers.difference(infected_passengers)

print("\n---")
print(f"Выявили {len(potentially_infected_passengers)} потенциально заражённых пассажиров")

with open("potentially_infected_passengers.txt", "w", encoding="utf-8") as output_file:
    for user_id in potentially_infected_passengers:
        output_file.write(user_id)
        output_file.write("\n")

