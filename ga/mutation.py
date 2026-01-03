import random

def mutate(chromosome, food_list, mutation_rate=0.1):
    """
    Mutate chromosome safely for dynamic length
    """
    if random.random() < mutation_rate:
        index = random.randrange(len(chromosome))
        chromosome[index] = random.choice(food_list)
