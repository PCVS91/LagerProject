
# In[1]:


import random as rd
import numpy as np
import copy
from Classes import *
from typing import List, Tuple


# In[2]:


def pick(corr: Corr, platz: int, choice: int) -> float:
    # Redefine regal1 and regal2 based on choice
    regal1, regal2 = (corr.regal1, corr.regal2) if choice == 0 else (corr.regal2, corr.regal1)
    
    # Extract reference distance and code from the chosen regal
    ref_d = regal1.tuples[platz][0]
    ref_code = regal1.tuples[platz][1]
    
    # Calculate error based on both regals within the corridor
    total_error = 0.0
    for regal in [regal1, regal2]:
        for shelf in regal.tuples:
            if regal.tuples[shelf][1] == ref_code:
                error_distance = abs(regal.tuples[shelf][0] - ref_d)
                if error_distance == 0 and regal is regal1:
                    continue  # Skip adding error if distance is 0 and in the correct regal
                if error_distance == 0:
                    total_error += 5
                elif error_distance == 1:
                    total_error += 3 if regal is regal2 else 5
                elif error_distance == 2:
                    total_error += 1 if regal is regal2 else 2
                elif error_distance == 3:
                    total_error += 0.5 if regal is regal2 else 1
                elif error_distance == 4 and regal is regal1:
                    total_error += 0.5

    return total_error


# In[3]:


def calculate_fitness(corr: Corr) -> float:
    total_error = 0.0
    for _ in range(1000):  # Sampling 1000 picks for fitness evaluation
        choice = rd.randint(0, 1)
        platz = rd.randint(1, len(corr.regal1.tuples) if choice == 0 else len(corr.regal2.tuples))
        error = pick(corr, platz, choice)
        total_error += error
    return total_error / 1000

# Initialize population with different numbers of sections for regal1 and regal2
def initialize_population(pop_size: int, num_sections_regal1: int, num_sections_regal2: int) -> List[Tuple[Regal, Regal]]:
    population = []
    for _ in range(pop_size):
        sections1 = [Section(racks=[rd.randint(1, 3) for _ in range(3)], distance=i) for i in range(num_sections_regal1)]
        sections2 = [Section(racks=[rd.randint(1, 3) for _ in range(3)], distance=i) for i in range(num_sections_regal2)]
        regal1 = Regal(sections1)
        regal2 = Regal(sections2)
        population.append(Corr(regal1, regal2))
    return population

def select_parents(population: List[Corr], fitnesses: List[float], num_parents: int) -> List[Corr]:
    selected = np.random.choice(population, size=num_parents, p=fitnesses / np.sum(fitnesses))
    return selected.tolist()

def crossover(parent1: Corr, parent2: Corr) -> Tuple[Corr, Corr]:
    crossover_point = rd.randint(1, len(parent1.regal1.sections) - 1)
    child1_regal1_sections = parent1.regal1.sections[:crossover_point] + parent2.regal1.sections[crossover_point:]
    child1_regal2_sections = parent1.regal2.sections[:crossover_point] + parent2.regal2.sections[crossover_point:]
    child2_regal1_sections = parent2.regal1.sections[:crossover_point] + parent1.regal1.sections[crossover_point:]
    child2_regal2_sections = parent2.regal2.sections[:crossover_point] + parent1.regal2.sections[crossover_point:]
    return Corr(Regal(child1_regal1_sections), Regal(child1_regal2_sections)), Corr(Regal(child2_regal1_sections), Regal(child2_regal2_sections))

def mutate(corr: Corr, mutation_rate: float):
    for regal in [corr.regal1, corr.regal2]:
        for section in regal.sections:
            if rd.random() < mutation_rate:
                section.fix()

def genetic_algorithm(pop_size: int, num_generations: int, num_sections: List[int], mutation_rate: float) -> Corr:
    population = initialize_population(pop_size, num_sections[0],num_sections[1])
    best_solution = None
    best_fitness = float('inf')

    for generation in range(num_generations):
        fitnesses = [calculate_fitness(corr) for corr in population]
        min_fitness_idx = fitnesses.index(min(fitnesses))
        if fitnesses[min_fitness_idx] < best_fitness:
            best_fitness = fitnesses[min_fitness_idx]
            best_solution = population[min_fitness_idx]
        parents = select_parents(population, fitnesses, pop_size // 2)
        offspring = []
        for i in range(0, len(parents), 2):
            if i + 1 < len(parents):
                child1, child2 = crossover(parents[i], parents[i + 1])
                mutate(child1, mutation_rate)
                mutate(child2, mutation_rate)
                offspring.append(child1)
                offspring.append(child2)
        population = parents + offspring

    return best_solution


