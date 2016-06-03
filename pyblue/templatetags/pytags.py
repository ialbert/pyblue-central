from __future__ import print_function, unicode_literals, absolute_import, division
from django import template
import logging, re
import bleach
import CommonMark
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils import encoding

logger = logging.getLogger('pyblue')

register = template.Library()

def get_markdown():
    md = CommonMark.commonmark
    return md

# Allow overriding the markdown parser.
markdown = get_markdown()


def render_attrs(attrs={}):
    "Renders dictionary attributes as key=value pairs of text."
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
        msg = "Nothing matches pattern: '{}'".format(pattern)
        logger.error(msg)
        return None, relpath, msg

    first = items[0]
    if len(items) > 1:
        # More than one file matches the pattern.
        msg = "{} files match pattern: '{}' in file '{}'".format(len(items), pattern, start.fname)
        logger.error(msg)
        for item in items:
            logger.error("pattern '{}' matches '{}'".format(pattern, item.fname))
    name = first.name
    rpath = first.relpath(start=start)

    return first, rpath, name


@register.simple_tag(takes_context=True)
def find(context, pattern):
    "Returns the content of a file matched by the pattern"
    obj, rpath, name = match_file(context=context, pattern=pattern)
    if obj:
        text = open(obj.fpath).read()
    else:
        text = name
    return text


@register.simple_tag(takes_context=True)
def img(context, pattern, css='', attrs={}):
    obj, relpath, name = match_file(context=context, pattern=pattern)
    extras = render_attrs(attrs)
    html = '<img src="{}" class="{}" alt="{}" {}>'.format(relpath, css, name, extras)
    return mark_safe(html)

@register.inclusion_tag('say_hello.html')
def say_hello():
    return dict()


@register.inclusion_tag('thumbnail.html', takes_context=True)
def thumb(context, pattern, link="#", title="", size=4, clearfix=False):
    obj, relpath, name = match_file(context=context, pattern=pattern)
    obj, rellink, linkname = match_file(context=context, pattern=link)
    title = title or linkname
    params = dict(src=relpath, name=name, link=rellink, title=title, size=size, clearfix=clearfix)
    return params

@register.simple_tag(takes_context=True)
def link(context, pattern, text=None, css='', attrs={}):
    obj, relpath, name = match_file(context=context, pattern=pattern)
    # Allow overriding the link display.
    text = text or name
    extras = render_attrs(attrs)
    html = '<a class="%s" href="%s" %s>%s</a>' % (css, relpath, extras, text)
    return mark_safe(html)


@register.simple_tag(takes_context=True)
def code(context, pattern, lang="bash",  safe=True):
    text = find(context=context, pattern=pattern)
    html = '<pre><code class="language-{}">{}</code></pre>'.format(lang, text)
    if safe:
        html = mark_safe(html)
    return html


@register.simple_tag(takes_context=True)
def include_markdown(context, pattern, safe=True):
    text = find(context=context, pattern=pattern)
    text = encoding.smart_unicode(text)
    html = markdown(text)
    html = mark_safe(html)
    return html


@register.inclusion_tag('site_assets.html', takes_context=True)
def site_assets(context):
    return dict(context=context)


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
