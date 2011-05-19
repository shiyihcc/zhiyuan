# -*- coding: UTF-8 -*-

from django.core.exceptions import ValidationError

def validate_mobileno(text):
    if (str(int(text)) != text) or (len(text) != 11) or (text[0] not in ('9', '1')):
        raise ValidationError(u'请输入一个有效的手机号码。')
