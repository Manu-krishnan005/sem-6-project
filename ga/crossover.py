import random

def crossover(parent1, parent2):
    """
    Single-point crossover with duplicate removal
    """
    child = parent1[:2] + parent2[2:]

    seen = set()
    fixed_child = []

    for food in child:
        if food["food"] not in seen:
            fixed_child.append(food)
            seen.add(food["food"])

    # Fill missing slots with random non-used foods
    all_foods = parent1 + parent2
    random.shuffle(all_foods)

    for food in all_foods:
        if len(fixed_child) == 4:
            break
        if food["food"] not in seen:
            fixed_child.append(food)
            seen.add(food["food"])

    return fixed_child
