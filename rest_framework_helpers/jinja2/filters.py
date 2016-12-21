# coding: utf-8
from __future__ import unicode_literals

from dateutil.parser import parse as datetime_parse
from django.conf import settings
from django.utils.encoding import smart_str

from django_jinja.builtins.filters import date as _date


def date(value, _format='DATE_FORMAT'):
    if hasattr(settings, smart_str(_format)):
        _format = getattr(settings, smart_str(_format), None)

    if isinstance(value, basestring):
        value = datetime_parse(value)

    return _date(value, _format)


def int_format(value, decimal_points=3, seperator=u' '):
    value = str(value)
    if len(value) <= decimal_points:
        return value
    # say here we have value = '12345' and the default params above
    parts = []
    while value:
        parts.append(value[-decimal_points:])
        value = value[:-decimal_points]
    # now we should have parts = ['345', '12']
    parts.reverse()
    # and the return value should be u'12.345'
    return seperator.join(parts)
