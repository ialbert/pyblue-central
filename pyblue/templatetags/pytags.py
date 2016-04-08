from __future__ import print_function, unicode_literals, absolute_import, division
from django import template
#from markdown2 import markdown
import re, logging
from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name, PythonLexer, HtmlLexer, XmlLexer, BashLexer
from pygments.formatters import HtmlFormatter

import bleach

def get_markdown():
    import mistune

    formatter = HtmlFormatter()

    class HighlightRenderer(mistune.Renderer):


        def block_code(self, code, lang='bash'):
            if not lang:
                code = code.strip().strip("\n")
                return '\n<pre><code>%s</code></pre>\n' % \
                    mistune.escape(code)
            lexer = get_lexer_by_name(lang, stripall=True)
            return highlight(code, lexer, formatter)

    renderer = HighlightRenderer()
    md = mistune.Markdown(renderer=renderer)
    return md

markdown = get_markdown()

logger = logging.getLogger(__name__)

register = template.Library()

@register.filter
def lower(value):
    return value.lower()

def render_attrs(attrs={}):
    "Renders a dictionary attributes as key=value pairs in text."
    items = map(lambda item: "%s=%s" % item, attrs.items())
    text = " ".join(items)
    return text

def match_file(context, pattern):
    """
    Returns a relative path and a name for a matched object.
    """
    start = context['page']
    files = context['files']
    items = filter(lambda page: re.search(pattern, page.fname, re.IGNORECASE), files)
    items = list(items)

    if not items:
        # Pattern does not match
        relpath = "#"
        msg = "*** pattern '%s' does not match" % pattern
        logger.error(msg)
        return None, relpath, msg

    first = items[0]
    if len(items) > 1:
        # More than one file matches the pattern.
        msg = "*** pattern '%s' matches more than one item: %s" % (pattern, items)
        logger.error(msg)

    name = first.name
    relpath = first.relpath(start=start)

    return first, relpath, name


@register.simple_tag(takes_context=True)
def img(context, pattern, css='', attrs={}):
    obj, relpath, name = match_file(context=context, pattern=pattern)
    other = render_attrs(attrs)
    html =  '<img src="{}" class="{}" alt="{}" {}>'.format(relpath, css, name, other)
    return html

@register.inclusion_tag('thumbnail.html', takes_context=True)
def thumb(context, pattern, link="#", title="", size=4, clearfix=False):
    obj, relpath, name = match_file(context=context, pattern=pattern)
    obj, rellink, linkname = match_file(context=context, pattern=link)
    title = title or linkname
    params = dict(src=relpath, name=name, link=rellink, title=title, size=size, clearfix=clearfix)
    return params

@register.simple_tag(takes_context=True)
def link(context, pattern, text=None, css='', attrs={}):
    "Returns an html link to the pattern"
    obj, relpath, name = match_file(context=context, pattern=pattern)

    # Allow overriding the link display.
    text = text or name
    other = render_attrs(attrs)
    html = '<a class="%s" href="%s" %s>%s</a>' % (css, relpath, other, text)
    return html

@register.simple_tag(takes_context=True)
def load(context, pattern):
    "Returns the content of a file matched by the pattern"
    obj, relpath, name = match_file(context=context, pattern=pattern)
    if obj:
        text = open(obj.fpath).read()
    else:
        text = name
    return text

HINT2LEXER = dict(
    python=PythonLexer,
    html=HtmlLexer,
    xml=XmlLexer,
    bash=BashLexer,
)

@register.simple_tag(takes_context=True)
def code(context, pattern, hint="bash"):

    text = load(context=context, pattern=pattern)
    lexer = HINT2LEXER.get(hint, PythonLexer)
    html = highlight(text, lexer(), HtmlFormatter())
    return html



@register.simple_tag(takes_context=True)
def include_markdown(context, pattern):
    text = load(context=context, pattern=pattern)
    html = markdown(text)
    return html


@register.simple_tag()
def pygments_css():
    css= """
    <style media="screen" type="text/css">
        %s
    </style>
    """ % HtmlFormatter().get_style_defs('.highlight')
    return css

@register.simple_tag()
def bootstrap_cdn():
    text = """
        <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css" rel="stylesheet">
        <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
    """
    return text

#
# Based on http://jamie.curle.io/blog/minimal-markdown-template-tag-django/
#

def top_level_only(attrs, new=False):

    if not new:
        return attrs

    text = attrs['_text']
    if not text.startswith(('http:', 'https:')):
        return None

    return attrs

class MarkDownNode(template.Node):
    CALLBACKS = [ top_level_only ]
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        text = self.nodelist.render(context)
        text = markdown(text)
        text = bleach.linkify(text, callbacks=self.CALLBACKS, skip_pre=True)
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