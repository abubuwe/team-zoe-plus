from cache_to_disk import cache_to_disk
import os
from colorutils import Color
from colorsys import rgb_to_hsv, hsv_to_rgb

DEBUG = True

# I'm doing this to conserve our API credits for now:
def debug_picklify(function):
    if not DEBUG:
        return function
    
    return cache_to_disk(0)(function)

def complementary_colour(colour: str):
    """ Finds the complementary of a hex RGB colour """
    c = Color(hex = colour)
    hsv = rgb_to_hsv(c.red, c.green, c.blue)
    return hsv_to_rgb((hsv[0] + 0.5) % 1, hsv[1], hsv[2])