from django.views.generic import View
from django.shortcuts import render_to_response, RequestContext
from rest_framework.views import Response
from urlparser import UrlParser
from apidocview import APIDocView
from docgenerator import DocumentationGenerator


class SwaggerUIView(View):
    def get(self, request, *args, **kwargs):
        template_name = "rest_framework_swagger/index.html"
        data = {'settings': {
                'discovery_url': "%sapi-docs/" % request.build_absolute_uri()
                }
        }
        response = render_to_response(template_name, RequestContext(request, data))

        return response


class SwaggerResourcesView(APIDocView):

    def get(self, request):
        apis = []
        resources = self.get_resources()

        for path in resources['root_paths']:
            apis.append({
                'path': "/%s" % path,
            })

        return Response({
            'apiVersion': '1',
            'swaggerVersion': '1.2.4',
            'basePath': self.host,
            'apis': apis
        })

    def get_resources(self):
        urlparser = UrlParser()
        apis = urlparser.get_apis()
        return urlparser.get_top_level_apis(apis)


class SwaggerApiView(APIDocView):

    def get(self, request, path):
        apis = self.get_api_for_resource(path)
        generator = DocumentationGenerator()

        return Response({
            'apis': generator.generate(apis),
            'models': generator.get_models(apis),
            'basePath': self.api_full_uri,
        })

    def get_api_for_resource(self, filter_path):
        urlparser = UrlParser()
        return urlparser.get_apis(filter_path=filter_path)
