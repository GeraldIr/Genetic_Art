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


def generate_visual_fp_bw(individual):
    im = Image.new("L", values.picture_size, color=0)
    pixels = im.load()
    value = generation.get_pixel_values_picture()

    for x in range(values.picture_size_x):
        for y in range(values.picture_size_y):
            index = values.picture_size_x * x + y
            print(int(value[index]*255))
            pixels[x, y] = int(value[index]*255)

    im.save("hello.jpg", "JPEG")
    return -1


def generate_visual_fp(individual):
    im = Image.new("RGB", values.picture_size, color=0)
    pixels = im.load()
    value = generation.get_pixel_values_picture()

    for x in range(values.picture_size_x):
        for y in range(values.picture_size_y):
            ir = (values.picture_size_x * x + y)
            ig = (values.picture_size_x * x + y)+(values.picture_size_x*values.picture_size_y)
            ib = (values.picture_size_x * x + y)+(2*values.picture_size_x*values.picture_size_y)

            print(int(value[ir]*255))
            pixels[x, y] = (int(value[ir]*255), int(value[ig]*255), int(value[ib]*255))


    im.save("hello.jpg", "JPEG")
    return -1

# generate_visual(1)
generate_visual_fp(1)
# test()