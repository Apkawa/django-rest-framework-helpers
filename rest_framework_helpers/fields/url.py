# coding: utf-8
from __future__ import unicode_literals

import urllib

import six
from rest_framework import serializers

from ..utils import get_absolute_url
from .mixins import AbsoluteUrlMixin


class AbsoluteURLField(AbsoluteUrlMixin, serializers.URLField):
    pass


class AbsoluteViewField(serializers.HyperlinkedRelatedField):
    def __init__(self, *args, **kwargs):
        self.view_kwargs = kwargs.pop('view_kwargs', {})
        self.view_params = kwargs.pop('view_params', None)

        kwargs['read_only'] = True
        kwargs['source'] = '*'
        super(AbsoluteViewField, self).__init__(*args, **kwargs)

    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        # Unsaved objects will not yet have a valid URL.
        view_params = self.view_params
        view_kwargs = {k: v.format(obj=obj) for k, v in self.view_kwargs.items()}

        url = self.reverse(view_name, kwargs=view_kwargs, request=request, format=format)

        if isinstance(view_params, dict):
            view_params = {k: v.format(obj=obj) for k, v in self.view_params.items()}
            view_params = urllib.urlencode(view_params)
        elif isinstance(view_params, six.string_types):
            view_params = view_params.format(obj=obj)
        if view_params:
            url += '?' + view_params

        return get_absolute_url(url)
