#
# This library demonstrates the use of custom demo tags
#
from django import template

register = template.Library()

@register.simple_tag()
def page_title(text):
    html = "<h2>%s</h2>" % text
    return html