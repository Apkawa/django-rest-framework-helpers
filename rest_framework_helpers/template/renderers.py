# coding: utf-8
from __future__ import unicode_literals

import warnings
from django import forms

JINJA2_TEMPLATE_CLASSES = tuple()
try:
    from django.template.backends import jinja2

    JINJA2_TEMPLATE_CLASSES += (jinja2.Template,)
    try:
        from django_jinja.backend import Template as JinjaTemplate

        JINJA2_TEMPLATE_CLASSES += (JinjaTemplate,)
    except ImportError:
        pass
except ImportError:
    warnings.warn("Need jinja2 package", ImportWarning)

import django_filters

from django.utils.encoding import smart_str

from rest_framework import serializers
from rest_framework.renderers import TemplateHTMLRenderer as _TemplateHTMLRenderer, JSONRenderer
from rest_framework.utils.encoders import JSONEncoder


class TemplateHTMLRenderer(_TemplateHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders data to HTML, using Django's standard template rendering.

        The template name is determined by (in order of preference):

        1. An explicit .template_name set on the response.
        2. An explicit .template_name set on this class.
        3. The return result of calling view.get_template_names().
        """
        renderer_context = renderer_context or {}
        view = renderer_context['view']
        request = renderer_context['request']
        response = renderer_context['response']

        if response.exception:
            template = self.get_exception_template(response)
        else:
            template_names = self.get_template_names(response, view)
            template = self.resolve_template(template_names)

        context = self.resolve_context(data, request, response)
        if isinstance(template, JINJA2_TEMPLATE_CLASSES):
            return template.render(context, request=request)
        return template.render(context)

    def resolve_context(self, data, request, response):
        if response.exception:
            data['status_code'] = response.status_code
        return data


class TemplateContextJsonEncoder(JSONEncoder):
    def encode_serializer(self, serializer):
        """
        :param serializer:
        :return:
        """
        serializer_data = {}
        for field in serializer:
            attrs = ['label', 'name', 'value', 'errors']
            field_data = {a: getattr(field, a) for a in attrs}
            if hasattr(field, 'options'):
                options_data = []
                for select in field.options:
                    s_attrs = ['start_option_group', 'end_option_group', 'label', 'disabled', 'display_text']
                    options_data.append({a: getattr(select, a, None) for a in s_attrs})
                field_data['options'] = options_data

            serializer_data[field.name] = field_data

        return serializer_data

    def encode_form(self, form):
        try:
            from django_remote_forms.forms import RemoteForm
            return RemoteForm(form).as_dict()
        except ImportError:
            pass
        return repr(form)

    def encode_filter(self, filter_instance):
        return {'form': self.encode_form(filter_instance.form)}

    def default(self, obj):
        if isinstance(obj, forms.BaseForm):
            return repr(obj)

        if isinstance(obj, django_filters.FilterSet):
            return self.encode_filter(obj)

        if isinstance(obj, serializers.BaseSerializer):
            return self.encode_serializer(obj)
        return super(TemplateContextJsonEncoder, self).default(obj)

    def iterencode(self, o, _one_shot=False):
        chunks = super(TemplateContextJsonEncoder, self).iterencode(o, _one_shot=_one_shot)
        return map(smart_str, chunks)


class TemplateContextJsonRenderer(JSONRenderer):
    encoder_class = TemplateContextJsonEncoder
