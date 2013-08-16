__author__ = 'ialbert'
import os, logging, re
from itertools import *

_logger = logging.getLogger(__name__)

MAX_SIZE_KB = 500

def parse_meta(fname):
    """
    Parses meta information from a file
    """
    meta = dict()
    stream = file(fname)
    stream = filter(lambda x: x.startswith('##'), stream)
    stream = map(lambda x: x.strip("#").split(), stream)
    stream = filter(lambda x: len(x) > 1, stream)
    for r in stream:
        meta[r[0]] = " ".join(r[1:]).strip()
    return meta

def get_size(path):
    statinfo = os.stat(path)
    size = 1.0 * statinfo.st_size / 1024
    return size

class File(object):
    "Represents a file object with attributes"

    def __init__(self, fname, root=None):
        self.root  = root
        self.fname = fname
        self.fpath = os.path.join(root, fname)
        self.rpath = os.path.relpath(self.root, self.fpath)
        self.meta  =  dict(name=self.nice_name, sortkey=fname)
        if not self.skip_file:
            self.meta.update(parse_meta(self.fpath))

    @property
    def nice_name(self):
        "Attempts to generate a nicer name from the filename"
        head, tail = os.path.split(self.fname)
        base, ext = os.path.splitext(tail)
        return base.title().replace("-", " ").replace("_", " ")

    def content(self):
        return file(self.fpath).read()

    @property
    def name(self):
        return self.meta.get("name", "*** name not set ***")

    @property
    def size(self):
        "Decides wether to skip a file"
        return get_size(self.fpath)

    @property
    def skip_file(self):
        return self.size > MAX_SIZE_KB

    def write(self, output_folder, text):
        loc = os.path.join(output_folder, self.fname)
        d = os.path.dirname(loc)
        if not os.path.exists(d):
            os.makedirs(d)
        with open(loc, "wb") as fp:
            fp.write(text)
