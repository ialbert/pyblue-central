__author__ = 'iabert'
import argparse, bottle
from mako import exceptions
import os, os.path, itertools

VERSION = '2.0.0'


def get_parser(cmd):
    parser = argparse.ArgumentParser(description='PyBlue %s, static site generator' % VERSION)

    # Subcommands to the parser.
    subpar = parser.add_subparsers(dest='action')

    # The serve subcommand.
    serve = subpar.add_parser('serve', help='serve the web site')

    serve.add_argument('-p', '--port', type=int, default=8080, help='folder containg files to serve')
    serve.add_argument('-f', '--folder', default=".", help='folder containg files to serve')
    serve.add_argument('-d', '--disable-templates', action='store_true', default=False,
                       help='just serve static files, do not use invoke Mako')
    serve.add_argument('-v', '--verbose', default=False, action="store_true",
                       help='outputs more messages')
    serve.add_argument('-n', '--norefresh', default=False, action="store_true",
                       help='do not refresh files on every request')


    # Print the command line
    print (parser.description)
    args = parser.parse_args(cmd)

    return args

class PyBlue(object):
    TEMPLATE_EXTS = ".html .md .rst".split()
    def __init__(self):
        # The Bottle application that will serve the pages.
        self.app = bottle.Bottle()

        # a set of strings that identifies the extension of the files
        # that should be processed using Mako
        self.template_exts = set(self.TEMPLATE_EXTS)

        # The folder where the files to serve are located.
        # Do not set this attribute directly, use set_folder() instead.
        self.folder = "."

        # The list of all files that can be crawled. Initialized via set_folder().
        self.files = []



def run():
    pass

def test():
    def serve():
        if args.disable_templates:
            self.template_exts = set([])
        self.refresh = not args.norefresh
        self.run(port=args.port)

    parser_serve.set_defaults(func=serve)

if __name__ == '__main__':
    run()