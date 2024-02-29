from PIL import Image, ImageDraw
from bybit_1 import *


# draw.rectangle((0, height - 50, width, height), fill=(0, 0, 0))
def do_pointer_green(i, bottom, draw, height):
    draw.rectangle((10 * i, height - bottom + 10, 10 * i + 10, height - bottom + 20), fill=(0, 128, 0),
                   outline=(0, 0, 0))


def do_pointer_red(i, top, draw, height):
    draw.rectangle((10 * i, height - top - 20, 10 * i + 10, height - top - 10), fill=(255, 0, 0), outline=(0, 0, 0))
def do_pointer_red1(i, top, draw, height):
    draw.rectangle((10 * i, height - top - 20, 10 * i + 10, height - top - 10), fill=(255, 123, 124), outline=(0, 0, 0))
def do_pointer_red2(i, top, draw, height):
    draw.rectangle((10 * i, height - top - 20, 10 * i + 10, height - top - 10), fill=(255, 123, 0), outline=(0, 0, 0))

# m = export(1, "KSMUSDT", 5)[-10000:]
# orders = [[1], [5]]

def crasota(m, orders):
    m0 = [i[0] for i in m]
    m1 = [i[1] for i in m]
    buf = max(m0 + m1) - min(m0 + m1)
    mi = min(m0 + m1)
    ma = max(m0 + m1)
    width = 10 * len(m0) + 10
    height = 2000
    m0_do = [i - mi for i in m0]
    m1_do = [i - mi for i in m1]
    one_dollar_to_pixel = (height - 100) / buf
    m0_do1 = [one_dollar_to_pixel * i + 50 for i in m0_do]
    m1_do1 = [one_dollar_to_pixel * i + 50 for i in m1_do]
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    for i in range(len(m0_do1)):
        if m0_do1[i] > m1_do1[i]:
            color = (255, 0, 0)
            position = (10 * i, height - m0_do1[i], 10 * i + 10, height - m1_do1[i])
        else:
            color = (0, 128, 0)
            position = (10 * i, height - m1_do1[i], 10 * i + 10, height - m0_do1[i])
        draw.rectangle(position, fill=color, outline=(0, 0, 0))

    for pos in range(len(m1_do1)):
        if pos in orders[1]:
            do_pointer_green(pos, min(m0_do1[pos], m1_do1[pos]), draw, height)
        if pos in orders[0]:
            do_pointer_red(pos, max(m0_do1[pos], m1_do1[pos]), draw, height)

    img.show("test.png")
# crasota(m, orders)
