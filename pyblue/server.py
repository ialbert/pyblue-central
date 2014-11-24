__author__ = 'ialbert'
import argparse, bottle, waitress, logging
import sys, os, os.path, itertools, imp

from pyblue import VERSION, PYBLUE_DIR
DESCR = "PyBlue %s, static site generator" % VERSION
from django.conf import settings
from django.template import Context, Template
from django.template.loader import get_template
from .utils import File
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


if __name__ == '__main__':
    run()