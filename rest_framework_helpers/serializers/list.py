# coding: utf-8
from __future__ import unicode_literals

import itertools
from rest_framework import serializers


class ColumnListSerializer(serializers.ListSerializer):
    column = 3

    def to_representation(self, data):
        object_list = super(ColumnListSerializer, self).to_representation(data)
        result = [list() for i in xrange(self.column)]
        for col, obj in itertools.izip(itertools.cycle(range(self.column)), object_list):
            result[col].append(obj)
        return result


def ColumnListSerializerClassFactory(column=3):
    return type(b'ColumnListSerializer', (ColumnListSerializer,), {'column': column})
