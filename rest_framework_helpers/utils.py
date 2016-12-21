# coding: utf-8
from __future__ import unicode_literals

from ._compat import urlparse


from django.conf import settings

SITE_URL = getattr(settings, 'SITE_URL', None)


def get_absolute_url(url, request=None):
    if request:
        return request.build_absolute_uri(url)
    if SITE_URL:
        url = urlparse.urljoin(SITE_URL, url)
    return url
