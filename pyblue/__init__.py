VERSION = '2.0.0'

import sys, os


def join (*args):
    return os.path.abspath(os.path.join(*args))

PYBLUE_DIR = os.path.abspath(os.path.dirname(__file__))
zip_file = join(PYBLUE_DIR, '..', 'lib', 'packages.zip')

# Add the required packages to the import path.
# We append at the end so that local environments may override it.
sys.path.append(zip_file)



