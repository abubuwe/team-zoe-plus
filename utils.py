from cache_to_disk import cache_to_disk
import os

DEBUG = bool(os.environ.get("DEBUG", False))

# I'm doing this to conserve our API credits for now:
def debug_picklify(function):
    if not DEBUG:
        return function
    
    return cache_to_disk(0)(function)
