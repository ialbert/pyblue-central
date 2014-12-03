#
# The data file named context.py in the root folder
# will be loaded automatically into the page.
#

NUMBERS = range(5)

# It may contain any valid python construct.

def say_hello(name):
    return "Hello %s" % name

greeting = say_hello("World!")
