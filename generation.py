#Written by Gerald Walter Irsiegler


import math
import values
import numpy as np
from numpy import random as pyr


class Network(object):

    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]

    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a

    def mutate(self):
        for b in self.biases:
            if pyr.rand() < 0.1:
                if pyr.rand() < 0.5:
                    b += (pyr.rand() - 0.5) / 10
                else:
                    b *= 1 + ((pyr.rand() - 0.5) / 10)
        for w in self.weights:
            if pyr.rand() < 0.5:
                if pyr.rand() < 0.5:
                    w += (pyr.rand() - 0.5) / 10
                else:
                    w *= 1 + ((pyr.rand() - 0.5) / 10)

    def crossover(self, other):
        child1 = Network(values.fp_sizes)
        child2 = Network(values.fp_sizes)

        for x in range(0, int(len(self.weights))):
            for y in range(0, len(self.weights[0])):
                if pyr.rand() < 0.5:
                    child1.weights[x][y] = self.weights[x][y]
                    child2.weights[x][y] = other.weights[x][y]
                else:
                    child2.weights[x][y] = self.weights[x][y]
                    child1.weights[x][y] = other.weights[x][y]

        for x in range(0, int(len(self.biases))):
            for y in range(0, int(len(self.biases[0]))):
                if pyr.rand() < 0.5:
                    child1.biases[x][y] = self.biases[x][y]
                    child2.biases[x][y] = other.biases[x][y]
                else:
                    child2.biases[x][y] = self.biases[x][y]
                    child1.biases[x][y] = other.biases[x][y]

        return child1, child2

    def difference(self, other):
        bias_diff = 0
        weight_diff = 0

        bias_list1 = []
        bias_list2 = []
        weight_list1 = []
        weight_list2 = []

        for bs in self.biases:
            for bsx in bs:
                bias_list1.append(bsx)
        for bo in other.biases:
            for box in bo:
                bias_list2.append(box)
        for ws in self.weights:
            for wsx in ws:
                weight_list1.append(bsx)
        for wo in other.weights:
            for wox in wo:
                weight_list2.append(box)

        for x in range(0, len(bias_list1)):
            bias_diff += abs(bias_list1[x] - bias_list2[x])

        for x in range(0, len(weight_list1)):
            weight_diff += abs(weight_list1[x] - weight_list2[x])


            # bias_diff += bias_list1[x] - bias_list2[x]
        # for x in range(0, len(self.weights)):
            # weight_diff += weight_list1[x] - weight_list2[x]
        bias_diff /= len(bias_list1)
        weight_diff /= len(weight_list1)

        diff = (bias_diff + weight_diff) / 2
        return sigmoid(diff)


def get_pixel_value(individual: Network, x: int, y: int):
    inputs = [0] * values.number_of_inputs
    # inputs[(x*values.picture_size_x)+y] = 1

    number = values.picture_size_x*x + y
    for x in range(len(bin(number))-2):
        inputs[x] = int(bin(number)[x+2])

    a = individual.feedforward(inputs)
    return a
    

def get_pixel_values_picture(individual: Network):
    a = individual.feedforward(values.input_fp)
    return a


def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))
