'''
Really simple static site generator. Uses Django templates.
'''
from __future__ import print_function, unicode_literals, absolute_import, division
import argparse, sys, io, json, re, shutil, os, logging, time, imp, importlib
import bottle, importlib
from string import strip
import django
from django.conf import settings
from django.template import Context, get_templatetags_modules
from django.template.loader import get_template

__author__ = 'ialbert'

VERSION = '3.0.0'
DESCRIPTION = "PyBlue %s, static site generator" % VERSION

logger = logging.getLogger(__name__)


def join(*args):
    # Shorcut to building full paths.
    return os.path.abspath(os.path.join(*args))

class PyBlue(object):
    IGNORE_EXTS = {".pyc"}

    def __init__(self, root, args):

        # Rescan all subdirectories for changes on each request.
        self.auto_refresh = not args.no_scan

        # The name of the context variable.
        self.context = args.context

        # Check timestamps when generating files.
        self.time_check = not args.no_time

        # The folder where the files to serve are located.
        # Do not set these attributes directly, use the set_root() method.
        self.root, self.files = None, []

        # This is a method because it needs refresh the files on each request.
        self.set_root(root)

        # Initialize the django template engine.
        self.django_init()

        # The context module will live under the name ctx.
        ctx_path = join(self.root, self.context)
        try:
            ctx = None
            if os.path.isfile(ctx_path):
                # Attempts to import a python module as a context
                ctx = imp.load_source('ctx', ctx_path)
            else:
                logger.warning("cannot find context module {}".format(ctx_path))
        except Exception as exc:
            logger.warning("unable to import context module: {} error: {}".format(ctx_path, exc))

        def render(path):
            '''
            The rendering handler.
            '''
            if self.auto_refresh:
                self.set_root(self.root)

            logger.info("rendering: %s" % path)
            fname = join(self.root, path)
            page = File(fname=fname, root=self.root)

            if page.is_template:
                params = dict(page=page, root=self.root, context=ctx, files=self.files)
                template = get_template(page.fname)
                context = Context(params)
                return template.render(context)
            else:
                return bottle.static_file(fname, root=self.root)


        # Make a shortcut to the renderer.
        self.render = render

        # The Bottle application will serve the pages.
        self.app = bottle.Bottle()
        self.app.route('/', method=['GET', 'POST', 'PUT', 'DELETE'])(lambda: self.render('index.html'))
        self.app.route('/<path:path>', method=['GET', 'POST', 'PUT', 'DELETE'])(lambda path: self.render(path))

    def serve(self, host='0.0.0.0', port=8080):
        "Launch the WSGI app development web server"
        import waitress
        waitress.serve(self.app, host=host, port=port)

    def walk(self):
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

    def set_root(self, path):
        "Sets the folder where the files to serve are located."
        self.root = os.path.abspath(path)

        if not os.path.isdir(self.root):
            logger.error("directory does not exist: %s" % self.root)
            sys.exit()

        self.files = []
        for dirpath, dirnames, filenames in os.walk(self.root):
            for name in sorted(filenames):
                start, ext = os.path.splitext(name)
                if ext in self.IGNORE_EXTS:
                    continue
                fname = os.path.join(dirpath, name)
                self.files.append(File(fname=fname, root=self.root))

    def django_init(self):
        '''
        Initializes the django engine. The root must have been set already."
        '''

        BASE_APP = []
        try:
            # Attempt to import the root folder. This is necessary to access
            # the local templatetag libraries.
            base = os.path.split(self.root)[-1]
            logger.debug("importing app: %s" % base)
            importlib.import_module(base)
            BASE_APP = [base]
        except ImportError as exc:
            logger.warning("app '{}' cannot be imported.".format(base))

        TEMPLATE_DIR = join(os.path.dirname(__file__), "templates")

        settings.configure(
            DEBUG=True, TEMPLATE_DEBUG=True,
            TEMPLATE_DIRS=[TEMPLATE_DIR, self.root],
            TEMPLATE_LOADERS=(
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ),
            INSTALLED_APPS=["pyblue", "django.contrib.humanize", "django.contrib.staticfiles" ] + BASE_APP,
            TEMPLATE_STRING_IF_INVALID=" ??? ",
            STATIC_URL = '/static/',
        )
        django.setup()



        logger.info("templatetags: %s" % ", ".join(get_templatetags_modules()))


def mtime(fname):
    '''
    Safer file modification time detection.
    '''
    t = os.stat(fname).st_mtime if os.path.isfile(fname) else 0
    return t


class File(object):
    """
    Represents a file object within PyBlue relative to a root directory.
    """

    # Files over this size will not be copied when making the file.
    MAX_SIZE_MB = 50
    TEMPLATE_EXTENSIONS = {".html", ".htm"}
    IMAGE_EXTENSIONS = {".png", ".gif", ".jpg", "jpeg", ".svg"}
    MARKDOWN_EXTENSION = {".md"}

    def __init__(self, fname, root):
        self.root = root
        self.meta = dict()

        # Rewrite the fname to be relative name
        fname = os.path.abspath(fname)
        fname = os.path.relpath(fname, self.root)
        self.fname = fname

        # Full path to the file.
        self.fpath = self.path = os.path.join(root, fname)
        if not os.path.isfile(self.path):
            logger.warning("file does not exist: %s" % fname)
            return

        # File size.
        statinfo = os.stat(self.path)
        self.size = statinfo.st_size

        # Last modification date.
        mt = time.gmtime(statinfo.st_mtime)
        self.last_modified = time.strftime("%A, %B %d, %Y", mt)

        # The directory that contains the file.
        self.dname = os.path.dirname(self.path)

        # File extension.
        self.ext = os.path.splitext(fname)[1]

        # Only templates will be handled through Django.
        self.is_template = self.ext in self.TEMPLATE_EXTENSIONS

        # Images may occasionally get special treatment.
        self.is_image = self.ext in self.IMAGE_EXTENSIONS

        # Is it a markdown document.
        self.is_markdown = self.ext in self.MARKDOWN_EXTENSION

        # Find a more readable name.
        name = title = self.nicer_name(fname)

        # This object stores the metadata.
        self.meta = dict(fname=fname, name=name, title=title, sortkey="5")

        # Parse templates files for metadata.
        if self.is_template:
            meta = parse_metadata(self.path)
            self.meta.update(meta)

    @property
    def content(self):
        MAXSIZE = 1024 * 1024 * 50
        # Don't load large files
        if self.size > MAXSIZE:
            logger.warn("file size is too large to be rendered %s" % self.size)
            return "?"

        return io.open(self.path).read()

    def nicer_name(self, fname):
        """
        Attempts to generate a nicer name from the filename.
        Removes underscores, dashes and extensions.
        """
        head, tail = os.path.split(fname)
        base, ext = os.path.splitext(tail)
        name = base.title().replace("-", " ").replace("_", " ")
        if not self.is_template:
            # Add back extension for non templates.
            name += self.ext
        return name

    def write(self, output, content='', check=True):
        """
        Writes the text into an output folder
        """
        dest = os.path.join(output, self.fname)

        # Sanity check.
        if os.path.abspath(dest) == os.path.abspath(self.path):
            raise Exception("cannot not overwrite the original file: %s" % dest)

        # Only write newer files.
        if check and (mtime(dest) > mtime(self.path)):
            logger.info("destination newer: %s" % dest)
            return

        # Make the directory if needed.
        dpath = os.path.dirname(dest)
        if not os.path.exists(dpath):
            os.makedirs(dpath)

        # Write the destination file
        if self.is_template and content:
            logger.info("saving: %s" % dest)
            with io.open(dest, "wt", encoding='utf-8') as fp:
                fp.write(content)
        else:
            logger.info("copying: %s" % dest)
            shutil.copyfile(self.path, dest)

    def relpath(self, start=None):
        """
        Relative path of this file from a start location
        """
        start = start or self
        rpath = os.path.relpath(self.root, start.dname)
        rpath = os.path.join(rpath, self.fname)
        return rpath

    def __getattr__(self, name):
        """
        Metadata may be accessed as an attributes on the class.
        This gets triggered as a fallback if an attribute is not found.
        """
        value = self.meta.get(name, None)
        return value

    def __repr__(self):
        """
        User friendly representation
        """
        return "%s: %s (%s)" % (self.__class__.__name__, self.name, self.fname)


def parse_metadata(path):
    '''
    Attempts to parse out metadata from django comments.
    Each comment is assumed to be key = value where the value is a JSON object.
    '''
    # Match Django template comments.
    PATTERN = re.compile(r'^{#\s?(?P<name>\w+)\s?=\s?(?P<value>[\S\s]+)\s?#}')

    # Check only the start of the file.
    lines = io.open(path).read().splitlines()[:100]
    lines = map(strip, lines)
    meta = dict()
    for line in lines:
        m = PATTERN.search(line)
        if m:
            name, value = m.group('name'), m.group('value')
            try:
                obj = json.loads(value)
            except ValueError as exc:
                obj = str(value)
            meta[name] = obj

    print (meta)
    return meta


def add_common_arguments(parser):
    '''
    Adds the common parameters to each subparser.
    '''
    parser.add_argument('-r', dest='root', metavar="DIR", default=".", required=True,
                        help='root directory to operate from (%(default)s)')

    parser.add_argument('-c', dest="context", metavar="FILE", type=str, required=False,
                        default="context.py",
                        help='the context (python module) to load (%(default)s)')

    parser.add_argument('--no-scan', dest="no_scan", default=False, action="store_true",
                        help='turn off file scan on each request (%(default)s)')

    parser.add_argument('--no-time', dest="no_time", default=False, action="store_true",
                        help='bypass timestamp check (%(default)s)')

    parser.add_argument('--verbose', dest="verbose", default=False, action="store_true",
                        help='increase message verbosity')


def get_parser():
    '''
    Returns the command line parser.
    '''
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    # Subcommands to the parser.
    subpar = parser.add_subparsers(dest="action",
                                   help=" action: serve, make")

    # The serve subcommand.
    serve = subpar.add_parser('serve',
                              help='serve the web site',
                              epilog="And that's how pyblue serves a directory during development.")

    serve.add_argument('-p', metavar="NUMBER", type=int, default=8080,
                       help='server port to bind to (%(default)s)')

    add_common_arguments(serve)

    # The make subcommand.
    make = subpar.add_parser('make',
                             help='generates the static website',
                             epilog="And that's how pyblue makes static output.")

    make.add_argument('-o', dest="output", metavar="DIR", type=str, required=True,
                      help='the target directory to store the generated site in')

    add_common_arguments(make)

    return parser


def run():
    # Process command line arguments.
    parser = get_parser()

    # Trigger help on plain invocation.
    if len(sys.argv) < 3:
        sys.argv.append("--help")

    # Parse the command line.
    args = parser.parse_args()

    # Logging setup.
    level = logging.DEBUG if args.verbose else logging.WARNING
    format = '%(levelname)s\t%(module)s.%(funcName)s\t%(message)s'
    logging.basicConfig(format=format, level=level)

    pb = PyBlue(root=args.root, args=args)

    if args.action == "serve":
        pb.serve()

    elif args.action == "make":
        pb.make(args.output)

if __name__ == '__main__':
    run()
