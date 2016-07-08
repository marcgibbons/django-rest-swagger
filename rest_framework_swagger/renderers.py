from django.conf import settings
from django.shortcuts import resolve_url
from django.template import loader, RequestContext
from openapi_codec import OpenAPICodec
from rest_framework.renderers import BaseRenderer


class OpenAPIRenderer(BaseRenderer):
    media_type = 'application/openapi+json'
    charset = None
    format = 'openapi'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        codec = OpenAPICodec()
        return codec.dump(data)


class SwaggerUIRenderer(BaseRenderer):
    media_type = 'text/html'
    format = 'swagger'
    template = 'rest_framework_swagger/index.html'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        context = self.get_context(renderer_context)
        template = loader.get_template(self.template)

        return template.render(context)

    def get_context(self, renderer_context):
        path = renderer_context['request'].path
        urls = {
            'login_url': settings.LOGIN_URL,
            'logout_url': settings.LOGOUT_URL
        }
        renderer_context.update({
            key: '%s?next=%s' % (resolve_url(val), path)
            for key, val in urls.items()
        })

        return RequestContext(renderer_context['request'], renderer_context)
