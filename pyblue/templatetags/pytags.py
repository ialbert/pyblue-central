from __future__ import print_function, unicode_literals, absolute_import, division
from builtins import *
from django.utils.text import slugify
from django import template
import logging, re, itertools, os
import CommonMark
from django.utils.safestring import mark_safe
from django.utils import encoding
import bleach

logger = logging.getLogger('pyblue')

register = template.Library()

def get_markdown():
    md = CommonMark.commonmark
    return md

# Allows overriding the markdown parser.
markdown = get_markdown()

@register.inclusion_tag('pyblue_hello.html')
def hello(name='World'):
    '''
    Example of an inclusion tag.
    '''
    return dict(name=name)

class MDEntry(object):
    '''
    Represents a single markdown entry.
    The first non-empty line is considered the title.
    The body will contain an anchor that is the slugified title.
    '''
    def __init__(self, path):
        self.path = path
        self.title = itertools.dropwhile(lambda x: not x.strip(), open(path, 'rU')).next()
        self.title = self.title.lstrip('#')
        self.slug = slugify(self.title)
        self.body = open(path, 'rU').read()
        self.body = "<a name='{}'></a>\n".format(self.slug) + self.body
        self.body = mark_safe(self.body)

    def link(self):
        '''
        Returns a Markdown link to the anchor of the body.
        :return:
        '''
        text = "[{}](#{})".format(self.title, self.slug)
        text = mark_safe(text)
        return text

    def __repr__(self):
        path = os.path.split(self.path)[-1]
        return "MD(p={})".format(path)

@register.simple_tag(takes_context=True)
def markdown_items(context, pattern):
    '''
    Returns a list of Markdown Entries matched by a regular expression pattern.

    :param pattern: The RE pattern
    :return: a list of Markdown Entries
    '''
    files = context['files']
    items = filter(lambda page: re.search(pattern, page.fname, re.IGNORECASE), files)
    items = map(lambda f: MDEntry(f.path), items)
    items = list(items)
    return items

@register.inclusion_tag('pyblue_content.html', takes_context=True)
def markdown_content(context, pattern, toc=True):
    """
    Loops over all markdown files in a pattern
    and includes the markdown files
    """
    page = context['page']
    items = markdown_items(context=context, pattern=pattern)
    params = dict(items=items, pattern=pattern, page=page, toc=toc)
    return params

def match_file(context, pattern):
    """
    Returns a relative path and a name for a matched pattern.
    The path is computed relative to the page object of the current context.

    Returns a triplet of the object, the path and the name to of the object.
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
def read_file(context, pattern):
    """
    Returns the content of a file matched by the pattern.
    Returns an error message if the pattern cannot be found.
    """
    obj, rpath, name = match_file(context=context, pattern=pattern)
    if obj:
        text = open(obj.fpath).read()
    else:
        text = name
    return text


@register.inclusion_tag('pyblue_img.html', takes_context=True)
def img(context, pattern, css=''):
    obj, rpath, name = match_file(context=context, pattern=pattern)
    params = dict(src=rpath, name=name, css=css)
    return params


@register.inclusion_tag('pyblue_thumb.html', takes_context=True)
def thumb(context, pattern, css=''):
    obj, rpath, name = match_file(context=context, pattern=pattern)
    params = dict(src=rpath, name=name, css=css)
    return params


@register.simple_tag(takes_context=True)
def href(context, pattern):
    '''
    Generates a relative path to a pattern.
    '''
    obj, relpath, name = match_file(context=context, pattern=pattern)
    return relpath


@register.inclusion_tag('pyblue_link.html', takes_context=True)
def link(context, pattern, text=None, css=''):
    '''
    Generates a link to a pattern.
    '''
    obj, href, name = match_file(context=context, pattern=pattern)
    # Allows overriding the link display.
    name = text or name
    params = dict(href=href, name=name, css=css)
    return params


@register.inclusion_tag('pyblue_code.html', takes_context=True)
def code(context, pattern, lang="bash", css=''):
    '''
    Formats the content of a file as syntax highlighted code.
    '''
    text = read_file(context=context, pattern=pattern)
    params = dict(lang=lang, text=text, css=css)
    return params


@register.simple_tag(takes_context=True)
def markdown_file(context, pattern, safe=True):
    text = read_file(context=context, pattern=pattern)
    text = encoding.smart_unicode(text)
    html = markdown(text)
    html = mark_safe(html)
    return html


@register.inclusion_tag('pyblue_assets.html', takes_context=True)
def assets(context):
    '''
    A shortcut to site assets. Override template as needed.
    '''
    return dict(context=context)


def top_level_only(attrs, new=False):
    '''
    Helper function used when linkifying with bleach.
    '''
    if not new:
        return attrs
    text = attrs['_text']
    if not text.startswith(('http:', 'https:')):
        return None
    return attrs

# Custom Markdown tag processor.
# Based on http://jamie.curle.io/blog/minimal-markdown-template-tag-django/
#
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

if __name__ == '__main__':
    pass
