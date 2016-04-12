"""
This library demonstrates the use of custom demo tags
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import logging
from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)

register = template.Library()

@register.simple_tag()
def boom(text):
    html = "BOOM! BOOM! POW! <b>{}</b>!".format(text)
    return mark_safe(html)
