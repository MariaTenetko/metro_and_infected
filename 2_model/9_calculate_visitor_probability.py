import pandas as pd

potentially_infected_visitors_file = 'potentially_infected_visitors.txt'

infected_visitors_file_name = "../infected.xlsx"
town_points_file_name = "../town_points.xlsx"
points_visits_file_name = "../Table/points.csv"

infected_visitors_df = pd.read_excel(pd.ExcelFile(infected_visitors_file_name), parse_dates=["infected_dt"])
town_points_df = pd.read_excel(pd.ExcelFile(town_points_file_name))
points_visits_df = pd.read_csv(points_visits_file_name)

print(f"В датафрейме infected_visitors_df {len(infected_visitors_df)} заражённых посетителей")
print(f"В датафрейме points_visits_df {len(points_visits_df)} посещений")

probabilities = {}

with open(potentially_infected_visitors_file, 'r', encoding='utf-8') as input_file:
    potentially_infected_visitors = [row.strip() for row in input_file]

cinema_mall_visits_df = pd.DataFrame()
for _, visit in points_visits_df.iterrows():
    visit_point_type = town_points_df[
        (town_points_df["id"] == visit["id"])
    ]["тип"].values[0]

    if visit_point_type not in ["ТЦ", "Кинотеатр"]:
        continue
    
    else:
        cinema_mall_visits_df = cinema_mall_visits_df.append(visit)

print(f"В датафрейме cinema_mall_visits_df {len(cinema_mall_visits_df)} посещений")

infected_cinema_mall_visits_df = pd.DataFrame()
for _, visitor in infected_visitors_df.iterrows():
    infection_datetime = visitor["infected_dt"].tz_localize("Europe/Moscow")
    infection_timestamp = int(infection_datetime.timestamp())

    visitor_infected_visits = points_visits_df[
        (points_visits_df["user_id"] == visitor["user_id"])
        &
        (points_visits_df["start_ts"] > infection_timestamp)
        ]
    
    visitor_cinema_mall_infected_visits = pd.DataFrame()
    for _, visit in visitor_infected_visits.iterrows():
        visit_point_type = town_points_df[
            (town_points_df["id"] == visit["id"])
        ]["тип"].values[0]

        if visit_point_type not in ["ТЦ", "Кинотеатр"]:
            continue
        else:
            visitor_cinema_mall_infected_visits = visitor_cinema_mall_infected_visits.append(visit)
    
    infected_cinema_mall_visits_df = infected_cinema_mall_visits_df.append(visitor_cinema_mall_infected_visits)

print(f"В датафрейме infected_cinema_mall_visits_df {len(infected_cinema_mall_visits_df)} посещений")

potentially_infected_cinema_mall_visits_df = pd.DataFrame()
for _, infected_visit in infected_cinema_mall_visits_df.iterrows():

    infected_visit_point_type = town_points_df[
        (town_points_df["id"] == infected_visit["id"])
    ]["тип"].values[0]

    if infected_visit_point_type not in ["ТЦ", "Кинотеатр"]:
        continue

    potentially_infected_visits = cinema_mall_visits_df[
        (cinema_mall_visits_df["id"] == infected_visit["id"])
        &
        (abs(cinema_mall_visits_df["start_ts"] - infected_visit["start_ts"]) < 180)
    ]

    for _, visit in potentially_infected_visits.iterrows():
        potentially_infected_cinema_mall_visits_df = potentially_infected_cinema_mall_visits_df.append(visit)

print(f"В датафрейме potentially_infected_cinema_mall_visits_df {len(potentially_infected_cinema_mall_visits_df)} посещений")

for visitor_id in potentially_infected_visitors:
    total_visits = cinema_mall_visits_df[
        (cinema_mall_visits_df["user_id"] == visitor_id)
    ].values

    total_visits_number = len(total_visits)
    
    potentially_infected_visits = potentially_infected_cinema_mall_visits_df[
        (potentially_infected_cinema_mall_visits_df["user_id"] == visitor_id)
    ]

    potentially_infected_visits_number = len(potentially_infected_visits)

    prob = round(potentially_infected_visits_number / total_visits_number, 3)

    probabilities[visitor_id] = prob

with open("visitor_infection_probabilities.csv", "w", encoding="utf-8") as output_file:
    output_file.write("user_id,infection_probability\n")
    visitor_ids_sorted_by_probability = sorted(probabilities, key=probabilities.get)
    visitor_ids_sorted_by_probability.reverse()
    for id in visitor_ids_sorted_by_probability:
        output_file.write(f"{id},{probabilities[id]}\n")