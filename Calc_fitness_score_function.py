data = [
    {"id": "001", "sheduling": [0, 3, 6, 0, 3, 3, 0]},
    {"id": "002", "sheduling": [0, 0, 9, 0, 3, 3, 0]},
    {"id": "003", "sheduling": [0, 6, 3, 0, 3, 3, 0]},
    {"id": "004", "sheduling": [3, 0, 6, 3, 0, 3, 0]},
    {"id": "005", "sheduling": [3, 3, 0, 0, 3, 3, 3]},
    {"id": "006", "sheduling": [0, 3, 3, 0, 3, 3, 3]},
    {"id": "007", "sheduling": [3, 0, 6, 0, 3, 3, 0]},
    {"id": "008", "sheduling": [3, 9, 3, 0, 0, 0, 0]},
    
]


data_1 = [
    {"id": "001", "sheduling": [0, 3, 6, 0, 3, 3, 0]},
    {"id": "002", "sheduling": [0, 0, 9, 0, 3, 3, 0]},
    {"id": "003", "sheduling": [0, 6, 3, 0, 3, 3, 0]},
    {"id": "004", "sheduling": [3, 0, 6, 3, 0, 3, 0]},
    {"id": "005", "sheduling": [3, 3, 0, 0, 3, 3, 3]},
    {"id": "006", "sheduling": [0, 3, 3, 0, 3, 3, 3]},
    {"id": "007", "sheduling": [3, 0, 6, 0, 3, 3, 0]},
    {"id": "008", "sheduling": [3, 9, 3, 0, 0, 0, 0]},
    
]
import random

# Generate a valid scheduling array where each day's teaching hours sum to 15
def generate_valid_sheduling():
    while True:
        sheduling = [0] * 7
        remaining_hours = 15
        
        # Randomly allocate hours to 7 days
        for i in range(7):
            if remaining_hours > 0:
                hours = random.choice([0, 3, 6, 9, 12, 15])
                if hours <= remaining_hours:
                    sheduling[i] = hours
                    remaining_hours -= hours
        
        if remaining_hours == 0:  # Ensure the sum is exactly 15
            return sheduling

# Initialize a population with valid scheduling
def initialize_population(pop_size):
    population = []
    for i in range(pop_size):
        population.append({
            "id": f"{i+1:03}",
            "sheduling": generate_valid_sheduling(),
            "multip": 1,  # Initialize multip and percent for each individual
            "percent": 0
        })
    return population

# Calculate multiplication-based fitness function
def calc_multip_fitness_function(data):
    for entry in data:
        multip = 1
        for value in entry["sheduling"]:
            if value == 0:
                value = 1  # Treat 0 as 1 for fitness calculation
            multip *= value
        entry["multip"] = multip  # Store the multiplication result
    return data

# Calculate the total multip for the population
def calc_total_multip(data):
    total_multip = sum(entry["multip"] for entry in data)
    return total_multip

# Calculate the percentage fitness for each individual in the population
def calc_percent_fitness(data):
    total = calc_total_multip(data)
    for entry in data:
        entry['percent'] = entry["multip"] / total if total > 0 else 0
    return data

# Selection based on fitness (probabilistic based on percentage)
def select_parents(population):
    total_fitness = sum(entry['multip'] for entry in population)
    selection_probs = [entry['multip'] / total_fitness for entry in population]
    return random.choices(population, weights=selection_probs, k=2)

# Crossover operation ensuring the total hours remains 15
def crossover(parent1, parent2):
    crossover_point = random.randint(1, 6)  # Random crossover point (1 to 6)
    child1 = parent1["sheduling"][:crossover_point] + parent2["sheduling"][crossover_point:]
    child2 = parent2["sheduling"][:crossover_point] + parent1["sheduling"][crossover_point:]
    
    # Correct the total to ensure it sums to 15
    def correct_schedule(schedule):
        if sum(schedule) > 15:
            for i in range(7):
                while sum(schedule) > 15 and schedule[i] > 0:
                    schedule[i] -= 3  # Decrease hours
        elif sum(schedule) < 15:
            for i in range(7):
                while sum(schedule) < 15:
                    if schedule[i] < 15:
                        schedule[i] += 3  # Increase hours
        return schedule

    return {"sheduling": correct_schedule(child1)}, {"sheduling": correct_schedule(child2)}

# Mutation operation ensuring the total hours remains 15
def mutate(individual):
    idx = random.randint(0, 6)  # Choose a random day
    current_value = individual["sheduling"][idx]
    
    # Randomly choose a new value from allowed hours
    possible_values = [0, 3, 6, 9, 12, 15]
    new_value = random.choice(possible_values)

    # Calculate the change in hours
    delta = new_value - current_value
    
    # Update the schedule and ensure the sum remains 15
    if sum(individual["sheduling"]) + delta == 15:
        individual["sheduling"][idx] = new_value  # Accept mutation

# Main genetic algorithm loop
def genetic_algorithm(data, generations):
    # Step 1: Use the provided data as the initial population
    population = data
    
    for generation in range(generations):
        # Step 2: Calculate fitness for each individual
        calc_multip_fitness_function(population)
        calc_percent_fitness(population)

        # Step 3: Create a new population
        new_population = []
        
        while len(new_population) < len(population):
            # Step 4: Select parents based on fitness
            parent1, parent2 = select_parents(population)
            
            # Step 5: Perform crossover to produce children
            child1, child2 = crossover(parent1, parent2)
            
            # Step 6: Mutate children while maintaining the sum constraint
            mutate(child1)
            mutate(child2)
            
            # Step 7: Add children to the new population
            new_population.append({
                "id": f"{len(new_population) + 1:03}",
                "sheduling": child1["sheduling"],
                "multip": 1,
                "percent": 0
            })
            if len(new_population) < len(population):
                new_population.append({
                    "id": f"{len(new_population) + 1:03}",
                    "sheduling": child2["sheduling"],
                    "multip": 1,
                    "percent": 0
                })
        
        # Step 8: Replace old population with new one
        population = new_population[:len(population)]
    
    # Final fitness calculation for the resulting population
    calc_multip_fitness_function(population)
    calc_percent_fitness(population)
    
    return population

final_population = genetic_algorithm(data, generations=100)
calc_multip_fitness_function(data_1)
calc_percent_fitness(data_1)


# Print results
# Compare the original data and after using the genetic algorithm
for individual in data_1:
    print(f"ID: {individual['id']}, Sheduling: {individual['sheduling']}, Multip: {individual['multip']}, Percent: {individual['percent']:.2%}")

print("\n")

for individual in final_population:
    print(f"ID: {individual['id']}, Sheduling: {individual['sheduling']}, Multip: {individual['multip']}, Percent: {individual['percent']:.2%}")

calc_multip_fitness_function(data_1)
calc_percent_fitness(data_1)

print("\n")