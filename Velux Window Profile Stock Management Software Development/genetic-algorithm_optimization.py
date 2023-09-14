import random

# Given data
L = 5  # meters
C = 50  # € per meter
A = 0.60  # meters
B = 2.80  # meters
E = 10  # bars started
N = 100  # windows per week

# Genetic Algorithm Parameters
population_size = 100
generations = 100
mutation_rate = 0.1

# Function to calculate potential cost savings
def calculate_potential_cost_savings(price):
    current_cost_per_window = (2 * (B - A) + A) * C
    potential_cost_savings_per_window = (2 * (B - A) + A) * (C - price)
    total_potential_cost_savings_per_week = N * potential_cost_savings_per_window
    annual_potential_cost_savings = total_potential_cost_savings_per_week * 52
    return annual_potential_cost_savings

# Create an initial population with random prices
population = [random.uniform(0, C) for _ in range(population_size)]

# Genetic Algorithm
for generation in range(generations):
    # Evaluate fitness of each individual in the population
    fitness = [calculate_potential_cost_savings(price) for price in population]

    # Select the top 50% based on fitness
    num_parents = population_size // 2
    parents = [population[i] for i in sorted(range(population_size), key=lambda x: fitness[x], reverse=True)[:num_parents]]

    # Create the next generation through crossover and mutation
    children = []
    while len(children) < num_parents:
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        crossover_point = random.randint(0, population_size - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        if random.random() < mutation_rate:
            mutation = random.uniform(-0.1 * C, 0.1 * C)
            child = min(max(child + mutation, 0), C)  # Ensure the price is within bounds
        children.append(child)

    # Replace the old population with the new generation
    population = parents + children

# Find the best price in the final population
best_price = max(population, key=lambda x: calculate_potential_cost_savings(x))

# Calculate the corresponding annual potential cost savings
best_savings = calculate_potential_cost_savings(best_price)

print(f"Best price for the software: €{best_price:.2f}")
print(f"Corresponding annual potential cost savings: €{best_savings:.2f}")
