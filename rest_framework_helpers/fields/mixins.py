# coding: utf-8
from __future__ import unicode_literals

from ..utils import get_absolute_url


class AbsoluteUrlMixin(object):
    def _to_absolute(self, value):
        if not value:
            return None
        url = None
        if isinstance(value, basestring):
            url = value

        elif hasattr(value, 'url'):
            url = value.url

        if url:
            request = self.context.get('request', None)
            return get_absolute_url(url, request)
        return value

    def to_representation(self, value):
        value = super(AbsoluteUrlMixin, self).to_representation(value)
        return self._to_absolute(value)
