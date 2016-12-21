# coding: utf-8
from __future__ import unicode_literals
from rest_framework.generics import GenericAPIView as _GenericAPIView
from rest_framework.response import Response

from . import mixins


class GenericAPIView(
    mixins.SerializerRendererMixin,
    _GenericAPIView):
    def get_paginated_response(self, data):
        response = super(GenericAPIView, self).get_paginated_response(data)
        response.data['object_list'] = response.data.pop('results')
        return response



class TemplateApiView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response(self.get_context_data())


class SerializerProcessApiView(mixins.SerializerProcessMixin, GenericAPIView):
    def post(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.show_form(request, *args, **kwargs)


class CreateAPIView(mixins.CreateModelMixin,
    GenericAPIView):
    """
    Concrete view for creating a model instance.
    """

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListAPIView(mixins.ListModelMixin,
    GenericAPIView):
    """
    Concrete view for listing a queryset.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveAPIView(mixins.RetrieveModelMixin,
    GenericAPIView):
    """
    Concrete view for retrieving a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class DestroyAPIView(mixins.DestroyModelMixin,
    GenericAPIView):
    """
    Concrete view for deleting a model instance.
    """

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UpdateAPIView(mixins.UpdateModelProcessMixin,
    GenericAPIView):
    """
    Concrete view for updating a model instance.
    """

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListCreateAPIView(mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveUpdateAPIView(mixins.RetrieveModelMixin,
    mixins.UpdateModelProcessMixin,
    GenericAPIView):
    """
    Concrete view for retrieving, updating a model instance.
    """

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(self.get_context_data(object=serializer.data, serializer=serializer, form=serializer))

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RetrieveDestroyAPIView(mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView):
    """
    Concrete view for retrieving or deleting a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
    mixins.UpdateModelProcessMixin,
    mixins.DestroyModelMixin,
    GenericAPIView):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
