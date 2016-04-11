from __future__ import print_function, unicode_literals, absolute_import, division
from django import template
import logging
import bleach
import CommonMark


logger = logging.getLogger(__name__)

register = template.Library()

#
# Based on http://jamie.curle.io/blog/minimal-markdown-template-tag-django/
#

@register.simple_tag(takes_context=True)
def link(context, pattern, hint="bash"):
    html = "TODO"
    return html

@register.simple_tag(takes_context=True)
def code(context, pattern, hint="bash"):
    html = "TODO"
    return html

@register.simple_tag(takes_context=True)
def code(context, pattern, hint="bash"):
    html = "TODO"
    return html


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
        text = CommonMark.commonmark(text)
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