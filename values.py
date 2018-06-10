import math
import numpy as np

size = 2
picture_size = (size, size)
picture_size_x = picture_size[0]
picture_size_y = picture_size[1]
number_of_inputs = int(np.log2(picture_size_x * picture_size_y))  # 64
color_channels = 3
fp_number_of_outputs = picture_size_x * picture_size_y * color_channels
number_of_outputs = color_channels
number_of_hidden_layers = 3
size_of_hidden_layers = 16
input_fp = 1
sizes = [number_of_inputs, 16, number_of_outputs]
fp_sizes = [1, fp_number_of_outputs, fp_number_of_outputs]
