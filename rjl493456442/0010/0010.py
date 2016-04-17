"""
    author: gary rong
    date : 2016/04/17
    description: generate a verification jpeg with specific length char
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

charset = ""
bg_color = (255, 255, 255) # white background color
font_color = (255, 0, 0) # red font color

image_size = (250, 40)
width, height = image_size
font_size = 22
font_type = "Arial.ttf"
text_length = 5
disturbance_point_number = 200
disturbance_line_number = 10

image = Image.new('RGB', image_size, bg_color)
draw_painter = ImageDraw.Draw(image)


def init_charset():
    """
        init the charset for sample
    """
    global charset
    lower_letters = "".join(map(chr, range(97, 122)))
    upper_letters = lower_letters.upper()
    num_letters = "".join(map(str, range(0,10)))
    charset = lower_letters + upper_letters + num_letters

def draw_image():
    text_list = [random.choice(charset) for i in range(text_length)]
    text = ''
    for char in text_list:
        text += random.randint(0,2) * " "
        text += char
    font = ImageFont.truetype(font_type, font_size)
    draw_painter.text((10, 2), text, font = font, fill = font_color)

def chaos():
    def transform():
        global image
        global draw_painter
        params = [1 - float(random.randint(1, 2)) / 100,0,0,0,1 - float(random.randint(1, 10)) / 100,float(random.randint(1, 2)) / 500,0.001,float(random.randint(1, 2)) / 500]
        image = image.transform(image_size, Image.PERSPECTIVE, params)
        draw_painter = ImageDraw.Draw(image)
    def add_point():
        for i in range(disturbance_point_number):
            point_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw_painter.point((x, y), point_color)
    def add_line():
        for i in range(disturbance_line_number):
            line_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw_painter.line(((x1, y1), (x2, y2)), line_color)
    transform()
    add_point()
    add_line()

def flush_image():
    global image
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    image = image.filter(ImageFilter.SMOOTH)

def save_image():
    image.save("verification.jpg")

if __name__ == "__main__":
    init_charset()
    draw_image()
    chaos()
    flush_image()
    save_image()
