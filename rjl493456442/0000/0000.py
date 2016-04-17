#!/usr/bin/env python
'''
    draw a number to your avatar
'''

from PIL import Image, ImageDraw, ImageFont

IMAGE_ORIGINAL = "avatar.jpg"
IMAGE_AFRER_PROCESS = None

NUMBER = 4

FONT_COLOR = (255, 255, 255)
FONT = "Arial.ttf"
FONT_SIZE = 130
FONT_INFO = (FONT, FONT_SIZE, FONT_COLOR)

CIRCLR_SIZE = 150
CIRCLR_COLOR = (255, 0, 0)
CIRCLR_INFO = (CIRCLR_SIZE, CIRCLR_COLOR)
def add_number(number, font_info, circle_info):
    """
    Args:
        1) number: the number to be draw
        2) font_info: a tuple contains font information like font type, size, color
        3) circle_info: a tuple contains circle information
    """
    try:
        image = Image.open(IMAGE_ORIGINAL)
    except IOError, e:
        print "image can not be found"

    # first draw a circle with red color
    # the position of the circle is on the top-right corner of the image
    # the r of the circle is 50px

    circle_position = [image.size[0] - circle_info[0], 0, image.size[0], circle_info[0]]
    ImageDraw.Draw(image).ellipse(circle_position, circle_info[1])

    text = str(number)
    font = ImageFont.truetype(font_info[0], font_info[1])
    # put text in the top right corner
    # consider the size of the font, the adjustment of the position is necessary
    position = (image.size[0] - 115, 10)
    ImageDraw.Draw(image).text(position, text, font_info[2], font)
    image.show()

if __name__ == "__main__":
    add_number(NUMBER, FONT_INFO, CIRCLR_INFO)
