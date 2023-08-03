import sys

VERSION = '2022.08.01'

CURRENT_VERSION = sys.version_info
REQUIRED_VERSION = (3, 6)

if (CURRENT_VERSION < REQUIRED_VERSION):
    sys.exit("This program requires Python: {} or above. You have version: {}".format(REQUIRED_VERSION, CURRENT_VERSION))


