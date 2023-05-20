import pandas as pd

sessions_there_file_name = "sessions_extended_there.csv"
sessions_back_file_name = "sessions_extended_back.csv"
infected_trips_there_file_name = "infected_trips_there.csv"
infected_trips_back_file_name = "infected_trips_back.csv"
potentially_infected_trips_there_file_name = "potentially_infected_trips_there.csv"
potentially_infected_trips_back_file_name = "potentially_infected_trips_back.csv"

infected_passengers_file_name = "../infected.xlsx"

sessions_there_df = pd.read_csv(sessions_there_file_name, parse_dates=["start_dt", "end_dt"])
sessions_back_df = pd.read_csv(sessions_back_file_name, parse_dates=["start_dt", "end_dt"])

infected_trips_there_df = pd.read_csv(infected_trips_there_file_name)
infected_trips_back_df = pd.read_csv(infected_trips_back_file_name)

potentially_infected_trips_there_df = pd.read_csv(potentially_infected_trips_there_file_name)
potentially_infected_trips_back_df = pd.read_csv(potentially_infected_trips_back_file_name)

infected_passengers_df = pd.read_excel(pd.ExcelFile(infected_passengers_file_name), parse_dates=["infected_dt"])

# Общее число комбинаций "поездка + поездка":

sessions_total = len(sessions_there_df) + len(sessions_back_df)
print(f"Всего поездок: {sessions_total}")

# Число поездок инфицированных людей:

infected_trips_total =  len(infected_trips_there_df) + len(infected_trips_back_df)
print(f"Всего поездок, сделанных инфицированными пассажирами: {infected_trips_total}")

# Число поездок неинфицированных людей:
noninfected_trips_total = sessions_total - infected_trips_total
print(f"Всего поездок, сделанных неинфицированными пассажирами: {noninfected_trips_total}")

# Число поездок потенциально инфицированных людей:

potentially_infected_trips_total = len(potentially_infected_trips_there_df) + len(potentially_infected_trips_back_df)
print(f"Всего поездок неинфицированных пассажиров вместе с инфицированными пассажирами: {potentially_infected_trips_total}")

# Посчитаем возможные комбинации пассажир-1 + пассажир-2:

print("---")

session_combinations_total = sessions_total * (sessions_total - 1)
print(f"Всего возможных комбинаций поездок 'пассажир-1' + 'пассажир-2': {session_combinations_total}\n")

noninfected_noninfected_total = noninfected_trips_total * (noninfected_trips_total - 1)
print(f"Всего возможных комбинаций поездок 'неинфицированный пассажир' + 'неинфицированный пассажир': {noninfected_noninfected_total}")

infected_noninfected_total = noninfected_trips_total * infected_trips_total
print(f"Всего возможных комбинаций поездок 'инфицированный пассажир' + 'неинфицированный пассажир': {infected_noninfected_total}")
print(f"Всего возможных комбинаций поездок 'неинфицированный пассажир' + 'инфицированный пассажир': {infected_noninfected_total}")

infected_infected_total = infected_trips_total * (infected_trips_total - 1)
print(f"Всего возможных комбинаций поездок 'инфицированный пассажир' + 'инфицированный пассажир': {infected_infected_total}")

# Посчитаем вероятность поездки незаражённого пассажира с заражённым пассажиром:
prob = round((infected_noninfected_total * 2) / session_combinations_total, 3)
print(
    "Если заражение происходит после поездки незаражённого пассажира в одном поезде с заражённым пассажиром,"
    f"то вероятность такой поездки - {prob}%"
)
