import math
import numpy as np

picture_size = (16, 16)
picture_size_x = picture_size[0]
picture_size_y = picture_size[1]
number_of_inputs = int(np.log2(picture_size_x * picture_size_y))  # 64
number_of_outputs = 3
number_of_hidden_layers = 3
size_of_hidden_layers = 16
sizes = [number_of_inputs, 16, number_of_outputs]
