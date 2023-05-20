import pandas as pd

infected_visitors_file_name = "../infected.xlsx"
town_points_file_name = "../town_points.xlsx"
points_visits_file_name = "../Table/points.csv"

infected_visitors_df = pd.read_excel(pd.ExcelFile(infected_visitors_file_name), parse_dates=["infected_dt"])
town_points_df = pd.read_excel(pd.ExcelFile(town_points_file_name))
points_visits_df = pd.read_csv(points_visits_file_name)

print(f"В датафрейме infected_visitors_df {len(infected_visitors_df)} заражённых посетителей")
print(f"В датафрейме points_visits_df {len(points_visits_df)} посещений")

# Посчитаем общее количество посещений кинозалов и торговых центров

total_mall_and_cinema_visits = 0
for _, visit in points_visits_df.iterrows():

    visit_point_type = town_points_df[
        (town_points_df["id"] == visit["id"])
    ]["тип"].values[0]

    if visit_point_type not in ["ТЦ", "Кинотеатр"]:
        continue
    
    else:
        total_mall_and_cinema_visits += 1


# Посчитаем количество посещений кинозалов и торговых центров заражёнными людьми

infected_mall_and_cinema_visits = 0
infected_visits_df = pd.DataFrame()

for _, visitor in infected_visitors_df.iterrows():
    infection_datetime = visitor["infected_dt"].tz_localize("Europe/Moscow")
    infection_timestamp = int(infection_datetime.timestamp())

    visitor_infected_visits = points_visits_df[
        (points_visits_df["user_id"] == visitor["user_id"])
        &
        (points_visits_df["start_ts"] > infection_timestamp)
        ]
    infected_visits_df = infected_visits_df.append(visitor_infected_visits)

for _, infected_visit in infected_visits_df.iterrows():
    infected_visit_point_type = town_points_df[
        (town_points_df["id"] == infected_visit["id"])
    ]["тип"].values[0]

    if infected_visit_point_type not in ["ТЦ", "Кинотеатр"]:
        continue
    else:
        infected_mall_and_cinema_visits += 1

print("---")

# Общее число комбинаций "посещение + посещение":

visits_combinations_total = total_mall_and_cinema_visits * (total_mall_and_cinema_visits - 1)
print(f"Всего {total_mall_and_cinema_visits} посещений")
print(f"Всего возможных комбинаций встреч 'посетитель-1' + 'посетитель-2': {visits_combinations_total}\n")

# Число комбинаций
infected_combinations_total = infected_mall_and_cinema_visits * (infected_mall_and_cinema_visits - 1)
print(f"Всего {infected_mall_and_cinema_visits} посещений инфицированными посетителями")
print(f"Всего возможных комбинаций встреч 'инфицированный посетитель' + 'инфицированный посетитель': {infected_combinations_total}\n")

noninfected_mall_and_cinema_visits = total_mall_and_cinema_visits - infected_mall_and_cinema_visits
noninfected_combinations_total = noninfected_mall_and_cinema_visits * (noninfected_mall_and_cinema_visits - 1)
print(f"Всего {noninfected_mall_and_cinema_visits} посещений неинфицированными посетителями")
print(f"Всего возможных комбинаций встреч 'неинфицированный посетитель' + 'неинфицированный посетитель': {noninfected_combinations_total}\n")

infected_noninfected_combinations_total = infected_mall_and_cinema_visits * noninfected_mall_and_cinema_visits * 2
print("Всего возможных комбинаций встреч 'неинфицированный посетитель' + 'неинфицированный посетитель,'")
print(f"а также возможных комбинаций встреч 'инфицированный пользователь + неинфицированный пользователь: {infected_noninfected_combinations_total}\n")

# Посчитаем вероятность встречи незаражённого посетителя с заражённым посетителем:
prob = round(infected_noninfected_combinations_total / visits_combinations_total, 3)
print(
    "Если заражение происходит после встречи незаражённого посетителя в одном ТЦ или кинотеатре с заражённым посетителем,"
    f"то вероятность такой встречи - {prob}%"
)

