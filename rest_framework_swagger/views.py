import json
from django.utils import six

from django.conf import settings
from django.views.generic import View
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_text
from django.shortcuts import render_to_response, RequestContext
from django.core.exceptions import PermissionDenied
from .compat import import_string

from rest_framework.views import Response
from rest_framework.settings import api_settings
from rest_framework.utils import formatting

from rest_framework_swagger.urlparser import UrlParser
from rest_framework_swagger.apidocview import APIDocView
from rest_framework_swagger.docgenerator import DocumentationGenerator

import rest_framework_swagger as rfs


try:
    JSONRenderer = list(filter(
        lambda item: item.format == 'json',
        api_settings.DEFAULT_RENDERER_CLASSES,
    ))[0]
except IndexError:
    from rest_framework.renderers import JSONRenderer


def get_restructuredtext(view_cls, html=False):
    from docutils import core

    description = view_cls.__doc__ or ''
    description = formatting.dedent(smart_text(description))
    if html:
        parts = core.publish_parts(source=description, writer_name='html')
        html = parts['body_pre_docinfo'] + parts['fragment']
        return mark_safe(html)
    return description


def get_full_base_path(request):
    try:
        base_path = rfs.SWAGGER_SETTINGS['base_path']
    except KeyError:
        return request.build_absolute_uri(request.path).rstrip('/')
    else:
        protocol = 'https' if request.is_secure() else 'http'
        return '{0}://{1}'.format(protocol, base_path.rstrip('/'))


class SwaggerUIView(View):
    def get(self, request, *args, **kwargs):

        if not self.has_permission(request):
            return self.handle_permission_denied(request)

        template_name = rfs.SWAGGER_SETTINGS.get('template_path')
        data = {
            'swagger_settings': {
                'discovery_url': "%s/api-docs/" % get_full_base_path(request),
                'api_key': rfs.SWAGGER_SETTINGS.get('api_key', ''),
                'api_version': rfs.SWAGGER_SETTINGS.get('api_version', ''),
                'token_type': rfs.SWAGGER_SETTINGS.get('token_type'),
                'enabled_methods': mark_safe(
                    json.dumps(rfs.SWAGGER_SETTINGS.get('enabled_methods'))),
                'doc_expansion': rfs.SWAGGER_SETTINGS.get('doc_expansion', ''),
            },
            'rest_framework_settings': {
                'DEFAULT_VERSIONING_CLASS':
                    settings.REST_FRAMEWORK.get('DEFAULT_VERSIONING_CLASS', '')
                    if hasattr(settings, 'REST_FRAMEWORK') else None,

            },
            'django_settings': {
                'CSRF_COOKIE_NAME': mark_safe(
                    json.dumps(getattr(settings, 'CSRF_COOKIE_NAME', 'csrftoken'))),
            }
        }
        response = render_to_response(
            template_name, RequestContext(request, data))

        return response

    def has_permission(self, request):
        if rfs.SWAGGER_SETTINGS.get('is_superuser') and \
                not request.user.is_superuser:
            return False

        if rfs.SWAGGER_SETTINGS.get('is_authenticated') and \
                not request.user.is_authenticated():
            return False

        return True

    def handle_permission_denied(self, request):
        permission_denied_handler = rfs.SWAGGER_SETTINGS.get(
            'permission_denied_handler')
        if isinstance(permission_denied_handler, six.string_types):
            permission_denied_handler = import_string(
                permission_denied_handler)

        if permission_denied_handler:
            return permission_denied_handler(request)
        else:
            raise PermissionDenied()


class SwaggerResourcesView(APIDocView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, *args, **kwargs):
        apis = [{'path': '/' + path} for path in self.get_resources()]
        return Response({
            'apiVersion': rfs.SWAGGER_SETTINGS.get('api_version', ''),
            'swaggerVersion': '1.2',
            'basePath': self.get_base_path(),
            'apis': apis,
            'info': rfs.SWAGGER_SETTINGS.get('info', {
                'contact': '',
                'description': '',
                'license': '',
                'licenseUrl': '',
                'termsOfServiceUrl': '',
                'title': '',
            }),
        })

    def get_base_path(self):
        try:
            base_path = rfs.SWAGGER_SETTINGS['base_path']
        except KeyError:
            return self.request.build_absolute_uri(
                self.request.path).rstrip('/')
        else:
            protocol = 'https' if self.request.is_secure() else 'http'
            return '{0}://{1}/{2}'.format(protocol, base_path, 'api-docs')

    def get_resources(self):
        urlparser = UrlParser()
        urlconf = getattr(self.request, "urlconf", None)
        exclude_url_names = rfs.SWAGGER_SETTINGS.get('exclude_url_names')
        exclude_namespaces = rfs.SWAGGER_SETTINGS.get('exclude_namespaces')
        apis = urlparser.get_apis(urlconf=urlconf, exclude_url_names=exclude_url_names,
                                  exclude_namespaces=exclude_namespaces)
        authorized_apis = filter(lambda a: self.handle_resource_access(self.request, a['pattern']), apis)
        authorized_apis_list = list(authorized_apis)
        resources = urlparser.get_top_level_apis(authorized_apis_list)
        return resources


class SwaggerApiView(APIDocView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, path, *args, **kwargs):
        apis = self.get_apis_for_resource(path)
        generator = DocumentationGenerator(for_user=request.user)
        return Response({
            'apiVersion': rfs.SWAGGER_SETTINGS.get('api_version', ''),
            'swaggerVersion': '1.2',
            'basePath': self.api_full_uri.rstrip('/'),
            'resourcePath': '/' + path,
            'apis': generator.generate(apis),
            'models': generator.get_models(apis),
        })

    def get_apis_for_resource(self, filter_path):
        urlparser = UrlParser()
        urlconf = getattr(self.request, "urlconf", None)
        exclude_url_names = rfs.SWAGGER_SETTINGS.get('exclude_url_names')
        exclude_namespaces = rfs.SWAGGER_SETTINGS.get('exclude_namespaces')
        apis = urlparser.get_apis(urlconf=urlconf, filter_path=filter_path,
                                  exclude_url_names=exclude_url_names,
                                  exclude_namespaces=exclude_namespaces)
        authorized_apis = filter(lambda a: self.handle_resource_access(self.request, a['pattern']), apis)
        authorized_apis_list = list(authorized_apis)
        return authorized_apis_list
