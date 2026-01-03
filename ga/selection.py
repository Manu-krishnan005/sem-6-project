from ga.fitness import calculate_fitness

def selection(population, user):
    population.sort(
        key=lambda x: calculate_fitness(x, user),
        reverse=True
    )
    cutoff = int(0.2 * len(population))
    return population[:cutoff]
