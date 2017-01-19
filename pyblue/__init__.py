import sys

VERSION = '2017.01.13'

# Python 3.6 only.
CURRENT_VERSION = sys.version_info
REQUIRED_VERSION = (3, 6)

if (CURRENT_VERSION < REQUIRED_VERSION):
    sys.exit("This program requires Python: {} you have: {}".format(REQUIRED_VERSION, CURRENT_VERSION))


