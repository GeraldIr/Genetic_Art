#Written by Gerald Walter Irsiegler

import generation
import genetics
from PIL import Image
import values


def init():
    genetics.init("test")
    loop()


def loop():
    while True:
        for x in range(genetics.max_generation_size):
            current_candidate = genetics.first_generation[x]
            rate_candidate(current_candidate)


def rate_candidate(candidate):
    return input("Rate the following word '" + candidate + "' (1-100): ")


def get_next_candidate_visual():
    return -1


def generate_visual(individual):
    im = Image.new("RGB", values.picture_size, color=0)
    pixels = im.load()
    for x in range(values.picture_size_x):
        for y in range(values.picture_size_y):
            value = generation.get_pixel_value(individual, x, y)
            pixels[x, y] = (int(value[0][-1]*255), int(value[1][-1]*255), int(value[2][-1]*255))

    return im


def generate_visual_fp_bw(individual):
    im = Image.new("L", values.picture_size, color=0)
    pixels = im.load()
    value = generation.get_pixel_values_picture(individual)

    for x in range(values.picture_size_x):
        for y in range(values.picture_size_y):
            index = values.picture_size_x * x + y
            print(int(value[index]*255))
            pixels[x, y] = int(value[index]*255)

    im.save("Picture.jpg", "JPEG")
    im.show("Picture")
    return im

# generate_visual(1)
# generate_visual_fp(1)
