#Written by Gerald Walter Irsiegler

import random
import string
from numpy import random as pyr
import math
import controller

current_weights;
current_biases;

def setup_weights(individual: list):
    global current_weights;
    global current_biases;

    current_biases[0] = individual[1][0:controller.number_of_inputs-1]

    for i in range(0, controller.number_of_hidden_layers):
        current_biases[i+1] = individual[1][controller.number_of_inputs+(i*controller.size_of_hidden_layers):controller.number_of_inputs+(i*controller.size_of_hidden_layers)+controller.size_of_hidden_layers-1];

    current_biases [controller.number_of_hidden_layers+1] = individual[1][-controller.number_of_outputs:];



def get_pixel_value(x: int, y: int):
    inputs = [0] * controller.number_of_inputs;
    inputs[(x*controller.picture_size_x)+y] = 1;
    

def sigmoid(x):
    return 1 / (1 + math.exp(-x))