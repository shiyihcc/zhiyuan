# -*- coding: UTF-8 -*-
from django import template
register = template.Library()

@register.filter
def plusplus(text):
    return str(int(text) + 1)
