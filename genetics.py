# Written by Gerald Walter Irsiegler

import random
import string
from numpy import random as pyr
import math

# Global Variables
size_of_first_generation = 5
max_generation_size = 10
number_of_generations = 100
chance_of_mutation_per_individual = 0.1
chance_of_crossover = 0.65
survival_probability_constant = 0.5  # don't mess with this, anything else than 0.5 crashes the program, fix soon
new_generation = []
optimum = input()


def main(opt):
    first_generation = generate_first_generation(opt)
    sort_generation_by_fitness(first_generation)
    print(first_generation)
    print(get_fitness_list(first_generation))
    set_new_generation(get_next_generation(first_generation))
    print(new_generation)
    print(get_fitness_list(new_generation))
    for x in range(0, number_of_generations):
        set_new_generation(get_next_generation(new_generation))
        print(new_generation)
        print(get_fitness_list(new_generation))


def set_new_generation(generation: list):
    global new_generation
    new_generation = generation


def generate_first_generation(opt: str):
    length = len(opt)
    firstgeneration = []
    for x in range(0, size_of_first_generation):
        tempstring = ''
        for y in range(0, length):
            tempstring += random.choice(string.ascii_letters)
        firstgeneration.append(tempstring)
    return firstgeneration


def get_fitness(individual: str):
    fitness = 0
    for x in range(0, len(individual)):
        if individual[x] == optimum[x]:
            fitness += 1
    return fitness/(len(individual))


def mutate_generation(generation: list):
    for x in range(0, len(generation)):
        randomnumber = random.randint(0, 100000)/100000
        if randomnumber <= chance_of_mutation_per_individual:
            generation[x] = mutate_single_individual(generation[x])
            print('mutation')


def get_fitness_list(generation: list):
    fitnesslist = []
    for x in range(0, len(generation)):
        fitnesslist.append(get_fitness(generation[x]))
    return fitnesslist


def get_diversity_list(generation: list):
    diversitylist = []
    for x in range(0, len(generation)):
        diversitylist.append(get_diversity(generation(x)))
    return diversitylist


def get_rating_list(generation: list):
    ratinglist = []
    for x in range(0, len(generation)):
        ratinglist.append(get_rating(generation[x]))
    return ratinglist


def get_rating(individual: str):
    inversediversity = (get_diversity(individual))**2
    inversefitness = (get_fitness(individual))**2
    rating = math.sqrt(inversediversity+inversefitness)/math.sqrt(2)
    return rating


def get_probability_list(generation: list):
    rating_list = get_rating_list(generation)
    prob_list = []
    for x in range(0, len(rating_list)):
        if x == (len(rating_list)-1):
            prob_list.append(get_probability_of_survival(x-1))
        else:
            prob_list.append(get_probability_of_survival(x))
    return prob_list


def sort_generation_by_rating(generation: list):
    return generation.sort(key=get_rating, reverse=True)


def sort_generation_by_fitness(generation: list):
    return generation.sort(key=get_fitness)


def select_surviving_individual(generation: list):
    probability_list = get_probability_list(generation)
    return pyr.choice(generation, p=probability_list)


def get_probability_of_survival(ind: int):
    return ((1-survival_probability_constant)**ind)*survival_probability_constant


def generate_children_p3(p1: string, p2: string, p3: string):
    return -1



def get_next_generation(previous_generation: list):
    set_new_generation([])
    newgeneration = []
    while len(newgeneration) < max_generation_size:
        randomnumber = random.randint(0, 100000)/100000
        if randomnumber <= chance_of_crossover:
            newindividual1, newindividual2 = crossover(previous_generation)
            newgeneration.append(newindividual1)
            newgeneration.append(newindividual2)
        else:
            newgeneration.append(select_surviving_individual(previous_generation))
        sort_generation_by_rating(newgeneration)
    mutate_generation(newgeneration)
    sort_generation_by_rating(newgeneration)
    return newgeneration


def get_diversity(individual: str):
    diversity = 0
    for newindividual in new_generation:
        diversity += different_chars(individual, newindividual)
    if len(new_generation) <= 0:
        return 0
    else:
        return (diversity/len(new_generation))/len(individual)


def different_chars(cd1: str, cd2: str):
    diffchars = 0
    for x in range(0, len(cd1)):
        if cd1[x] == cd2[x]:
            diffchars += 1
    return diffchars


def crossover(generation: list):
    x, y = '', ''
    while x == y:
        x = select_surviving_individual(generation)
        y = select_surviving_individual(generation)
    return generate_children_p2(x, y)


def mutate_single_individual(individual: str):
    newindividual = ''
    mutated_char = random.choice(range(0, len(individual)))
    for x in range(0, 1):
        for y in range(0, len(individual)):
            if y == mutated_char:
                newindividual += get_random_letter()
            else:
                newindividual += individual[y]
    return newindividual


def generate_children_p2(individual1: str, individual2: str):
    length = len(individual1)//2
    firstpartc1, secondpartc1 = individual1[:length], individual1[length:]
    firstpartc2, secondpartc2 = individual2[:length], individual2[length:]
    newindividual1 = firstpartc1 + secondpartc2
    newindividual2 = firstpartc2 + secondpartc1
    return newindividual1, newindividual2


def get_random_letter():
    return random.choice(string.ascii_letters)

main(optimum)
