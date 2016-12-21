
# -*- coding: utf-8 -*-

from __future__ import absolute_import  # Python 2 only
from __future__ import unicode_literals

from jinja2 import Environment


EXTENSIONS = [
    "jinja2.ext.do",
    "jinja2.ext.loopcontrols",
    "jinja2.ext.with_",
    "jinja2.ext.i18n",
    "jinja2.ext.autoescape",
    "django_jinja.builtins.extensions.CsrfExtension",
    "django_jinja.builtins.extensions.CacheExtension",
    "django_jinja.builtins.extensions.TimezoneExtension",
    "django_jinja.builtins.extensions.UrlsExtension",
    "django_jinja.builtins.extensions.StaticFilesExtension",
    "django_jinja.builtins.extensions.DjangoFiltersExtension",
]


def environment(**options):
    options['extensions'] = EXTENSIONS
    env = Environment(**options)
    env.globals.update(FUNCTIONS)
    env.filters.update(FILTERS)

    return env
