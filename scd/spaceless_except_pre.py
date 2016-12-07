"""Copyright (c) 2013-2014 Stephan Groß, under MIT license."""
from __future__ import unicode_literals

import re

from django import template
from django.template import Node
from django.utils import six
from django.utils.encoding import force_text
from django.utils.functional import allow_lazy


register = template.Library()


def strip_spaces_between_tags_except_pre(value):
    def replacement(count, matches, match):
        matches.append(match.group(0)[1:-1])  # save the whole match without leading "<" and trailing ">"
        count[0] += 1
        return '<}>'.format(count[0])  # add "<" and ">" to preserve space stripping
    count = [-1]
    matches = []
    value = re.sub(r'<pre(\s.*)?>(.*?)</pre>', lambda match: replacement(count, matches, match), force_text(value), flags=re.S | re.M | re.I)
    value = re.sub(r'>\s+<', '><', force_text(value))
    return value.format(*matches)
strip_spaces_between_tags_except_pre = allow_lazy(strip_spaces_between_tags_except_pre, six.text_type)


class SpacelessExceptPreNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        return strip_spaces_between_tags_except_pre(self.nodelist.render(context).strip())


@register.tag
def spaceless_except_pre(parser, token):
    """Remove whitespace between HTML tags, including tab and newline characters except content between <pre>"""
    nodelist = parser.parse(('endspaceless_except_pre',))
    parser.delete_first_token()
    return SpacelessExceptPreNode(nodelist)
