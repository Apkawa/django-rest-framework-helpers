# coding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

import django_filters

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.settings import api_settings

from .renderers import TemplateHTMLRenderer, TemplateContextJsonRenderer


class FilterMixin(object):
    def get_filter(self, queryset):
        for backend in list(self.filter_backends):
            if backend == django_filters.rest_framework.DjangoFilterBackend:
                b = backend()
                filter_class = b.get_filter_class(self, queryset)
                if not filter_class:
                    return None

                filter_instance = filter_class(self.request.query_params, queryset=queryset, request=self.request)
                return filter_instance


class SerializerViewMixin(object):
    serializer_class = None

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.serializer_class

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'view': self
        }


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class ApiContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(ApiContextMixin, self).get_context_data(**kwargs)
        return context


class SerializerProcessMixin(object):
    success_url = '.'

    def get_success_url(self, serializer):
        return self.success_url

    def serializer_valid(self, serializer):
        return redirect(self.get_success_url(serializer))

    def serializer_invalid(self, serializer):
        return Response(self.get_context_data(object=serializer.data, form=serializer))

    def get_initial_data(self):
        return {}

    def process(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_initial_data(), data=request.data)
        if serializer.is_valid():
            return self.serializer_valid(serializer)
        return self.serializer_invalid(serializer)

    def show_form(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_initial_data())
        return Response(self.get_context_data(object=serializer.data, form=serializer))


class SiteContextMixin(object):
    def get_site_context(self):
        return {}


class SerializerRendererMixin(SiteContextMixin):
    """
    A view that returns a templated HTML representation of a given user.
    """
    renderer_classes = (TemplateHTMLRenderer,)
    if settings.DEBUG:
        renderer_classes += (BrowsableAPIRenderer, TemplateContextJsonRenderer)
    template_name = None
    lookup_field = 'pk'

    def get_object_data(self, response):
        response_data = {}
        data = response.data
        if isinstance(data, list):
            response_data['object_list'] = data
        elif isinstance(self, ListAPIView):
            _data = data.pop('results', None)
            response_data.update(data)
            response_data['object_list'] = _data
        else:
            response_data['object'] = data
        return response_data

    def get_context_data(self, **kwargs):
        context = {'SITE_CONTEXT': self.get_site_context()}
        context.update(kwargs)
        context.pop('serializer', None)
        return context

    def prepare_templates(self, templates):
        # TODO
        return templates

    def get_template_names(self):
        templates = [self.template_name]
        new_templates = self.prepare_templates(templates)
        return new_templates

    def finalize_response(self, request, response, *args, **kwargs):
        return super(SerializerRendererMixin, self).finalize_response(request, response, *args, **kwargs)


class CreateModelMixin(object):
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            self.get_context_data(object=serializer.data, serializer=serializer),
            status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}


class ListModelMixin(FilterMixin):
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filter_instance = self.get_filter(queryset)
        queryset = self.filter_queryset(queryset)

        extra_context = dict(
            filter=filter_instance
        )

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data.update(self.get_context_data(serializer=serializer, **extra_context))
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response(self.get_context_data(object_list=serializer.data, serializer=serializer, **extra_context))


class RetrieveModelMixin(object):
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(self.object)
        return Response(self.get_context_data(object=serializer.data, serializer=serializer))


class UpdateModelProcessMixin(SerializerProcessMixin):
    """
    Update a model instance.
    """

    def serializer_valid(self, serializer):
        self.perform_update(serializer)
        return super(UpdateModelProcessMixin, self).serializer_valid(serializer)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        self.object = self.get_object()
        serializer = self.get_serializer(self.object, data=request.data, partial=partial)

        if serializer.is_valid():
            return self.serializer_valid(serializer)
        return self.serializer_invalid(serializer)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin(object):
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.perform_destroy(self.object)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
