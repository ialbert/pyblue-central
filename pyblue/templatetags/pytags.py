from __future__ import print_function, unicode_literals, absolute_import, division
from django import template
from markdown2 import markdown
import re, logging
from pygments import highlight
from pygments.lexers import guess_lexer, PythonLexer
from pygments.formatters import HtmlFormatter
# import bleach

logger = logging.getLogger(__name__)

register = template.Library()

@register.filter
def lower(value):
    return value.lower()


@register.simple_tag(takes_context=True)
def link(context, word, text=None):
    start = context['page']
    files = context['files']
    items = filter(lambda x: re.search(word, x.fname, re.IGNORECASE), files)
    items = list(items)
    if not items:
        f = files[0]
        logger.error("link '%s' does not match" % word)
        rpath, text = "#", "Link pattern '%s' does not match!" % word
    else:
        f = items[0]
        if len(items) > 1:
            logger.warn("link '%s' matches more than one item: %s" % (word, items))
        rpath = f.relpath(start=start)
    text = text or f.title
    return '<a href="%s">%s</a>' % (rpath, text)

@register.simple_tag(takes_context=True)
def load(context, word):
    files = context['files']
    items = filter(lambda x: re.search(word, x.fname, re.IGNORECASE), files)
    items = list(items)
    if not items:
        logger.error("pattern '%s' does not match" % word)
        text = "include pattern '%s' does not match!" % word
    else:
        f = items[0]
        if len(items) > 1:
            logger.warn("link '%s' matches more than one item: %s" % (word, items))
        text = open(f.fpath).read()
    return text

@register.simple_tag(takes_context=True)
def code(context, word):
    text = load(context=context, word=word)
    try:
        lexer = guess_lexer(text)
    except Exception as exc:
        lexer = PythonLexer()
    html = highlight(text, lexer, HtmlFormatter())
    return html


@register.simple_tag()
def pygments_css():
    css= """
    <style media="screen" type="text/css">
        %s
    </style>
    """ % HtmlFormatter().get_style_defs('.highlight')
    return css

#
# Based on http://jamie.curle.io/blog/minimal-markdown-template-tag-django/
#
class MarkDownNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        text = self.nodelist.render(context)
        text = markdown(text, safe_mode=False, extras=["code-friendly", "tables"])
        #text = bleach.linkify(text, skip_pre=True)
        return text

@register.tag('markdown')
def markdown_tag(parser, token):
    """
    Enables a block of markdown text to be used in a template.

    Syntax::

            {% markdown %}
            ## Markdown

            Now you can write markdown in your templates. This is good because:

            * markdown is awesome
            * markdown is less verbose than writing html by hand

            {% endmarkdown %}
    """
    nodelist = parser.parse(('endmarkdown',))
    # need to do this otherwise we get big fail
    parser.delete_first_token()
    return MarkDownNode(nodelist)