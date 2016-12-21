# coding: utf-8
from __future__ import unicode_literals

from rest_framework import serializers


class MethodWritableField(serializers.SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs['source'] = '*'
        kwargs['read_only'] = False
        serializers.Field.__init__(self, **kwargs)


class ChoiceField(serializers.ChoiceField):
    @property
    def options(self):
        return self.iter_options()
