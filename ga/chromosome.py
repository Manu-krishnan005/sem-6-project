import random

MEAL_ORDER = ["breakfast", "lunch", "snack", "dinner", "late_snack"]

def generate_chromosome(food_list, meals):
    """
    Generate a chromosome with N meals
    """
    meals = int(meals)

    if len(food_list) < meals:
        return random.sample(food_list * meals, meals)

    selected = random.sample(food_list, meals)

    chromosome = []
    for i in range(meals):
        chromosome.append({
            "meal": MEAL_ORDER[i],
            "food": selected[i]["food"],
            "calories": selected[i]["calories"],
            "protein": selected[i]["protein"],
            "carbs": selected[i]["carbs"],
            "fats": selected[i]["fats"],
            "cost": selected[i]["cost"]
        })

    return chromosome
