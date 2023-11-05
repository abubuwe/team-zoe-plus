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
    print(hsv)
    return hsv_to_rgb((hsv[0] + 0.5) % 1, hsv[1], hsv[2])

def get_complementary(color: str):
    # strip the # from the beginning
    color = color[1:]
 
    # convert the string into hex
    color = int(color, 16)
 
    # invert the three bytes
    # as good as substracting each of RGB component by 255(FF)
    comp_color = 0xFFFFFF ^ color
 
    # convert the color back to hex by prefixing a #
    comp_color = "#%06X" % comp_color
 
    # return the result
    return comp_color