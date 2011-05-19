# -*- coding: UTF-8 -*-
from django import template
from string import index
register = template.Library()

punc = u".,)!?;: ，。？！）；：\n"

@register.filter
def context(text, kw):
    try:
        length = len(text)
        start = index(text, kw)
        if length < 100:
            return text
        start -= 10
        end = start + 80
        if end >= length:
            end = length - 1
            start = end - 65
        if start < 0:
            start = 0

        while start > 0:
            if text[start - 1] in punc:
                break
            start -= 1

        while end < length:
            if text[end] in punc:
                break
            end += 1

        text = text[start:end]
        if start > 0:
            text = "... " + text
        if end < length - 1:
            text = text + " ..."
        return text

    except:
        return ""
