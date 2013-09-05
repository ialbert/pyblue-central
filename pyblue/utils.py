__author__ = 'ialbert'
import os, logging, re, itertools
from StringIO import StringIO
from itertools import *
import docutils.core

try:
    from asciidocapi import AsciiDocAPI
    asciidoc = True
except ImportError:
    asciidoc = False

_logger = logging.getLogger(__name__)

MAX_SIZE_MB = 5

# tags that should be treated as lists
TAG_NAMES = "tags".split()

def rst(text):
    html = docutils.core.publish_string(text, writer_name='html')
    return html

def asc(text):
    if not asciidoc:
        _logger.error("Unable to import asciidocapi.py")
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
    Parses meta information from a file
    """
    meta = dict()
    stream = file(fname)
    stream = filter(lambda x: x.startswith('##'), stream)
    stream = map(lambda x: x.strip("#").split(), stream)
    stream = filter(lambda x: len(x) > 1, stream)
    for r in stream:
        meta[r[0]] = " ".join(r[1:]).strip()

    for tag in TAG_NAMES:
        if tag in meta:
            meta[tag] = meta[tag].split()
    return meta

def get_size(path, unit=1024*1024):
    statinfo = os.stat(path)
    size = 1.0 * statinfo.st_size / unit
    return size

def hello():
    return "Hello World!"

def test():
    text = """
    ABCD
    EFG
    123
    HIJ
    """
    lines = text.splitlines()
    lines = itertools.dropwhile(lambda x: not re.search("123", x), lines)
    lines = list(lines)
    print lines

if __name__ == '__main__':
    test()
