
import coreapi
from django.shortcuts import render, resolve_url
from openapi_codec import OpenAPICodec
from rest_framework.renderers import BaseRenderer, JSONRenderer
from rest_framework import status
import simplejson as json

from .settings import swagger_settings


class OpenAPIRenderer(BaseRenderer):
    media_type = 'application/openapi+json'
    charset = None
    format = 'openapi'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context['response'].status_code != status.HTTP_200_OK:
            return JSONRenderer().render(data)

        assert isinstance(data, coreapi.Document), (
            'Expected a coreapi.Document, but received %s instead.' %
            type(data)
        )
        document = self.get_document(data, renderer_context)

        return OpenAPICodec().encode(document)

    def get_document(self, data, renderer_context):
        title = data.title
        url = data.url
        content = dict(data)
        self.add_customizations(content, renderer_context)

        return coreapi.Document(title=title, url=url, content=content)

    def add_customizations(self, data, renderer_context):
        """
        Adds settings, overrides, etc. to the specification.
        """
        self.add_security_definitions(data)
        if not data.get('host'):
            data['host'] = self.get_host(renderer_context)

    def add_security_definitions(self, data):
        if not swagger_settings.SECURITY_DEFINITIONS:
            return

        data['securityDefinitions'] = swagger_settings.SECURITY_DEFINITIONS

    def get_host(self, renderer_context):
        return renderer_context['request'].get_host()


class SwaggerUIRenderer(BaseRenderer):
    media_type = 'text/html'
    format = 'swagger'
    template = 'rest_framework_swagger/index.html'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        self.set_context(renderer_context)
        return render(
            renderer_context['request'],
            self.template,
            renderer_context
        )

    def set_context(self, renderer_context):
        renderer_context['USE_SESSION_AUTH'] = \
            swagger_settings.USE_SESSION_AUTH
        renderer_context.update(self.get_auth_urls())

        renderer_context['drs_settings'] = json.dumps(self.get_ui_settings())

    def get_auth_urls(self):
        urls = {}
        if swagger_settings.LOGIN_URL is not None:
            urls['LOGIN_URL'] = resolve_url(swagger_settings.LOGIN_URL)
        if swagger_settings.LOGOUT_URL is not None:
            urls['LOGOUT_URL'] = resolve_url(swagger_settings.LOGOUT_URL)

        return urls

    def get_ui_settings(self):
        data = {
            'apisSorter': swagger_settings.APIS_SORTER,
            'docExpansion': swagger_settings.DOC_EXPANSION,
            'jsonEditor': swagger_settings.JSON_EDITOR,
            'operationsSorter': swagger_settings.OPERATIONS_SORTER,
            'showRequestHeaders': swagger_settings.SHOW_REQUEST_HEADERS,
            'supportedSubmitMethods': swagger_settings.SUPPORTED_SUBMIT_METHODS
        }
        if swagger_settings.VALIDATOR_URL != '':
            data['validatorUrl'] = swagger_settings.VALIDATOR_URL

        return data
