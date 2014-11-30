# Python 2/3 ready.
from __future__ import print_function, unicode_literals, absolute_import, division

__author__ = 'ialbert'

import django
from django.conf import settings
from django.template import Context, Template, get_templatetags_modules
from django.template.loader import get_template
import bottle, waitress, importlib
import sys, os, io, imp, argparse, logging, re, time, shutil

from pyblue import VERSION

DESCRIPTION = "PyBlue %s, static site generator" % VERSION

logger = logging.getLogger(__name__)


def join(*args):
    # Shorcut to building full paths.
    return os.path.abspath(os.path.join(*args))


def strip(text):
    # Why was this removed from Python 3?
    return text.strip()


def mtime(fname):
    # File modification time.
    t = os.stat(fname).st_mtime if os.path.isfile(fname) else 0
    return t


TEMPLATE_DIR = join(os.path.dirname(__file__), "templates")


def get_parser():
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    # Subcommands to the parser.
    subpar = parser.add_subparsers(dest="action",
                                   help=" action: serve, deploy")

    # The serve subcommand.
    serve = subpar.add_parser('serve',
                              help='serve the web site',
                              epilog="And that's how pyblue serves a directory during development.")

    serve.add_argument('-r', dest='root', metavar="DIR", default=".", required=True,
                       help='root directory to serve from (%(default)s)')

    serve.add_argument('-p', metavar="NUMBER", type=int, default=8080,
                       help='server port to bind to (%(default)s)')

    serve.add_argument('-v', dest="verbose", default=False, action="store_true",
                       help='increase message verbosity')

    serve.add_argument('--no-scan', dest="no_scan", default=False, action="store_true",
                       help='turn off file scan on each request (%(default)s)')

    serve.add_argument('--no-time', dest="no_time", default=False, action="store_true",
                       help='bypass timestamp check (%(default)s)')

    serve.add_argument('--context', dest="context", metavar="FILE", type=str, required=False,
                       default="context.py", help='the python module to load as context (%(default)s)')

    # The make subcommand.
    make = subpar.add_parser('make',
                             help='generates the static website',
                             epilog="And that's how pyblue makes static output.")

    make.add_argument('-r', dest='root', metavar="DIR", default=".", required=True,
                      help='root directory to process (%(default)s)')

    make.add_argument('-o', dest="output", metavar="DIR", type=str, required=True,
                      help='the target directory to store the generated site in')

    make.add_argument('-v', dest="verbose", default=False, action="store_true",
                      help='increase message verbosity')

    make.add_argument('--no-scan', dest="no_scan", default=False, action="store_true",
                      help='turn off file scan on each request (%(default)s)')

    make.add_argument('--no-time', dest="no_time", default=False, action="store_true",
                      help='bypass timestamp check (%(default)s)')

    make.add_argument('--context', dest="context", metavar="FILE", type=str, required=False,
                      default="context.py", help='the python module to load as context (%(default)s)')

    return parser


class File(object):
    """
    Represents a file object within PyBlue.
    Each file object is visible in the template context.
    """
    MAX_SIZE_MB = 5
    IMAGE_EXTENSIONS = set(".png .jpg .gif .svg".split())
    TEMPLATE_EXTENSIONS = set(".html .htm .md".split())

    def __init__(self, fname, root):
        self.root = root
        self.fname = fname

        # Full path to the file.
        self.fpath = os.path.join(root, fname)
        self.is_template = False

        if not os.path.isfile(self.fpath):
            logger.warning("file does not exist: %s" % fname)
            return

        # File size.
        statinfo = os.stat(self.fpath)
        self.size = statinfo.st_size

        # Last modification date.
        mt = time.gmtime(statinfo.st_mtime)
        self.last_modified = time.strftime("%A, %B %d, %Y", mt)

        # Directory that contains the file.
        self.dname = os.path.dirname(self.fpath)

        # File extension.
        self.ext = os.path.splitext(fname)[1]

        # Used when rendering galleries and building names.
        self.is_image = self.ext in self.IMAGE_EXTENSIONS

        # Only templates will be handled through Django.
        self.is_template = self.ext in self.TEMPLATE_EXTENSIONS

        # Is it a markdown document.
        self.is_markdown = (self.ext == ".md")

        # The nice name is used by default for name and title.
        name = self.nicer_name(fname)

        # This object stores the metadata.
        self.meta = dict(fname=fname, name=name, title=name, sortkey="5")

        # Parse templates files only for metadata.
        if self.is_template:
            try:
                lines = io.open(self.fpath).read().splitlines()[:20]
                self.meta.update(parse_lines(lines))
            except Exception as exc:
                logger.error(exc)
    @property
    def content(self):
        # Don't load large files
        if self.size > 1024 * 1024 * 5:
            logger.warn("file size is too large to be rendered %s" % self.size)
            return "?"

        return io.open(self.fpath).read()

    def nicer_name(self, fname):
        """
        Attempts to generate a nicer name from the filename
        """
        head, tail = os.path.split(fname)
        base, ext = os.path.splitext(tail)
        name = base.title().replace("-", " ").replace("_", " ")
        if self.is_image:
            # Add back extensions for images.
            name += self.ext
        return name

    def write(self, output, content='', check=True):
        """
        Writes the text into an output folder
        """
        dest = os.path.join(output, self.fname)

        # Sanity check.
        if os.path.abspath(dest) == os.path.abspath(self.fpath):
            raise Exception("may not overwrite the original file: %s" % dest)

        # Only write newer files.
        if check and (mtime(dest) > mtime(self.fpath)):
            logger.info("pass: %s" % dest)
            return

        # Make the directory if needed.
        dpath = os.path.dirname(dest)
        if not os.path.exists(dpath):
            os.makedirs(dpath)

        if self.is_template and content:
            logger.info("save: %s" % dest)
            with io.open(dest, "wt") as fp:
                fp.write(content)
        else:
            logger.info("copy: %s" % dest)
            shutil.copyfile(self.fpath, dest)


    def relpath(self, start=None):
        """
        Relative path of this file from the start location
        """
        start = start or self
        rpath = os.path.relpath(self.root, start.dname)
        rpath = os.path.join(rpath, self.fname)
        return rpath


    def __getattr__(self, name):
        """
        Metadata will be exposed as attributes on the class.
        """
        value = self.meta.get(name, None)
        if not value:
            logger.error(self.meta)
            logger.error(" *** attribute '%s' for '%s' not found" % (name, self.fname))
            value = '?'
        return value

    def __repr__(self):
        """
        User friendly representation
        """
        return "%s: %s (%s)" % (self.__class__.__name__, self.name, self.fname)


# Conversion regular expressions.
int_patt = re.compile("\d+")
flt_patt = re.compile("\d+\.\d+")
lst_patt = re.compile("\[(?P<body>[\S\s]+?)\]")


def convert_text(text):
    """
    Converts text to an appropriate python datatype: int, float or list.
    """
    global int_patt, flt_patt, lst_patt
    text = text.strip()
    try:
        if flt_patt.match(text):
            return float(text)

        if int_patt.match(text):
            return int(text)

        m = lst_patt.search(text)
        if m:
            vals = m.group('body').split(",")
            vals = map(convert_text, vals)
            return list(vals)
    except Exception as exc:
        logger.error("conversion error of %s -> %s " % (text, exc))
        return text
    return text

# Match Django template comments.
com_patt = re.compile(r'^{# (?P<name>\w+)\s?=\s?(?P<value>[\S\s]+) #}')


def parse_lines(lines):
    "Attempts to parse out metadata from django comments"
    global com_patt
    meta = dict()
    lines = map(strip, lines)
    for line in lines:
        m = com_patt.search(line)
        if m:
            name, value = m.group('name'), m.group('value')
            meta[name] = convert_text(value)
    return meta


class PyBlue(object):
    IGNORE_EXTS = ".pyc"

    def django_init(self, context="context.py"):
        "Initializes the django engine. The root must have been set already!"

        BASE_APP = [ ]
        try:
            # checks if the root is importable
            base = os.path.split(self.root)[-1]
            importlib.import_module(base)
            logger.info("imported %s" % base)
            BASE_APP = [ base ]
        except Exception as exc:
            logger.info("%s" % exc)

        settings.configure(
            DEBUG=True, TEMPLATE_DEBUG=True,
            TEMPLATE_DIRS=(self.root, TEMPLATE_DIR),
            TEMPLATE_LOADERS=(
                'django.template.loaders.filesystem.Loader',

            ),
            INSTALLED_APPS=["pyblue", "django.contrib.humanize"] + BASE_APP,
            TEMPLATE_STRING_IF_INVALID = " ??? ",
        )

        django.setup()

        logger.info("templatetag modules: %s" % ", ".join(get_templatetags_modules()))


    def __init__(self, root, args):

        # Rescan all subdirectories for changes on each request.
        self.auto_refresh = not args.no_scan

        # The name of the context variable.
        self.context = args.context

        # Check timestamps when generating files.
        self.time_check = not args.no_time

        # A set of strings that identifies the extension of the files
        # that should be processed using the Django templates.
        self.ignore_exts = set(self.IGNORE_EXTS.split())

        # The folder where the files to serve are located.
        # Do not set this attribute directly, use set_root() method instead.
        self.root, self.files = None, []

        # This is a method because it needs refresh the files on each request.
        self.set_root(root)

        # Initialize the django template engine.
        self.django_init()

        try:
            # Attempts to import a python module as a context
            ctx = imp.load_source('ctx', join(self.root, self.context))
        except Exception as exc:
            ctx = None
            logger.warning("unable to import context module: %s" % self.context)

        def render(path):

            # This needs to rerun to pick up
            # new files that migh have been added in the meantime.
            # On the other hand might slow down large sites.
            if self.auto_refresh:
                self.set_root(self.root)

            logger.info("render: %s" % path)
            page = File(fname=path, root=self.root)

            if page.is_template:
                params = dict(page=page, root=self.root, context=ctx, files=self.files)
                if page.is_markdown:
                    templ_name = "markdown-base.html"
                else:
                    templ_name = page.fname

                templ = get_template(templ_name)
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

        if not os.path.isdir(self.root):
            logger.error("directory does not exist: %s" % self.root)
            sys.exit()

        # Reads all files in the root.
        self.files = [File(fname=path, root=self.root) for path in self.collect()]

    def collect(self):
        files = []
        for dirpath, dirnames, filenames in os.walk(self.root):
            for name in sorted(filenames):
                start, ext = os.path.splitext(name)
                if ext in self.ignore_exts:
                    continue
                absp = os.path.join(dirpath, name)
                path = os.path.relpath(absp, self.root)
                files.append(path)
        logger.info("found: %d files" % len(files))
        return files


    def serve(self, host='0.0.0.0', port=8080):
        "Launch the WSGI app development web server"
        waitress.serve(self.app, host=host, port=port)

    def generate(self, output):
        """
        Generates a complete static version of the web site.
        """
        self.auto_refresh = False
        for f in self.files:
            if f.is_template:
                content = self.render(f.fname)
                f.write(output, content=content, check=self.time_check)
            else:
                f.write(output, check=self.time_check)


def run():
    # Process command line arguments.
    parser = get_parser()

    # Trigger help on plain invocation.
    if len(sys.argv) < 3:
        sys.argv.append("--help")

    # Parse the command line.
    args = parser.parse_args(sys.argv[1:])

    # Loggins setup.
    level = level = logging.DEBUG if args.verbose else logging.WARNING
    format = '%(levelname)s\t%(module)s.%(funcName)s\t%(message)s'
    logging.basicConfig(format=format, level=level)

    pb = PyBlue(root=args.root, args=args)
    if args.action == "serve":
        pb.serve()

    elif args.action == "make":
        pb.generate(args.output)


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

    print(meta)


if __name__ == '__main__':
    run()