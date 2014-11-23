from django import template
from markdown import markdown
import re, logging

logger = logging.getLogger(__name__)

register = template.Library()


@register.filter
def lower(value):
    return value.lower()


@register.simple_tag(takes_context=True)
def link(context, word, text=None):
    start = context['f']
    files = context['files']
    items = filter(lambda x: re.search(word, x.fname, re.IGNORECASE), files)
    if not items:
        f = files[0]
        logger.error("link '%s' does not match" % word)
        return "Link pattern '%s' does not match!" % word
    else:
        f = items[0]
        if len(items) > 1:
            logger.warn("link '%s' matches more than one item: %s" % (word, items))

    rpath = f.relpath(start=start)
    text = text or f.fname
    return '<a href="%s">%s</a>' % (rpath, text)


#
# Based on http://jamie.curle.io/blog/minimal-markdown-template-tag-django/
#
class MarkDownNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        text = self.nodelist.render(context)
        return markdown(text, safe_mode=False, smart_emphasis=True)


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