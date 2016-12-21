# coding: utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

try:
    from phonenumbers import PhoneNumber, format_number
    from phonenumber_field.phonenumber import to_python
    from phonenumber_field.validators import validate_international_phonenumber
    from phonenumbers import PhoneNumberFormat


    class PhoneNumberField(serializers.CharField):
        default_error_messages = {
            'invalid': _('Enter a valid phone number.'),
        }
        default_validators = [validate_international_phonenumber]

        def to_internal_value(self, data):
            phone_number = to_python(data)
            if phone_number and not phone_number.is_valid():
                raise ValidationError(self.error_messages['invalid'])
            return phone_number

        def to_representation(self, value):
            if isinstance(value, PhoneNumber):
                return format_number(value, PhoneNumberFormat.INTERNATIONAL)
            return value
except ImportError:
    pass
