from colorthief import ColorThief
from io import BytesIO

def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def get_palette(img):
    color_thief = ColorThief(BytesIO(img.content))
    palette = color_thief.get_palette(color_count=6)
    palette_hex = [rgb2hex(r=color[0], g=color[1], b=color[2]) for color in palette]

    return palette_hex