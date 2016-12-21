# coding: utf-8
from __future__ import unicode_literals

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO



try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse