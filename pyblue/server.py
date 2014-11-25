# Python 2/3 ready.
from __future__ import print_function, unicode_literals, absolute_import, division

__author__ = 'ialbert'

import sys, os, imp, argparse, bottle, waitress, logging, re, time, string

from pyblue import VERSION, PYBLUE_DIR
DESCR = "PyBlue %s, static site generator" % VERSION
from django.conf import settings
from django.template import Context, Template
from django.template.loader import get_template
import django

logger = logging.getLogger(__name__)

def join (*args):
    return os.path.abspath(os.path.join(*args))

def get_parser():

    parser = argparse.ArgumentParser(description=DESCR)


    # Subcommands to the parser.
    subpar = parser.add_subparsers(dest="action",
            help=" action: serve, deploy")


    # The serve subcommand.
    serve = subpar.add_parser('serve',
                              help='serve the web site',
                              epilog="And that's how pyblue serves a directory during development.")

    serve.add_argument('-f', dest='root', metavar="DIR", default=".", required=False,
                       help='root directory to serve from (%(default)s)')

    serve.add_argument('-p', metavar="NUMBER", type=int, default=8080,
                       help='server port to bind to (%(default)s)')

    serve.add_argument('-v', dest="value", default=False, action="store_true",
                       help='increase message verbosity')


    # The gen subcommand.
    generate = subpar.add_parser('gen',
                                 help='generate the static website',
                                 epilog="And that's how pyblue generates static output.")

    generate.add_argument('-f', dest='root', metavar="DIR", default=".",
                       help='root directory to process (%(default)s)')

    generate.add_argument('-o', dest="output", metavar="DIR", type=str, required=True,
                       help='the target directory to generate output into')

    return parser

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
            try:
                lines = open(self.fpath).read().splitlines()[:20]
                self.meta.update(parse_lines(lines))
            except Exception, exc:
                logger.error(exc)

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
            logger.error(" *** attribute '%s' for '%s' not found" % (name, self.fname))
            value = '?'
        return value

    def __repr__(self):
        return "File: %s (%s)" % (self.name, self.fname)


int_patt = re.compile("\d+")
flt_patt = re.compile("\d+\.\d+")
lst_patt = re.compile("\[(?P<body>[\S\s]+?)\]")


def convert(text):
    text = text.strip()
    try:
        if flt_patt.match(text):
            return float(text)

        if int_patt.match(text):
            return int(text)

        m = lst_patt.search(text)
        if m:
            vals = m.group('body').split(",")
            vals = map(convert, vals)
            return vals

    except Exception, exc:
        logger.error("conversion error of %s -> %s " % (text, exc))
        return text
    return text


def parse_lines(lines):
    "Attempts to parse out metadata from django comments"
    meta = dict()
    lines = map(string.strip, lines)
    lines = filter(lambda x: x.startswith("{#"), lines)
    p = re.compile(r'{# (?P<name>\w+)\s?=\s?(?P<value>[\S\s]+)#}')
    for line in lines:
        m = p.search(line)
        if m:
            name, value = m.group('name'), m.group('value')
            meta[name] = convert(value)
    return meta


class PyBlue(object):
    TEMPLATE_EXTS = ".html .md .rst".split()
    IGNORE_EXTS = ".pyc".split()

    def django_init(self, context="context.py"):
        "Initializes the django engine. The root must have been set already!"
        tmpl_dir = join(PYBLUE_DIR, "templates")
        settings.configure(
            DEBUG=True, TEMPLATE_DEBUG=True,
            TEMPLATE_DIRS=(self.root, tmpl_dir),
            TEMPLATE_LOADERS = (
                'django.template.loaders.filesystem.Loader',
            ),
            INSTALLED_APPS= ["pyblue", "django.contrib.humanize"],
            TEMPLATE_STRING_IF_INVALID=" ??? ",
        )
        django.setup()


    def __init__(self, root, context="context.py", auto_refresh=True):

        # Initialize logging.
        logging.basicConfig()

        # Rescan all subdirectories for changes on each request.
        self.auto_refresh = auto_refresh

        # A set of strings that identifies the extension of the files
        # that should be processed using the Django templates.
        self.template_exts = set(self.TEMPLATE_EXTS)
        self.ignore_exts = set(self.IGNORE_EXTS)

        # The folder where the files to serve are located.
        # Do not set this attribute directly, use set_root() method instead.
        self.root, self.files = None, []

        # This is a method because it needs refresh the files on each request.
        self.set_root(root)

        # Initialize the django template engine.
        self.django_init()

        try:
            # Attempts to import a python module as a context
            ctx = imp.load_source('ctx', join(self.root, context))
        except Exception, exc:
            ctx = None
            logger.info("unable to import context module: %s" % context)

        def render(path):

            # This needs to rerun to pick up
            # new files that migh have been added in the meantime.
            # On the other hand might slow down large sites.
            if self.auto_refresh:
                self.set_root(self.root)

            logger.info(path)
            page = File(fname=path, root=self.root)
            if page.is_template:
                params = dict(page=page, root=self.root, context=ctx, files=self.files)
                templ = get_template(page.fname)
                cont = Context(params)
                return templ.render(cont)
            else:
                return bottle.static_file(path, root=self.root)

        # Make a shortcut to the renderer.
        self.render = render

        # The Bottle application will serve the pages.
        self.app = bottle.Bottle()
        self.app.route('/', method=['GET', 'POST', 'PUT', 'DELETE'])(lambda: self.render('index.html'))
        self.app.route('/<path:path>', method=['GET', 'POST', 'PUT', 'DELETE'])(lambda path: self.render(path))

    def set_root(self, path):
        "Sets the folder where the files to serve are located."
        self.root = os.path.abspath(path)

        # Reads all files in the root.
        self.files = [File(fname=path, root=self.root) for path in self.collect_files()]

    def collect_files(self):
        files = []
        for dirpath, dirnames, filenames in os.walk(self.root):
            for name in sorted(filenames):
                start, ext = os.path.splitext(name)
                if ext in self.ignore_exts:
                    continue
                absp = os.path.join(dirpath, name)
                path = os.path.relpath(absp, self.root)
                files.append(path)
        logger.info("%d files" % len(files))
        return files


    def serve(self, host='0.0.0.0', port=8080):
        "Launch the WSGI app development web server"
        waitress.serve(self.app, host=host, port=port)

def run():
    # Process command line arguments.
    parser = get_parser()

    # Trigger help on plain invocation.
    if len(sys.argv) < 2:
        sys.argv.append("--help")

    # Parse the command line.
    args = parser.parse_args(sys.argv[1:])

    if args.action == "serve":
        pb = PyBlue(root=args.root)
        pb.serve()

    elif args.action == "gen":
        pass


def test():
    # Initialize logging.
    logging.basicConfig()

    text = """
    This is a test document. Only tags in comments will be parsed.

    {# title = Page Title #}

    {#  name = !@#$%^&* #}

    {# x = AAA BBB CCC + some other 34 stuff #}

    {# y = zum123 + 234 #}

    {# ggg = 3.1 #}

    This should raise a sytax error

    {# abc = 100 #}

    {# stuff = [ 100, 200, Hello World ] #}

    {# value = [ 10, 20, hello world ] #}

    <body>Done!</body>
    """
    lines = text.splitlines()
    meta = parse_lines(lines)

    print (meta)

if __name__ == '__main__':
    run()