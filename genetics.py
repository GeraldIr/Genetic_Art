# Written by Gerald Walter Irsiegler

import random
import string
from numpy import random as pyr
import math
import generation
import values
from PIL import Image as pim
from PIL import ImageTk as pik
from tkinter import *
from tkinter import simpledialog, filedialog
import matplotlib.pyplot as plt


# Canvas stuff
master = Tk()
canvas = Canvas(master, width=800, height=800)
canvas.pack()


# Global Variables
size_of_first_generation = 10
max_generation_size = 20
number_of_generations = simpledialog.askinteger("# of Generations", "How many generations should be simulated?")
chance_of_mutation_per_individual = 0.35
chance_of_crossover = 0.7
survival_probability_constant = 0.5  # don't mess with this, anything else than 0.5 crashes the program, fix soon

# gene mutation
gene_mutation_chance = 0.1
gene_mutation_size = 10 # inverse, the bigger the smaller
max_gene_mutation_size = 3

# Hopefully soon to be non global values
first_generation = []
new_generation = []



# Control Variables
avg_fit = []

# Mode
mode = ""
optimum_picture = pim.new("RGB", values.picture_size, color=0)


def main_string(opt):
    init(opt)
    sort_generation_by_fitness(first_generation)
    print(first_generation)
    print(get_fitness_list(first_generation))
    set_new_generation(get_next_generation(first_generation))
    print(new_generation)
    print(get_fitness_list(new_generation))
    for x in range(0, number_of_generations):
        set_new_generation(get_next_generation(new_generation))
        save_generation(x)
        print(new_generation)
        print(get_fitness_list(new_generation))


def main():
    mode_choice()
    init()
    sort_generation_by_fitness(first_generation)
    print(get_rating_list(first_generation))
    save_generation(0)
    set_new_generation(get_next_generation(first_generation))
    for x in range(1, number_of_generations):
        set_new_generation(get_next_generation(new_generation))
        print(get_fitness_list(new_generation))
        save_new_generation(x)
        if mode != "m":
            draw_new_generation()
        avg = get_average_fitness()
        avg_fit.append(avg)
        # adjust_mutation_parameters()
    analysis()


def init():
    global first_generation
    first_generation = generate_first_generation()


def get_average_improvement_last_ten():
    avg_list = get_improvement_list()
    avg = 0
    if len(avg_list) < 10:
        return get_average_improvement()
    for x in range(0, 9):
        avg += avg_list[len(avg_list)-(x+1)]
    return avg/10


def adjust_mutation_parameters():
    global chance_of_mutation_per_individual
    global gene_mutation_chance
    global gene_mutation_size

    ten_avg = get_average_improvement_last_ten()

    if ten_avg < get_average_improvement():
        gene_mutation_chance += 0.001
    else:
        gene_mutation_chance -= 0.001

    chance_of_mutation_per_individual = 1 - get_average_fitness()
    gene_mutation_size = (1 - get_average_fitness()) * 20



def analysis():
    print("--------------------------------")
    print("------------ANALYSIS------------")
    print(get_average_improvement())

    plt.plot(avg_fit)
    plt.ylabel("Fitness")
    plt.xlabel("Generation")
    plt.show()

    plt.plot(get_improvement_list())
    plt.ylabel("Improvement")
    plt.xlabel("Generation")
    plt.show()


def mode_choice():
    global mode
    global optimum_picture
    mode = simpledialog.askstring("Mode Choice", "Test (t), Manual (m), Red (r), Picture (p) or Silhouettet (s): ")
    if mode == "p" or mode == "s":
        path = filedialog.askopenfilename(initialdir = "C:\home\project\Genetic_Art\Pictures",title = "Select optimal picture",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        optimum_picture = pim.open(path)
        optimum_picture = optimum_picture.resize(values.picture_size)
    if mode == "t":
        test()
        sys.exit(1)


def set_new_generation(gen: list):
    global new_generation
    new_generation = gen


def generate_first_generation():
    firstgeneration = [0] * size_of_first_generation
    for x in range(0, size_of_first_generation):
        firstgeneration[x] = generation.Network(values.fp_sizes)
    return firstgeneration


def get_improvement_list():
    improvements = []
    for x in range(1, len(avg_fit)):
        improvements.append(avg_fit[x] - avg_fit[x-1])
    return improvements


def get_average_improvement():
    avg = 0
    improvements = get_improvement_list()
    if len(improvements) == 0:
        return 0
    for x in improvements:
        avg += x
    avg /= len(improvements)
    return avg


def generate_first_generation_string(opt: str):
    length = len(opt)
    firstgeneration = []
    for x in range(0, size_of_first_generation):
        tempstring = ''
        for y in range(0, length):
            tempstring += random.choice(string.ascii_letters)
        firstgeneration.append(tempstring)
    return firstgeneration


def get_fitness_str(individual: str):
    fitness = 0
    for x in range(0, len(individual)):
        if individual[x] == 'a':
            fitness += 1
    return fitness/(len(individual))


def get_fitness_online(individual: generation.Network):
    return -1


def get_average_fitness():
    fitness = 0
    list = get_fitness_list(new_generation)

    for x in list:
        fitness +=x

    fitness /= len(list)
    return fitness


def get_fitness(individual: generation.Network):
    if mode == "m":
        return get_fitness_manual(individual)
    elif mode == "r":
        return get_fitness_automatic_red(individual)
    elif mode == "p":
        return get_fitness_automatic_picture(individual)
    elif mode == "s":
        return get_fitness_automatic_silhouette(individual)
    else:
        sys.exit(1)


def get_fitness_manual(individual: generation.Network):
    draw_individual(individual)
    fitness = simpledialog.askinteger("Rating", "Please rate the displayed picture from 0 to 100")
    master.update()
    return fitness;


def get_fitness_automatic_picture(individual: generation.Network):
    ind_pim = generate_visual_fp(individual)
    diff_r = 0
    diff_g = 0
    diff_b = 0
    pixels_ind = ind_pim.load()
    pixels_opt = optimum_picture.load()
    for x in range(0, values.picture_size_x):
        for y in range(0, values.picture_size_y):
            diff_r += abs(pixels_opt[x, y][0] - pixels_ind[x, y][0])
            diff_g += abs(pixels_opt[x, y][1] - pixels_ind[x, y][1])
            diff_b += abs(pixels_opt[x, y][2] - pixels_ind[x, y][2])

    diff_r /= values.size ** 2
    diff_g /= values.size ** 2
    diff_b /= values.size ** 2

    return 1 - (((diff_r + diff_g + diff_b) / 3) / 255)


def get_fitness_automatic_silhouette(individual: generation.Network):
    ind_pim = generate_visual_fp(individual)
    diff = 0
    pixels_ind = ind_pim.load()
    pixels_opt = optimum_picture.load()
    for x in range(0, values.picture_size_x):
        for y in range(0, values.picture_size_y):
            avg_ind = (pixels_ind[x, y][0] + pixels_ind[x, y][1] + pixels_ind[x, y][2]) / 3
            avg_opt = (pixels_opt[x, y][0] + pixels_opt[x, y][1] + pixels_opt[x, y][2]) / 3
            diff += abs(avg_opt - avg_ind)

    diff /= values.size**2

    return 1 - (diff / 255)


def get_fitness_automatic_red(individual: generation.Network):
    redness = 0
    greenness = 0
    blueness = 0

    a = individual.feedforward(values.input_fp)
    for x in range(0, int(a.size)):
        if 0 <= x < values.size**2:
            redness += a[x]
        if values.size**2 <= x < (values.size**2)*2:
            greenness += a[x]
        if (values.size**2)*2 <= x < (values.size**2)*3:
            greenness += a[x]

    redness /= (a.size / 3)
    greenness /= (a.size / 3)
    blueness /= (a.size / 3)

    fitness = redness - ((greenness + blueness) / 2)
    return generation.sigmoid(fitness)


def mutate_generation_string(gen: list):
    for x in range(0, len(gen)):
        if pyr.rand() <= chance_of_mutation_per_individual:
            gen[x] = mutate_single_individual_string(gen[x])


def draw_new_generation():
    pil_img = pim.open("Latest.jpg")
    pil_img = pil_img.resize((800, 800))
    img = pik.PhotoImage(pil_img)

    canvas.create_image(0, 0, anchor=NW, image=img)
    master.update()


def draw_individual(individual: generation.Network):
    pil_img = generate_visual_fp(individual)
    pil_img = pil_img.resize((800, 800))
    img = pik.PhotoImage(pil_img)

    canvas.create_image(0, 0, anchor=NW, image=img)
    master.update()


def mutate_generation(generation: list):
    for x in range(0, len(generation)):
        if pyr.rand() <= chance_of_mutation_per_individual:
            generation[x] = mutate_single_individual(generation[x])


def get_fitness_list(gen: list):
    fitnesslist = []
    for x in range(0, len(gen)):
        fitnesslist.append(get_fitness(gen[x]))
    return fitnesslist


def get_diversity_list(gen: list):
    diversity_list = []
    for x in range(0, len(gen)):
        diversity_list.append(get_diversity(gen[x]))
    return diversity_list


def get_rating_list(gen: list):
    rating_list = []
    for x in range(0, len(gen)):
        rating_list.append(get_rating(gen[x]))
    return rating_list


def get_rating_string(individual: str):
    inversediversity = (get_diversity(individual))**2
    inversefitness = (get_fitness(individual))**2
    rating = math.sqrt(inversediversity+inversefitness)/math.sqrt(2)
    return rating


def get_rating(individual: generation.Network):
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


def get_diversity_string(individual: str):
    diversity = 0
    for newindividual in new_generation:
        diversity += different_chars(individual, newindividual)
    if len(new_generation) <= 0:
        return 0
    else:
        return (diversity/len(new_generation))/len(individual)


def get_diversity(individual: generation.Network):
    diversity = 0
    for new_individual in new_generation:
        diversity += individual.difference(new_individual)
    if len(new_generation) <= 0:
        return 0
    else:
        return diversity/len(new_generation)


def different_chars(cd1: str, cd2: str):
    diffchars = 0
    for x in range(0, len(cd1)):
        if cd1[x] == cd2[x]:
            diffchars += 1
    return diffchars


def crossover_string(generation: list):
    x, y = '', ''
    while x == y:
        x = select_surviving_individual(generation)
        y = select_surviving_individual(generation)
    return generate_children_p2(x, y)


def crossover(generation: list):
    x = select_surviving_individual(generation)
    y = select_surviving_individual(generation)
    while x == y:
        x = select_surviving_individual(generation)
        y = select_surviving_individual(generation)
    return x.crossover(y)


def mutate_single_individual(individual: generation.Network):
    individual.mutate(gene_mutation_chance, gene_mutation_size)
    return individual


def mutate_single_individual_string(individual: str):
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


def save_generation(g: int):
    for x in range(0, len(first_generation)):
        p = first_generation[x]
        im = generate_visual_fp(p)
        im.save("Latest.jpg", "JPEG")


def save_new_generation(g: int):
    for x in range(0, len(new_generation)):
        p = new_generation[x]
        im = generate_visual_fp(p)
        im.save("Latest.jpg", "JPEG")


def generate_visual_fp(individual: generation.Network):
    im = pim.new("RGB", values.picture_size, color=0)
    pixels = im.load()
    value = individual.feedforward(values.input_fp)
    for x in range(values.picture_size_x):
        for y in range(values.picture_size_y):
            ir = (values.picture_size_x * x + y)
            ig = (values.picture_size_x * x + y)+values.size**2
            ib = (values.picture_size_x * x + y)+(values.size**2)*2

            pixels[x, y] = (int(value[ir]*255), int(value[ig]*255), int(value[ib]*255))

    return im


def test():
    print("------------TESTING-------------")
    ind = generation.Network(values.fp_sizes)
    draw_individual(ind)
    input()
    ind.mutate(gene_mutation_chance, gene_mutation_size)
    draw_individual(ind)
    input()

main()
