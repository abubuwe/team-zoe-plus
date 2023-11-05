from cache_to_disk import cache_to_disk
import os

DEBUG = bool(os.environ.get("DEBUG", False))

# I'm doing this to conserve our API credits for now:
def debug_picklify(function):
    if not DEBUG:
        return function
    
    return cache_to_disk(0)(function)

def get_complementary_colour(color: str):
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