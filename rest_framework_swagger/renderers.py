import coreapi
from coreapi.compat import force_bytes
from django.shortcuts import render, resolve_url
from openapi_codec import OpenAPICodec as _OpenAPICodec
from openapi_codec.encode import generate_swagger_object
from rest_framework.renderers import BaseRenderer, JSONRenderer
from rest_framework import status
import simplejson as json

from .settings import swagger_settings as settings


class OpenAPICodec(_OpenAPICodec):
    def encode(self, document, **options):
        if not isinstance(document, coreapi.Document):
            raise TypeError('Expected a `coreapi.Document` instance')

        data = generate_swagger_object(document)
        data.update(**options)

        return force_bytes(json.dumps(data))


class OpenAPIRenderer(BaseRenderer):
    media_type = 'application/openapi+json'
    charset = None
    format = 'openapi'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context['response'].status_code != status.HTTP_200_OK:
            return JSONRenderer().render(data)
        options = self.get_customizations()

        return OpenAPICodec().encode(data, **options)

    def get_customizations(self):
        """
        Adds settings, overrides, etc. to the specification.
        """
        data = {}
        if settings.SECURITY_DEFINITIONS:
            data['securityDefinitions'] = settings.SECURITY_DEFINITIONS

        return data


class SwaggerUIRenderer(BaseRenderer):
    media_type = 'text/html'
    format = 'swagger'
    template = 'rest_framework_swagger/index.html'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        self.set_context(data, renderer_context)
        return render(
            renderer_context['request'],
            self.template,
            renderer_context
        )

    def set_context(self, data, renderer_context):
        renderer_context['USE_SESSION_AUTH'] = \
            settings.USE_SESSION_AUTH
        renderer_context.update(self.get_auth_urls())

        drs_settings = self.get_ui_settings()
        renderer_context['drs_settings'] = json.dumps(drs_settings)
        renderer_context['spec'] = OpenAPIRenderer().render(
            data=data,
            renderer_context=renderer_context
        ).decode()

    def get_auth_urls(self):
        urls = {}
        if settings.LOGIN_URL is not None:
            urls['LOGIN_URL'] = resolve_url(settings.LOGIN_URL)
        if settings.LOGOUT_URL is not None:
            urls['LOGOUT_URL'] = resolve_url(settings.LOGOUT_URL)

        return urls

    def get_ui_settings(self):
        data = {
            'apisSorter': settings.APIS_SORTER,
            'docExpansion': settings.DOC_EXPANSION,
            'jsonEditor': settings.JSON_EDITOR,
            'operationsSorter': settings.OPERATIONS_SORTER,
            'showRequestHeaders': settings.SHOW_REQUEST_HEADERS,
            'supportedSubmitMethods': settings.SUPPORTED_SUBMIT_METHODS,
            'acceptHeaderVersion': settings.ACCEPT_HEADER_VERSION,
            'customHeaders': settings.CUSTOM_HEADERS,
        }
        if settings.VALIDATOR_URL != '':
            data['validatorUrl'] = settings.VALIDATOR_URL

        return data
