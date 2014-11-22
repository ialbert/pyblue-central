__author__ = 'ialbert'
import os, logging, re, itertools, string, time
from itertools import *

logger = logging.getLogger(__name__)

# Meta labels that should be treated as lists
LIST_TAGS = set("tags".split())


class File(object):
    """
    Represents a file object within PyBlue.
    Each file object is visible in the template context.
    """
    MAX_SIZE_MB = 5
    IMAGE_EXTENSIONS = set(".png .jpg .gif .svg".split())
    TEMPLATE_EXTENSIONS = set(".html .htm".split())

    def __init__(self, fname, root):
        self.root = root
        self.fname = fname

        # Full path to the file.
        self.fpath = os.path.join(root, fname)

        if not os.path.isfile(self.fpath):
            logger.warning("file does not exist: %s" % fname)
            return

        # Fill in various file related stats.
        statinfo = os.stat(self.fpath)
        self.size = statinfo.st_size

        mt = time.gmtime(statinfo.st_mtime)
        self.last_modified = time.strftime("%A, %B %d, %Y", mt)

        ct = time.gmtime(statinfo.st_ctime)
        self.created_date = time.strftime("%A, %B %d, %Y", ct)

        # Directory that contains the file.
        self.dname = os.path.dirname(self.fpath)
        self.ext = os.path.splitext(fname)[1]

        # Treated specially when rendering galleries.
        self.is_image = self.ext in self.IMAGE_EXTENSIONS

        # Only templates will be handled via Django.
        self.is_template = self.ext in self.TEMPLATE_EXTENSIONS

        # The nice name is used by default for name and title.
        nice = self.nice_name(fname)

        # This object stores the metadata.
        self.meta = dict(fname=fname, name=nice, title=nice, sortkey="5")

        # Only parse html files for metadata
        if self.is_template:
            self.meta.update(parse_meta(self.fpath))

    def nice_name(self, fname):
        "Attempts to generate a nicer name from the filename"
        head, tail = os.path.split(fname)
        base, ext = os.path.splitext(tail)
        name = base.title().replace("-", " ").replace("_", " ")
        if self.is_image:
            # add back extensions for images
            name = name + self.ext
        return name

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

    def relpath(self, start=None):
        """
        Relative path of this file from the start location
        """
        start = start or self
        rpath = os.path.relpath(self.root, start.dname)
        rpath = os.path.join(rpath, self.fname)
        return rpath

    def __getattr__(self, name):
        "Fallback context attributes"
        value = self.meta.get(name, None)
        if not value:
            logger.error(self.meta)
            logger.error(" *** attribute '%s' for '%s' not found" % (name, fname))
            value = '?'
        return value

    def __repr__(self):
        return "File: %s (%s)" % (self.name, self.fname)

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

    # Find lines that are Django comments.
    stream = filter(lambda x: x.startswith('{#'), stream)

    # Remove comment characters.
    stream = map(lambda x: x.strip("{#"), stream)

    stream = map(lambda x: x.strip("#}"), stream)

    # Split each line by the semicolons.
    stream = map(lambda x: x.split(';'), stream)

    # Flatten nested lists
    flat = [item for s in stream for item in s]

    # Generate the metavalues into the dictionary.
    for elems in flat:

        # Split each element by the = sign.
        parts = elems.split('=')
        if len(parts) != 2:
            continue
        name, values = parts[0].strip(), parts[1].strip()
        if name in LIST_TAGS:
            meta[name] = " ".join(values).strip()
        else:
            meta[name] = values

    return meta


def collect_files(root):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for f in sorted(filenames):
            absp = os.path.join(dirpath, f)
            path = os.path.relpath(absp, root)
            files.append(path)
    return files


def test():
    pass


if __name__ == '__main__':
    test()
