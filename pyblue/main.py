#! /usr/bin/python

from __future__ import unicode_literals, print_function

import bottle
from mako.lookup import TemplateLookup
from mako import exceptions
import os, os.path, itertools
import wsgiref.handlers
import sys, logging, re, os, time
import argparse, waitress
import utils

# setting up logging
_logger = logging.getLogger(__name__)

op = os.path
dn = op.dirname

class File(object):
    "Represents a file object within PyBlue"

    def __init__(self, fname, root):
        self.root  = root
        self.fname = fname
        self.fpath = os.path.join(root, fname)
        self.dname = dn(self.fpath)
        self.ext   = os.path.splitext(fname)[1]

        self.meta  =  dict(name=self.nice_name, sortkey="5", tags=set("data"), doctype="markdown")

        # large files should not be parsed
        if not self.skip_file:
            self.meta.update(utils.parse_meta(self.fpath))

    @property
    def nice_name(self):
        "Attempts to generate a nicer name from the filename"
        head, tail = os.path.split(self.fname)
        base, ext = os.path.splitext(tail)
        name = base.title().replace("-", " ").replace("_", " ")
        if self.is_image:
            # add back extensions for images
            name = name + self.ext
        return name

    @property
    def is_image(self):
        return self.ext in (".png", ".jpg", ".gif")

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

    @property
    def get_content(self):
        return file(self.fpath).read()

    @property
    def size(self):
        "File size in KB"
        return utils.get_size(self.fpath)

    @property
    def skip_file(self):
        return self.size > utils.MAX_SIZE_MB

    def write(self, output_folder, text):
        loc = os.path.join(output_folder, self.fname)

        if op.abspath(loc) == op.abspath(self.fpath):
            raise Exception("may not overwrite the original file %s" % loc)

        d = os.path.dirname(loc)
        if not os.path.exists(d):
            os.makedirs(d)
        with open(loc, "wb") as fp:
            fp.write(text)

    def url(self, start=None, text=''):
        "Relative path of the file to the start folder"
        start = start or self
        rpath = op.relpath(self.root, start.dname)
        rpath = op.join(rpath, self.fname)

        return rpath, text or self.name

    def __repr__(self):
        return "File: %s (%s)" % (self.name, self.fname)

class PyBlue:
    TEMPLATE_DIR = op.abspath(op.join(op.split(__file__)[0], "templates"))

    def __init__(self):

        # the Bottle application
        self.app = bottle.Bottle()
        # a set of strings that identifies the extension of the files
        # that should be processed using Mako
        self.template_exts = set([".html"])

        # the folder where the files to serve are located. Do not set
        # directly, use set_folder() instead
        self.folder = "."

        # the list of all crawled files, initialized in set_folder()
        self.files = []

        # should it recrawl directories on each request, used in serving
        # can be turned off in the options
        self.refresh = False

        # the TemplateLookup of Mako
        self.templates = TemplateLookup(directories=[self.folder, self.TEMPLATE_DIR],
                                        imports=[ "from pyblue.utils import markdown", "from pyblue.utils import rst, asc"],
                                        input_encoding='iso-8859-1',
                                        collection_size=100,
        )
        # A list of regular expression. Files whose the name match
        # one of those regular expressions will not be outputed when generating
        # a static version of the web site
        self.file_exclusion = [r".*\.mako", r".*\.py", r"(^|.*\/)\..*"]

        def is_public(path):
            for ex in self.file_exclusion:
                if re.match(ex, path):
                    return False
            return True

        def base_lister():
            files = []
            for dirpath, dirnames, filenames in os.walk(self.folder):
                filenames.sort()
                for f in filenames:
                    absp = os.path.join(dirpath, f)
                    path = os.path.relpath(absp, self.folder)
                    files.append(path)

            files = filter(is_public, files)

            return files

            # A list of function. Each function must return a list of paths

        # of files to export during the generation of the static web site.
        # The default one simply returns all the files contained in the folder.
        # It is necessary to define new listers when new routes are defined
        # in the Bottle application, or the static site generation routine
        # will not be able to detect the files to export.
        self.file_listers = [base_lister]

        def file_renderer(path):
            if is_public(path):
                _, ext = os.path.splitext(path)
                if ext in self.template_exts and self.templates.has_template(path):
                    f = File(fname=path, root=self.folder)
                    t = self.templates.get_template(path)
                    if self.refresh:
                        self.files = self.collect_files()
                    try:
                        data = t.render_unicode(p=self, f=f, u=utils)

                        # if it made it this far the user wants these to be rendered as html
                        if ext == '.md':
                            data = utils.markdown(data)
                        elif ext == '.rst':
                            data = utils.rst(data)

                        page = data.encode(t.module._source_encoding)
                        return page
                    except Exception, exc:
                        _logger.error("error %s generating page %s" % (exc, path))
                        return exceptions.html_error_template().render()

                return bottle.static_file(path, root=self.folder)
            return bottle.HTTPError(404, 'File does not exist.')

            # The default function used to render files. Could be modified to change the way files are

        # generated, like using another template language or transforming css...
        self.file_renderer = file_renderer
        self.app.route('/', method=['GET', 'POST', 'PUT', 'DELETE'])(lambda: self.file_renderer('index.html'))
        self.app.route('/<path:path>', method=['GET', 'POST', 'PUT', 'DELETE'])(lambda path: self.file_renderer(path))

    def set_folder(self, folder):
        """
        Sets the folder where the files to serve are located.
        """
        self.folder = folder
        self.templates.directories[0] = folder
        if self.folder not in sys.path:
            sys.path.append(self.folder)

        # append more ignored patterns
        ignore_file = op.join(self.folder, ".ignore")
        _logger.info("checking optional ignore file %s" % ignore_file)
        self.file_exclusion.extend(utils.parse_opt_file(ignore_file))
        _logger.info("excluded files: %s" % self.file_exclusion)

        # add more of the included extensions
        include_file = op.join(self.folder, ".include")
        _logger.info("checking optional include files %s" % include_file)
        self.template_exts.update(utils.parse_opt_file(include_file))
        _logger.info("template extensions: %s" % self.template_exts)

        # collect the files
        self.files = self.collect_files()

    def run(self, host='0.0.0.0', port=8080):
        """
        Launch a development web server.
        """
        waitress.serve(self, host=host, port=port)

    def get(self, f):
        """
        Get the content of a file, indentified by its path relative to the folder configured
        in PyGreen. If the file extension is one of the extensions that should be processed
        through Mako, it will be processed.
        """
        handler = wsgiref.handlers.SimpleHandler(sys.stdin, sys.stdout, sys.stderr, {})
        handler.setup_environ()
        env = handler.environ
        env.update({'PATH_INFO': "/%s" % f.fname, 'REQUEST_METHOD': "GET"})
        out = b"".join(self.app(env, lambda *args: None))
        return out

    @property
    def settings(self):
        m = __import__('settings', globals(), locals(), [], -1)
        return m

    def link(self, start, name, text=''):

        items = filter(lambda x: re.search(name, x.fname, re.IGNORECASE), self.files)
        if not items:
            f = self.files[0]
            _logger.error("link name '%s' in %s does not match" % (name, start.fname))
            return ("#", "Link pattern '%s' does not match!" % name)
        else:
            f = items[0]
            if len(items) > 1:
                _logger.warn("link name '%s' in %s matches more than one item %s" % (name, start.fname, items))

        link, value = f.url(start, text=text)

        return (link, value)

    def toc(self, start,  tag=None, match=None, is_image=False):
        "Produces name, links pairs from file names"

        if tag:
            items = filter(lambda x: tag in x.meta['tags'], self.files)
        else:
            items = self.files

        if match:
            items = filter(lambda x: re.search(match, x.fname, re.IGNORECASE), self.files)

        if is_image:
            items = filter(lambda x: x.is_image, items)

        if not items:
            _logger.error("tag %s does not match" % tag)

        urls = [f.url(start) for f in items]
        return urls

    def collect_files(self):
        """
        Collects all files that will be parsed. Will also be available in main context.
        TODO: this method crawls the entire directory tree each time it is accessed.
        It is handy during development but very large trees may affect performance.
        """
        files = []
        for l in self.file_listers:
            files += l()

        files = map(lambda x: File(x, self.folder), files)
        _logger.info("collected %s files" % len(files))

        # apply sort order
        decor = [(f.sortkey, f.name, f) for f in files]
        decor.sort()
        return [ f[2] for f in decor ]

    def gen_static(self, output_folder):
        """
        Generates a complete static version of the web site. It will stored in 
        output_folder.
        """

        # this makes all files available in the template context

        for f in self.files:
            if f.skip_file:
                _logger.info("skipping large file %s of %.1fkb" % (f.fname, f.size))
                continue
            _logger.info("generating %s" % f.fname)
            content = self.get(f)
            f.write(output_folder, content)

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

    def cli(self, cmd_args=None):
        """
        The command line interface of PyGreen.
        """
        import pyblue

        parser = argparse.ArgumentParser(description='PyBlue %s, static site generator' % pyblue.VERSION)

        subparsers = parser.add_subparsers(dest='action')

        parser_serve = subparsers.add_parser('serve', help='serve the web site')
        parser_serve.add_argument('-p', '--port', type=int, default=8080, help='folder containg files to serve')
        parser_serve.add_argument('-f', '--folder', default=".", help='folder containg files to serve')
        parser_serve.add_argument('-d', '--disable-templates', action='store_true', default=False,
                                  help='just serve static files, do not use invoke Mako')
        parser_serve.add_argument('-v', '--verbose', default=False, action="store_true", help='outputs more messages')
        parser_serve.add_argument('-n', '--norefresh', default=False, action="store_true", help='do not refresh files on every request')

        def serve():
            if args.disable_templates:
                self.template_exts = set([])
            self.refresh = not args.norefresh
            self.run(port=args.port)

        parser_serve.set_defaults(func=serve)

        parser_gen = subparsers.add_parser('gen', help='generate a static version of the site')
        parser_gen.add_argument('output', help='folder to store the files')
        parser_gen.add_argument('-f', '--folder', default=".", help='folder containg files to serve')
        parser_gen.add_argument('-v', '--verbose', default=False, action="store_true", help='outputs more messages')

        def gen():
            self.gen_static(args.output)

        def set_log_level(level):
            logging.basicConfig(level=level, format='%(levelname)s\t%(module)s.%(funcName)s\t%(message)s')


        parser_gen.set_defaults(func=gen)

        print(parser.description)
        args = parser.parse_args(cmd_args)

        level = logging.DEBUG if args.verbose else logging.WARNING
        set_log_level(level)

        _logger.info("starting pyblue")
        self.set_folder(args.folder)

        args.func()


server = PyBlue()

if __name__ == "__main__":
    server.cli()
