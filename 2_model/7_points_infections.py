import pandas as pd

infected_visitors_file_name = "../infected.xlsx"
town_points_file_name = "../town_points.xlsx"
points_visits_file_name = "../Table/points.csv"

infected_visitors_df = pd.read_excel(pd.ExcelFile(infected_visitors_file_name), parse_dates=["infected_dt"])
town_points_df = pd.read_excel(pd.ExcelFile(town_points_file_name))
points_visits_df = pd.read_csv(points_visits_file_name)

print(f"В датафрейме infected_visitors_df {len(infected_visitors_df)} заражённых посетителей")
print(f"В датафрейме points_visits_df {len(points_visits_df)} посещений")


# Достаём из датафрейма points_visits_df посещения инфицированных посетителей,
# которые они сделали после своего инфицирования

def make_visits_after_infection_dataframe(infected_visitors_df, points_visits_df):
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

    return infected_visits_df

infected_visits_df = make_visits_after_infection_dataframe(infected_visitors_df, points_visits_df)

print(f"В датафрейме infected_visits_df {len(infected_visits_df)} поездок после инфицирования")

# Посмотрим, в каких типах локаций были заражённые посетители:

point_types = {}
for _, row in infected_visits_df.iterrows():
    point_type = town_points_df[
        (town_points_df["id"] == row["id"])
    ]["тип"].values[0]

    if point_type in point_types:
        point_types[point_type] += 1
    else:
        point_types[point_type] = 1

for point_type in point_types:
    print(f"{point_type}: {point_types[point_type]} посещений")

# Видим 4 типа локаций:
# {'парки': 82147, 'ТЦ': 6723, 'улицы': 9625, 'Кинотеатр': 1628}
# Дальше смотрим только локации с замкнутым пространством: ТЦ и Кинотеатр

# Создаём множество с ID инфицированных посетителей (значения в нём будут уникальными):

infected_visitors = set(infected_visitors_df["user_id"])
print(f"В множестве infected_visitors {len(infected_visitors)} посетителей")


# Создаём множество, в которое будем складывать найденные ID посетителей, контактировавших с заражённым посетителем
# (значения в нём будут уникальными):

potentially_infected_visitors = set()

# Для каждой инфицированного посещения достаём все посещения, которые соответствуют трём условиям:
# - такой же id локации, как в инфицированном посещении;
# - разница во времени составляет не больше 3 часов;
# - тип локации - ТЦ или Кинотеатр;
#
# Сохраняем в множество potentially_infected_visitors ID посетителей из этих визитов,
# затем убираем из множества user_ids тех, кто уже инфицирован


def find_potentially_infected_visits(infected_visits_df, points_visits_df):
    for _, infected_visit in infected_visits_df.iterrows():

        infected_visit_point_type = town_points_df[
            (town_points_df["id"] == infected_visit["id"])
        ]["тип"].values[0]

        if infected_visit_point_type not in ["ТЦ", "Кинотеатр"]:
            continue

        potentially_infected_visits = points_visits_df[
            (points_visits_df["id"] == infected_visit["id"])
            &
            (abs(points_visits_df["start_ts"] - infected_visit["start_ts"]) < 180)
        ]

        for _, visit in potentially_infected_visits.iterrows():
            potentially_infected_visitors.add(visit["user_id"])


        # for _, visit in potentially_infected_visits.iterrows():
        #     print(visit)
        #     print("-----")
        # print("=================")


find_potentially_infected_visits(infected_visits_df, points_visits_df)
potentially_infected_visitors = potentially_infected_visitors.difference(infected_visitors)

print("\n---")
print(f"Выявили {len(potentially_infected_visitors)} потенциально заражённых посетителей")

with open("potentially_infected_visitors.txt", "w", encoding="utf-8") as output_file:
    for user_id in potentially_infected_visitors:
        output_file.write(user_id)
        output_file.write("\n")
