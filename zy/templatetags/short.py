# -*- coding: UTF-8 -*-
from django import template
register = template.Library()

@register.filter
def short(text, length):
    if len(text) > length:
        text = text[:length]
        text += '......'
    else:
        text = text[:length]
    return text
