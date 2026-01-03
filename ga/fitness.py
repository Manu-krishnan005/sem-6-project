def calculate_fitness(chromosome, user):
    total_cal = total_protein = total_carbs = total_fats = total_cost = 0
    foods = []

    for food in chromosome:
        foods.append(food["food"])
        total_cal += food["calories"]
        total_protein += food["protein"]
        total_carbs += food["carbs"]
        total_fats += food["fats"]
        total_cost += food["cost"]

    # Macro error
    macro_error = (
        abs(user["target_calories"] - total_cal) +
        abs(user["target_protein"] - total_protein) +
        abs(user["target_carbs"] - total_carbs) +
        abs(user["target_fats"] - total_fats)
    )

    # HARD calorie penalty (IMPORTANT)
    calorie_gap = abs(user["target_calories"] - total_cal)
    calorie_penalty = calorie_gap * 3   # strong push toward 2000 kcal

    # Cost penalty
    cost_penalty = max(0, total_cost - user["budget"]) * 20

    # Diversity penalty (CRITICAL)
    repetition_penalty = (len(foods) - len(set(foods))) * 100

    fitness = 1 / (1 + macro_error + calorie_penalty + cost_penalty + repetition_penalty)
    return fitness
