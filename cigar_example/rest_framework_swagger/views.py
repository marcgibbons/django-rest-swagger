from rest_framework.views import Response
from urlparser import UrlParser
from apidocview import APIDocView


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
        api_data = []

        for api in apis:
            api_data.append(
                {
                    "description": "Poop",
                    "operations": [
                        {
                            "httpMethod": "GET",
                            "nickname": "poopie balls" + api['path'],
                            "notes": "Big poop",
                            "summary": "Poop",
                            "responseClass": "Fuck tard"
                        }
                    ],
                    "path": api['path']
                }
            )
        return Response(
            {
                "basePath": "http://localhost:8000/api",
                "apis": api_data
            }
        )
#        return Response(
#            {
#                "basePath": "http://localhost:8000/api",
#                "apis": [
#                    {
#                        "description": "Operations about pets",
#                        "operations": [
#                            {
#                                "httpMethod": "GET",
#                                "nickname": "getPetById",
#                                "notes": "Only Pets which you have permission to see will be returned",
#                                "responseClass": "Pet",
#                                "summary": "Find pet by its unique ID"
#                            }
#                        ],
#                        "path": "/" + path
#                    }
#                ]
#            }
#        )
#
    def get_api_for_resource(self, filter_path):
        urlparser = UrlParser()
        return urlparser.get_apis(filter_path=filter_path)
