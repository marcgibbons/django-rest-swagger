from coreapi.compat import force_bytes
from django.shortcuts import render, resolve_url
from openapi_codec import OpenAPICodec
from rest_framework.renderers import BaseRenderer
import simplejson as json

from .settings import swagger_settings


class OpenAPIRenderer(BaseRenderer):
    media_type = 'application/openapi+json'
    charset = None
    format = 'openapi'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = self.get_openapi_specification(data)
        self.add_customizations(data)

        return self.dump(data)

    def dump(self, data):
        return force_bytes(json.dumps(data))

    def get_openapi_specification(self, data):
        """
        Converts data into OpenAPI specification.
        """
        codec = OpenAPICodec()
        return json.loads(codec.dump(data))

    def add_customizations(self, data):
        """
        Adds settings, overrides, etc. to the specification.
        """
        self.add_security_definitions(data)

    def add_security_definitions(self, data):
        if not swagger_settings.SECURITY_DEFINITIONS:
            return

        data['securityDefinitions'] = swagger_settings.SECURITY_DEFINITIONS


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
        renderer_context.update(self.get_auth_urls(renderer_context))

    def get_auth_urls(self, renderer_context):
        return {
            setting: self.add_next_to_url(url, renderer_context['request'])
            for setting, url in self.get_auth_url_settings().items()
        }

    def get_auth_url_settings(self):
        """
        Returns a dictionary containing LOGIN_URL and LOGOUT_URL
        from settings.
        """
        return {
            'LOGIN_URL': swagger_settings.LOGIN_URL,
            'LOGOUT_URL': swagger_settings.LOGOUT_URL
        }

    def add_next_to_url(self, url, request):
        """
        Appends the current request.path as querystring to the current path.
        """
        return '%s?next=%s' % (resolve_url(url), request.path)
