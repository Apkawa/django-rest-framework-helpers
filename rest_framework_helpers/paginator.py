# coding: utf-8
from __future__ import unicode_literals

import six

from digg_paginator import DiggPaginator

from rest_framework import pagination
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param

from django.core.paginator import Paginator as DjangoPaginator, InvalidPage


class PageNumberPagination(pagination.PageNumberPagination):
    view = None
    page_size_query_param = 'page_size'
    django_paginator_class = DjangoPaginator

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def _build_url(self, page_number):
        url = self.request.build_absolute_uri()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)

    def get_page_range(self):
        page_range = []
        for num in self.page.page_range:
            page_info = None
            if num:
                page_info = {
                    'url': self._build_url(page_number=num),
                    'page_number': num,
                }
            page_range.append(page_info)

        return page_range

    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'count': self.page.paginator.count,
                'page_number': self.page.number,
                'page_range': self.get_page_range(),
            },
            'results': data
        })



class DiggPageNumberPagination(PageNumberPagination):
    django_paginator_class = DiggPaginator
