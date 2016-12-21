# coding: utf-8
from __future__ import unicode_literals

from rest_framework.response import Response


class FileResponse(Response):
    """
    DRF Response to render data as a PDF File.
    kwargs:
        - pdf (byte array). The PDF file content.
        - file_name (string). The default downloaded file name.
    """

    def __init__(self, file_content, file_name, content_type=None, *args, **kwargs):
        headers = {
            'Content-Disposition': 'filename="{}"'.format(file_name),
            'Content-Length': len(file_content),
        }
        # TODO get content_type from filename
        super(FileResponse, self).__init__(
            file_content,
            content_type=content_type or 'application/pdf',
            headers=headers,
            *args,
            **kwargs
        )

    @property
    def rendered_content(self):
        self['Content-Type'] = self.content_type
        return self.data
