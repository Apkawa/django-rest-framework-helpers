# coding: utf-8
from __future__ import unicode_literals

from collections import OrderedDict

import six
from django.db.models import Model
from rest_framework import serializers


class SerializableRelationField(serializers.RelatedField):
    def __init__(self, serializer, serializer_function=None, *args, **kwargs):
        super(SerializableRelationField, self).__init__(*args, **kwargs)
        self.serializer = serializer
        self.serializer_function = serializer_function or self.do_serialize

    def to_representation(self, value):
        if isinstance(value, Model):
            return self.serializer_function(value, self.serializer)
        return value

    def to_internal_value(self, data):
        return self.serializer.Meta.model.objects.get(id=data)

    def do_serialize(self, obj, serializer=None):
        if not serializer:
            return obj.pk
        return serializer(obj).data

    @property
    def choices(self):
        queryset = self.get_queryset()
        if queryset is None:
            # Ensure that field.choices returns something sensible
            # even when accessed with a read-only field.
            return {}

        return OrderedDict([
            (
                six.text_type(item.pk),
                self.display_value(item)
            )
            for item in queryset
            ])
