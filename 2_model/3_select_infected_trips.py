import pandas as pd

sessions_there_file_name = "sessions_extended_there.csv"
sessions_back_file_name = "sessions_extended_back.csv"
infected_passengers_file_name = "../infected.xlsx"

sessions_there_df = pd.read_csv(sessions_there_file_name, parse_dates=["start_dt", "end_dt"])
sessions_back_df = pd.read_csv(sessions_back_file_name, parse_dates=["start_dt", "end_dt"])
infected_passengers_df = pd.read_excel(pd.ExcelFile(infected_passengers_file_name), parse_dates=["infected_dt"])

# Достаём из датафрейма sessions_df поездки инфицированных пассажиров,
# которые они сделали после своего инфицирования

def make_trips_after_infection_dataframe(infected_passengers_df, sessions_df):
    infected_trips_df = pd.DataFrame()
    for _, passenger in infected_passengers_df.iterrows():
        infection_datetime = passenger["infected_dt"].tz_localize("Europe/Moscow")
        infection_timestamp = int(infection_datetime.timestamp())

        passenger_infected_trips = sessions_df[
            (sessions_df["user_id"] == passenger["user_id"])
            &
            (sessions_df["start_ts"] > infection_timestamp)
            ]
        infected_trips_df = infected_trips_df.append(passenger_infected_trips)

    return infected_trips_df

infected_trips_there_df = make_trips_after_infection_dataframe(infected_passengers_df, sessions_there_df)
infected_trips_back_df = make_trips_after_infection_dataframe(infected_passengers_df, sessions_back_df)

print(f"В датафрейме infected_trips_there_df {len(infected_trips_there_df)} поездок после инфицирования")
print(f"В датафрейме infected_trips_back_df {len(infected_trips_back_df)} поездок после инфицирования")

# Сохраняем поездки инфицированных пассажиров,
# которые они сделали после своего инфицирования,
# в отдельные файлы

def make_infected_trips_df_file(direction, infected_trips_df):
    with open(f"infected_trips_{direction}.csv", "w", encoding="utf-8") as output_file:
        output_file.write("user_id,stst_id,stopst_id,start_ts,end_ts,start_dt,end_dt,train_id\n")
        for _, trip in infected_trips_df.iterrows():
            user_id = trip["user_id"]
            start_station_id = trip["stst_id"]
            stop_station_id = trip["stopst_id"]
            start_timestamp = trip["start_ts"]
            end_timestamp = trip["end_ts"]
            start_datetime = trip["start_dt"]
            end_datetime = trip["end_dt"]
            train_id = trip["train_id"]

            output_file.write(
                f"{user_id},{start_station_id},{stop_station_id},{start_timestamp},{end_timestamp},"
                f"{start_datetime},{end_datetime},{train_id}\n"
            )

make_infected_trips_df_file("there", infected_trips_there_df)
make_infected_trips_df_file("back", infected_trips_back_df)

