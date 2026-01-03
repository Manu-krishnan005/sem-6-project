import csv, os, random
from ga.chromosome import generate_chromosome
from ga.mutation import mutate
from ga.crossover import crossover
from ga.fitness import calculate_fitness

MEAL_ORDER = ["breakfast", "lunch", "snack", "dinner", "late_snack"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "food_data.csv")

def load_food_data():
    food_list = []
    with open(DATA_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            food_list.append({
                "food": row["food"],
                "calories": float(row["calories"]),
                "protein": float(row["protein"]),
                "carbs": float(row["carbs"]),
                "fats": float(row["fats"]),
                "cost": float(row["cost"]),
                "tags": row["tags"].lower()
            })
    return food_list

def normalize_day(day):
    normalized = []
    for i, food in enumerate(day):
        normalized.append({
            **food,
            "meal": MEAL_ORDER[i]
        })
    return normalized

def run_ga(user):
    food_list = load_food_data()

    if user["diet_type"] == "veg":
        food_list = [f for f in food_list if f["tags"] == "veg"]

    if user.get("allergies"):
        food_list = [
            f for f in food_list
            if not any(a in f["food"].lower() for a in user["allergies"])
        ]

    population = [
        generate_chromosome(food_list, user["meals"])
        for _ in range(100)
    ]

    for _ in range(50):
        population = sorted(
            population,
            key=lambda x: calculate_fitness(x, user),
            reverse=True
        )

        selected = population[:20]
        children = []

        while len(children) < 80:
            p1, p2 = random.sample(selected, 2)
            child = crossover(p1, p2)
            mutate(child, food_list)
            children.append(normalize_day(child))

        population = selected + children

    best = max(population, key=lambda x: calculate_fitness(x, user))
    return normalize_day(best)

def run_weekly_ga(user):
    return [run_ga(user) for _ in range(7)]

def calculate_day_totals(day):
    totals = {"calories": 0, "protein": 0, "carbs": 0, "fats": 0}

    portion_map = {2:1.5, 3:1.3, 4:1.0, 5:0.9}
    factor = portion_map[len(day)]

    for meal in day:
        totals["calories"] += meal["calories"] * factor
        totals["protein"] += meal["protein"] * factor
        totals["carbs"] += meal["carbs"] * factor
        totals["fats"] += meal["fats"] * factor

    return totals

def validate_calories(total, target, tol=0.05):
    return target*(1-tol) <= total <= target*(1+tol)
