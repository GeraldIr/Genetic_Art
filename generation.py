#Written by Gerald Walter Irsiegler


import math
import values
import numpy as np


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


network = Network(values.sizes)


def get_pixel_value(x: int, y: int):
    inputs = [0] * values.number_of_inputs
    # inputs[(x*values.picture_size_x)+y] = 1

    number = values.picture_size_x*x + y
    for x in range(len(bin(number))-2):
        inputs[x] = int(bin(number)[x+2])

    a = network.feedforward(inputs)
    return a
    

def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))

