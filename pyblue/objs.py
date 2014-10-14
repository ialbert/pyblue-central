__author__ = 'ialbert'
import os, logging, re, itertools, string, time
from StringIO import StringIO
from itertools import *

# Markdown is available by default.
# Other renderers are optional.
from .markdown import markdown

try:
    # Restructured text.
    from docutils import core
except ImportError, exc:
    core = False

try:
    # Import the ASCII doc renderer.
    from asciidocapi import AsciiDocAPI
    asciidoc = True
except ImportError:
    asciidoc = False

logger = logging.getLogger(__name__)

# Meta labels that should be treated as lists
LIST_TAGS = set("tags".split())

class File(object):
    """
    Represents a file object within PyBlue.
    Each file object is visible in the template context.
    """
    MAX_SIZE_MB = 5

    def __init__(self, fname, root):
        self.root = root
        self.fname = fname
        self.fpath = os.path.join(root, fname)
        self.dname = os.path.dirname(self.fpath)
        self.ext = os.path.splitext(fname)[1]
        self.name = self.nice_name
        # This object stores the metadata.
        self.meta = dict(fname=fname, name=self.name, sortkey="5")

        # large files should not be parsed
        if not self.skip_file:
            self.meta.update(parse_meta(self.fpath))

    @property
    def nice_name(self, fname):
        "Attempts to generate a nicer name from the filename"
        head, tail = os.path.split(fname)
        base, ext = os.path.splitext(tail)
        name = base.title().replace("-", " ").replace("_", " ")
        if self.is_image:
            # add back extensions for images
            name = name + self.ext
        return name

    @property
    def skip_file(self):
        "Skips larger files"
        return self.size > self.MAX_SIZE_MB

    @property
    def size(self):
        "File size in MB"
        return get_size(self.fpath)

    @property
    def is_image(self):
        return self.ext in (".png", ".jpg", ".gif")

    def write(self, output, text):
        """
        Writes the text into an output folder
        """
        loc = os.path.join(output, self.fname)

        if os.path.abspath(loc) == os.path.abspath(self.fpath):
            raise Exception("may not overwrite the original file %s" % loc)

        d = os.path.dirname(loc)
        if not os.path.exists(d):
            os.makedirs(d)
        with open(loc, "wb") as fp:
            fp.write(text)

    def url(self, start=None, text=''):
        """
        Relative path of the file from the start location
        """
        start = start or self
        rpath = os.path.relpath(self.root, start.dname)
        rpath = os.path.join(rpath, self.fname)

        return rpath, text or self.name

    @property
    def last_modified(self):
        t = os.path.getmtime(self.fpath)
        t = time.gmtime(t)
        return "%s" % time.strftime("%A, %B %d, %Y", t)

    def __getattr__(self, name):
        "Fallback context attributes"
        value = self.meta.get(name)
        if not value:
            raise Exception("context attribute %s not found" % name)
        return value


    def __repr__(self):
        return "File: %s (%s)" % (self.name, self.fname)

def render_rst(text):
    """reST renderer"""
    if not core:
        logger.error("Unable to import docutils.core.")
        return text
    html = core.publish_string(text, writer_name='html')
    return html


def render_md(text):
    """Markdown renderer"""
    html = markdown(text, safe_mode=False, smart_emphasis=True)
    return html


def render_asc(text):
    """ASCIIdoc renderer"""
    if not asciidoc:
        logger.error("Unable to import asciidocapi.py")
        return text
    inp = StringIO(text)
    out = StringIO()
    ad = AsciiDocAPI()
    ad.execute(inp, out, backend="html4")
    html = out.getvalue()
    print (html)
    return html



def parse_meta(fname):
    """
    Parses meta information from a file. Returns a dictionary.
    """

    # This will store the metadata.
    meta = dict()

    # Take just the first lines.
    stream = islice(file(fname), 100)

    # Strip the lines.
    stream = map(string.strip, stream)

    # Find locations with double ## signs.
    stream = filter(lambda x: x.startswith('##'), stream)

    # Remove comment characters.
    stream = map(lambda x: x.strip("#"), stream)

    # Split each line by whitespace.
    stream = map(string.split, stream)

    # Keep only lines have at least two elements
    stream = filter(lambda x: len(x) > 1, stream)

    # Generate the metavalues into the dictionary.
    for elems in stream:
        name, values = elems[0], elems[1:]
        if name in LIST_TAGS:
            meta[name] = values
        else:
            meta[name] = " ".join(values).strip()
    return meta

def get_size(path, unit=1024 * 1024):
    statinfo = os.stat(path)
    size = 1.0 * statinfo.st_size / unit
    return size

def test():
    pass

if __name__ == '__main__':
    test()
