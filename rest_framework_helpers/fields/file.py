# coding: utf-8
from __future__ import unicode_literals

import base64

import warnings
from django.core.files.base import ContentFile
from rest_framework import serializers

from .mixins import AbsoluteUrlMixin


class NullFileField(serializers.FileField):
    '''
    Фикс бага с FileField
    '''

    def to_representation(self, value):
        if not value:
            return value
        return super(NullFileField, self).to_representation(value)


class AbsoluteURIFileField(AbsoluteUrlMixin, serializers.FileField):
    pass


class MethodAbsoluteURIFileField(serializers.SerializerMethodField, AbsoluteUrlMixin):
    def to_representation(self, value):
        value = super(MethodAbsoluteURIFileField, self).to_representation(value)
        if not value:
            return None
        return self._to_absolute(value)


class Base64FileField(AbsoluteURIFileField):
    def to_internal_value(self, data):
        if isinstance(data, basestring):
            # todo best parsing dataUrl
            # data:image/png;base64,iVBORw0KGgoAAAAN
            # base64 encoded image - decode
            spl_data = data.split(",")
            if len(spl_data) == 2:
                dataURI, imgstr = spl_data
                format, encode_type = dataURI.split(';')  # format ~= data:image/X,
                ext = format.split('/')[-1].split("+")[0]  # guess file extension
            else:
                ext = "jpeg"
                imgstr = spl_data[0]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super(Base64FileField, self).to_internal_value(data)


try:
    from easy_thumbnails.exceptions import InvalidImageFormatError
    from easy_thumbnails.files import ThumbnailerFieldFile


    class EasyThumbnailAbsoluteFileField(AbsoluteURIFileField):
        def __init__(self, *args, **kwargs):
            self.thumbnail_field = kwargs.pop('thumbnail_field', None)
            super(EasyThumbnailAbsoluteFileField, self).__init__(*args, **kwargs)

        def to_representation(self, value):
            if not value:
                return None
            thumbnail_obj = value
            if self.thumbnail_field and isinstance(value, ThumbnailerFieldFile):
                try:
                    thumbnail_obj = value[self.thumbnail_field]
                except InvalidImageFormatError:
                    return None
            return super(EasyThumbnailAbsoluteFileField, self).to_representation(thumbnail_obj)
except ImportError:
    warnings.warn("EasyThumbnailAbsoluteFileField need easy-thumbnails package", ImportWarning)
