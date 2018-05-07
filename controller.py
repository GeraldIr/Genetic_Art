#Written by Gerald Walter Irsiegler

import generation
from PIL import Image
import values


def rate_candidate():
    return -1


def get_next_candidate_visual():
    return -1


def generate_visual(individual):
    im = Image.new("RGB", values.picture_size, color=0)
    pixels = im.load()
    for x in range(values.picture_size_x):
        for y in range(values.picture_size_y):
            value = generation.get_pixel_value(x, y)
            pixels[x, y] = (int(value[0][-1]*255), int(value[1][-1]*255), int(value[2][-1]*255))

    im.save("hello.jpg", "JPEG")
    im.show("Picture")
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

    im.save("Picture.jpg", "JPEG")
    im.show("Picture")
    return -1


def generate_visual_fp(individual):
    im = Image.new("RGB", values.picture_size, color=0)
    pixels = im.load()
    value = generation.get_pixel_values_picture()

    for x in range(values.picture_size_x):
        for y in range(values.picture_size_y):
            #ir = (values.picture_size_x * x + y)
            #ig = (values.picture_size_x * x + y)+(values.picture_size_x*values.picture_size_y)
            #ib = (values.picture_size_x * x + y)+(2*values.picture_size_x*values.picture_size_y)

            ir = (values.picture_size_x * x + y)*3
            ig = ((values.picture_size_x * x + y)*3)+1
            ib = ((values.picture_size_x * x + y)*3)+2

            print(str(int(value[ir]*255)) + ", " + str(int(value[ig]*255)) + ", " + str(int(value[ib]*255)))
            pixels[x, y] = (int(value[ir]*255), int(value[ig]*255), int(value[ib]*255))

    im.save("Picture.jpg", "JPEG")
    im.show("Picture")
    return -1


def test():
    cmd = input("Full Picture (fp), or Pixel Based Neural Network (pb)?")
    if cmd == "fp":
        generate_visual_fp(1)
    elif cmd == "pb":
        generate_visual(1)
    else:
        print("Exiting.")

# generate_visual(1)
# generate_visual_fp(1)
test()
