import os

from django.contrib.auth.signals import user_logged_in

from rest_framework_jwt.settings import api_settings

# generate pdf with html
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


def generate_jwt_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


class Render:

    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)

    @staticmethod
    def render_to_file(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        file_name = str(params['unit_info']['number']) + "_" + str(params['invoice_info']['invoice_no']) + ".pdf"
        file_path = "static/pdf/" + file_name
        with open(file_path, 'wb') as pdf:
            pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf)
        return [file_name, file_path]


    @staticmethod
    def render_to_contract_file(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        file_name = "contract_" + str(params['unit']['number']) + ".pdf"
        file_path = "static/pdf/" + file_name
        with open(file_path, 'wb') as pdf:
            pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf)
        return [file_name, file_path]
