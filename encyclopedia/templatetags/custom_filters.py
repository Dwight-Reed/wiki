import re

from django import template

register = template.Library()


# talk:title -> Talk: title
def format_title(value):
    title = re.subn(r"talk:", "", value, re.IGNORECASE)
    if title[1]:
        return "Talk: " + title[0]
    return title[0]


register.filter("format_title", format_title)
