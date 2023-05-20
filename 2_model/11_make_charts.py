import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

sessions_there_file_name = "sessions_extended_there.csv"
sessions_back_file_name = "sessions_extended_back.csv"
infected_trips_there_file_name = "infected_trips_there.csv"
infected_trips_back_file_name = "infected_trips_back.csv"
potentially_infected_trips_there_file_name = "potentially_infected_trips_there.csv"
potentially_infected_trips_back_file_name = "potentially_infected_trips_back.csv"

sessions_there_df = pd.read_csv(sessions_there_file_name, parse_dates=["start_dt", "end_dt"])
sessions_back_df = pd.read_csv(sessions_back_file_name, parse_dates=["start_dt", "end_dt"])

infected_trips_there_df = pd.read_csv(infected_trips_there_file_name)
infected_trips_back_df = pd.read_csv(infected_trips_back_file_name)

potentially_infected_trips_there_df = pd.read_csv(potentially_infected_trips_there_file_name)
potentially_infected_trips_back_df = pd.read_csv(potentially_infected_trips_back_file_name)

# ----------------------------
# Сделаем график количества неинфицированных и потенциально инфицированных
# пассажиров по дням

total_sessions_per_day = {}
potentially_infected_sessions_per_day = {}
non_infected_sessions_per_day = {}


first_timestamp = datetime.strptime("2020-09-01", "%Y-%m-%d")
last_timestamp = datetime.strptime("2020-09-15", "%Y-%m-%d")
one_day = timedelta(days=1)
timestamp = first_timestamp

while timestamp != last_timestamp:
    day = timestamp.strftime('%d')
    timestamp += one_day

    total_sessions_per_day[day] = 0
    potentially_infected_sessions_per_day[day] = 0
    non_infected_sessions_per_day[day] = 0


def make_total_sessions_per_day_dict(sessions_df):
    for _, trip in sessions_df.iterrows():
        day = datetime.fromtimestamp(trip["start_ts"]).strftime('%d')
        total_sessions_per_day[day] += 1


make_total_sessions_per_day_dict(sessions_there_df)
make_total_sessions_per_day_dict(sessions_back_df)


def make_potentially_infected_sessions_per_day_dict(sessions_df):
    for _, trip in sessions_df.iterrows():
        day = datetime.fromtimestamp(trip["start_ts"]).strftime('%d')
        potentially_infected_sessions_per_day[day] += 1


make_potentially_infected_sessions_per_day_dict(potentially_infected_trips_there_df)
make_potentially_infected_sessions_per_day_dict(potentially_infected_trips_back_df)

for day in potentially_infected_sessions_per_day:
    non_infected_sessions_per_day[day] = total_sessions_per_day[day] - potentially_infected_sessions_per_day[day]

labels = []
potentially_infected = []
non_infected = []

for day in total_sessions_per_day:
    labels.append(day)

for day in potentially_infected_sessions_per_day:
    potentially_infected.append(potentially_infected_sessions_per_day[day])

for day in non_infected_sessions_per_day:
    non_infected.append(non_infected_sessions_per_day[day])

fig, ax = plt.subplots()

ax.bar(labels, non_infected, label="Non-Inf.")
ax.bar(labels, potentially_infected, bottom=non_infected, label="Pot. Inf.")

ax.set_ylabel("Days")
ax.legend()

plt.savefig("potentially_infected_per_day.png")


# Сделаем распределение контактов здоровых пассажиров с заражёнными
# по часам в сутках

total_sessions_per_hour = {}
potentially_infected_sessions_per_hour = {}
non_infected_sessions_per_hour = {}

for hour in range(24):
    total_sessions_per_hour[hour] = 0
    potentially_infected_sessions_per_hour[hour] = 0
    non_infected_sessions_per_hour[hour] = 0


def make_total_sessions_per_hour_dict(sessions_df):
    for _, trip in sessions_df.iterrows():
        hour = datetime.fromtimestamp(trip["start_ts"]).strftime('%H')
        total_sessions_per_hour[int(hour)] += 1


make_total_sessions_per_hour_dict(sessions_there_df)
make_total_sessions_per_hour_dict(sessions_back_df)


def make_potentially_infected_sessions_per_hour_dict(sessions_df):
    for _, trip in sessions_df.iterrows():
        hour = datetime.fromtimestamp(trip["start_ts"]).strftime('%H')
        potentially_infected_sessions_per_hour[int(hour)] += 1


make_potentially_infected_sessions_per_hour_dict(potentially_infected_trips_there_df)
make_potentially_infected_sessions_per_hour_dict(potentially_infected_trips_back_df)

for hour in potentially_infected_sessions_per_hour:
    non_infected_sessions_per_hour[hour] = total_sessions_per_hour[hour] - potentially_infected_sessions_per_hour[hour]


labels = []
potentially_infected = []
non_infected = []

for hour in total_sessions_per_hour:
    labels.append(hour)

for hour in potentially_infected_sessions_per_hour:
    potentially_infected.append(potentially_infected_sessions_per_hour[hour])

for hour in non_infected_sessions_per_hour:
    non_infected.append(non_infected_sessions_per_hour[hour])

fig, ax = plt.subplots()

ax.bar(labels, non_infected, label="Non-Inf.")
ax.bar(labels, potentially_infected, bottom=non_infected, label="Pot. Inf.")

ax.set_ylabel("Hours")
ax.legend()

plt.savefig("potentially_infected_per_hour.png")
