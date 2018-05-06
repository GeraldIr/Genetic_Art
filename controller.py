#Written by Gerald Walter Irsiegler

import generation
from PIL import Image
import values


def rate_candidate():
    return -1


def get_next_candidate_visual():
    return -1


def test():
    value = generation.get_pixel_value(32, 32)
    print(int(value[0][0] * 255), int(value[1][0] * 255), int(value[2][0] * 255))
    value = generation.get_pixel_value(63, 63)
    print(int(value[0][0] * 255), int(value[1][0] * 255), int(value[2][0] * 255))


def generate_visual(individual):
    im = Image.new("RGB", values.picture_size, color=0)
    pixels = im.load()
    for x in range(values.picture_size_x):
        for y in range(values.picture_size_y):
            value = generation.get_pixel_value(x, y)
            pixels[x, y] = (int(value[0][-1]*255), int(value[1][-1]*255), int(value[2][-1]*255))

    im.save("hello.jpg", "JPEG")
    return -1

generate_visual(1)
# test()