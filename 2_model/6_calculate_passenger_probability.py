import pandas as pd

potentially_infected_passengers_file = 'potentially_infected_passengers.txt'

sessions_there_file_name = "sessions_extended_there.csv"
sessions_back_file_name = "sessions_extended_back.csv"

potentially_infected_trips_there_file_name = "potentially_infected_trips_there.csv"
potentially_infected_trips_back_file_name = "potentially_infected_trips_back.csv"

sessions_there_df = pd.read_csv(sessions_there_file_name, parse_dates=["start_dt", "end_dt"])
sessions_back_df = pd.read_csv(sessions_back_file_name, parse_dates=["start_dt", "end_dt"])
sessions_df = sessions_there_df.append(sessions_back_df)

potentially_infected_trips_there_df = pd.read_csv(potentially_infected_trips_there_file_name)
potentially_infected_trips_back_df = pd.read_csv(potentially_infected_trips_back_file_name)
potentially_infected_trips_df = potentially_infected_trips_there_df.append(potentially_infected_trips_back_df)

with open(potentially_infected_passengers_file, 'r', encoding='utf-8') as input_file:
    potentially_infected_passengers = [row.strip() for row in input_file]

probabilities = {}

for passenger_id in potentially_infected_passengers:
    total_trips = sessions_df[
        (sessions_df["user_id"] == passenger_id)
    ].values

    total_trips_number = len(total_trips)

    potentially_infected_trips = potentially_infected_trips_df[
        (potentially_infected_trips_df["user_id"] == passenger_id)
    ].values

    potentially_infected_trips_number = len(potentially_infected_trips)

    prob = round(potentially_infected_trips_number / total_trips_number, 3)

    probabilities[passenger_id] = prob

with open("passenger_infection_probabilities.csv", "w", encoding="utf-8") as output_file:
    output_file.write("user_id,infection_probability\n")
    passenger_ids_sorted_by_probability = sorted(probabilities, key=probabilities.get)
    passenger_ids_sorted_by_probability.reverse()
    for id in passenger_ids_sorted_by_probability:
        output_file.write(f"{id},{probabilities[id]}\n")


