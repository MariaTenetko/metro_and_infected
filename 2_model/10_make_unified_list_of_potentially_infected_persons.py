# Сделаем пересечение потенциально инфицированных пассажиров метро
# и потенциально инфицированных посетителей ТЦ и кинотеатров,
# чтобы исключить дубли


potentially_infected_passengers = []
potentially_infected_visitors = []

with open("potentially_infected_passengers.txt", "r", encoding="utf-8") as input_file:
    potentially_infected_passengers = [row.strip() for row in input_file]

with open("potentially_infected_visitors.txt", "r", encoding="utf-8") as input_file:
    potentially_infected_visitors = [row.strip() for row in input_file]

potentially_infected_passengers = set(potentially_infected_passengers)
potentially_infected_visitors = set(potentially_infected_visitors)

potentially_infected_persons_total = potentially_infected_passengers.union(potentially_infected_visitors)

with open("potentially_infected_people_total.txt", "w", encoding="utf-8") as output_file:
    for id in potentially_infected_persons_total:
        output_file.write(f"{id}\n")

print(f"Потенциально заражённых пассажиров: {len(potentially_infected_passengers)}")
print(f"Потенциально заражённых посетителей: {len(potentially_infected_visitors)}")
print(f"Всего потенциально заражённых персон: {len(potentially_infected_persons_total)}")
