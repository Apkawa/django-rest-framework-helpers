# coding: utf-8
from __future__ import unicode_literals

from .._compat import StringIO

from .response import FileResponse


class PDFViewMixin(object):
    def response_to_pdf_response(self, response, filename=None):
        from weasyprint import HTML
        html = HTML(string=response.rendered_content, base_url="http://" + self.request.META['HTTP_HOST'])
        fp = StringIO()
        html.write_pdf(target=fp, zoom=1)
        fp.seek(0)
        return FileResponse(fp.read(), file_name=filename, content_type='application/pdf')


class PDFView(PDFViewMixin):
    param_name = 'pdf'

    def is_pdf_mode(self):
        return self.param_name in self.request.GET

    def get_filename(self):
        return 'file.pdf'

    def get(self, request, *args, **kwargs):
        response = super(PDFView, self).get(request, *args, **kwargs)
        if self.is_pdf_mode():
            self.finalize_response(request, response)
            response = self.response_to_pdf_response(response, filename=self.get_filename())
            return response
        return response
