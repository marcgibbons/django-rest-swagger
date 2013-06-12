from rest_framework.views import Response
from urlparser import UrlParser
from apidocview import APIDocView
from docgenerator import DocumentationGenerator

class SwaggerResourcesView(APIDocView):

    def get(self, request):
        resources = self.get_resources()
        host = request.build_absolute_uri()

        #base_path = "/%s" % resources['base_path']

        apis = []
        for path in resources['root_paths']:
            apis.append({
                'path': "/%s" % path,
            })

        return Response({
            'apiVersion': '1',
            'swaggerVersion': '1.1',
            'basePath': host,
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
            'basePath': 'http://localhost:8000/api'
        })

    def get_api_for_resource(self, filter_path):
        urlparser = UrlParser()
        return urlparser.get_apis(filter_path=filter_path)
