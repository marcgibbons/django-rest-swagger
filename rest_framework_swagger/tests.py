from django.conf import settings
from django.utils.importlib import import_module
from django.conf.urls import patterns, url, include
from django.test import TestCase
from rest_framework_swagger.urlparser import UrlParser
from rest_framework_swagger.docgenerator import DocumentationGenerator
from django.contrib.admindocs.utils import trim_docstring

from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework import serializers
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet


class MockApiView(APIView):
    """
    A Test View

    This is more commenting
    """
    def get(self, request):
        """
        Get method specific comments
        """
        pass
    pass

class NonApiView(View):
    pass


class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()


class UrlParserTest(TestCase):
    def setUp(self):
        self.url_patterns = patterns('',
            url(r'a-view/?$', MockApiView.as_view(), name='a test view'),
            url(r'a-view/child/?$', MockApiView.as_view()),
            url(r'a-view/child2/?$', MockApiView.as_view()),
            url(r'another-view/?$', MockApiView.as_view(), name='another test view'),
        )

    def test_get_apis(self):
        urlparser = UrlParser()
        urls = import_module(settings.ROOT_URLCONF)
        # Overwrite settings with test patterns
        urls.urlpatterns = self.url_patterns
        apis = urlparser.get_apis()

        for api in apis:
            self.assertIn(api['pattern'], self.url_patterns)

    def test_flatten_url_tree(self):
        urlparser = UrlParser()
        apis = urlparser.get_apis(self.url_patterns)

        self.assertEqual(len(self.url_patterns), len(apis))

    def test_flatten_url_tree_url_import(self):
        urls = patterns('',
            url(r'api/base/path/', include(self.url_patterns))
        )
        urlparser = UrlParser()
        apis = urlparser.get_apis(urls)

        self.assertEqual(len(self.url_patterns), len(apis))

    def test_flatten_url_tree_with_filter(self):
        urlparser = UrlParser()
        apis = urlparser.get_apis(self.url_patterns, filter_path="a-view")

        self.assertEqual(1, len(apis))

    def test_flatten_url_tree_excluded_namesapce(self):
        urls = patterns('',
            url(r'api/base/path/', include(self.url_patterns, namespace='exclude'))
        )
        urlparser = UrlParser()
        apis = urlparser.__flatten_patterns_tree__(patterns=urls, exclude_namespaces='exclude')

        self.assertEqual([], apis)

    def test_flatten_url_tree_url_import_with_routers(self):
        from django.contrib.auth.models import User

        class MockApiViewSet(ModelViewSet):
            serializer_class = CommentSerializer
            model = User

        class AnotherMockApiViewSet(ModelViewSet):
            serializer_class = CommentSerializer
            model = User

        router = DefaultRouter()
        router.register(r'other_views', MockApiViewSet)
        router.register(r'more_views', MockApiViewSet)

        urls_app = patterns('',
            url(r'^', include(router.urls))
        )
        urls = patterns('',
            url(r'api/', include(urls_app)),
            url(r'test/', include(urls_app))
        )
        urlparser = UrlParser()
        apis = urlparser.get_apis(urls)

        self.assertEqual(sum(api['path'].find('api') != -1 for api in apis), 4)
        self.assertEqual(sum(api['path'].find('test') != -1 for api in apis), 4)

    def test_get_api_callback(self):
        urlparser = UrlParser()
        callback = urlparser.__get_pattern_api_callback__(self.url_patterns[0])

        self.assertTrue(issubclass(callback, MockApiView))

    def test_get_api_callback_not_rest_view(self):
        urlparser = UrlParser()
        non_api = patterns('',
            url(r'something', NonApiView.as_view())
        )
        callback = urlparser.__get_pattern_api_callback__(non_api)

        self.assertIsNone(callback)

    def test_get_top_level_api(self):
        urlparser = UrlParser()
        apis = urlparser.get_top_level_apis(urlparser.get_apis(self.url_patterns))

        self.assertEqual(4, len(apis))


    def test_assemble_endpoint_data(self):
        """
        Tests that the endpoint data is correctly packaged
        """
        urlparser = UrlParser()
        pattern = self.url_patterns[0]

        data = urlparser.__assemble_endpoint_data__(pattern)

        self.assertEqual(data['path'], '/a-view/')
        self.assertEqual(data['callback'], MockApiView)
        self.assertEqual(data['pattern'], pattern)

    def test_assemble_data_with_non_api_callback(self):
        bad_pattern = patterns('', url(r'^some_view/', NonApiView.as_view()))

        urlparser = UrlParser()
        data = urlparser.__assemble_endpoint_data__(bad_pattern)

        self.assertIsNone(data)

    def test_exclude_router_api_root(self):
        from django.contrib.auth.models import User

        class MyViewSet(ModelViewSet):
            serializer_class = CommentSerializer
            model = User

        router = DefaultRouter()
        router.register('test', MyViewSet)

        urls_created = len(router.urls)

        parser = UrlParser()
        apis = parser.get_apis(router.urls)

        self.assertEqual(4, urls_created - len(apis))




class DocumentationGeneratorTest(TestCase):
    def setUp(self):
        self.url_patterns = patterns('',
            url(r'a-view/?$', MockApiView.as_view(), name='a test view'),
            url(r'a-view/child/?$', MockApiView.as_view()),
            url(r'a-view/<pk>/?$', MockApiView.as_view(), name="detailed view for mock"),
            url(r'another-view/?$', MockApiView.as_view(), name='another test view'),
        )

    def test_get_description(self):
        generator = DocumentationGenerator()
        description = generator.__get_description__(MockApiView())

        self.assertEqual('A Test View', description)

    def test_get_method_docs(self):

        class TestApiView(APIView):
            def get(self, *args):
                """
                Here are my comments
                """
            pass

        generator = DocumentationGenerator()
        docs_get = generator.__get_method_docs__(TestApiView(), 'GET')

        self.assertEqual("Here are my comments", docs_get)

    def test_get_method_generic_api_view(self):

        class MyListView(ListCreateAPIView):
            """
            My comment
            """
            pass

        generator = DocumentationGenerator()
        method_docs = generator.__get_method_docs__(MyListView(), 'POST')

        self.assertEqual("My comment", method_docs)

    def test_get_operations(self):

        class AnAPIView(APIView):
            def post(self, *args, **kwargs):
                pass

        api = {
            'path': 'a-path/',
            'callback': AnAPIView,
            'pattern': patterns('')
        }
        docgen = DocumentationGenerator()
        operations = docgen.__get_operations__(api)

        self.assertEqual('POST', operations[0]['httpMethod'])

    def test_get_operations_with_no_methods(self):

        class AnAPIView(APIView):
            pass

        api = {
            'path': 'a-path/',
            'callback': AnAPIView,
            'pattern': patterns('')
        }
        docgen = DocumentationGenerator()
        operations = docgen.__get_operations__(api)

        self.assertEqual([], operations)

    def test_strip_params_from_docstring(self):
        class AnAPIView(APIView):
            """
            My comments are here

            param -- my param
            """
            pass

        docgen = DocumentationGenerator()
        docstring = docgen.__strip_params_from_docstring__(trim_docstring(AnAPIView.__doc__))

        self.assertEqual("My comments are here<br/><br/>", docstring)

    def test_get_models(self):
        class SerializedAPI(ListCreateAPIView):
            serializer_class = CommentSerializer

        urlparser = UrlParser()
        url_patterns = patterns('', url(r'my-api/', SerializedAPI.as_view()))
        apis = urlparser.get_apis(url_patterns)

        docgen = DocumentationGenerator()
        models = docgen.get_models(apis)

        self.assertIn('CommentSerializer', models)

    def test_get_serializer_set(self):
        class SerializedAPI(ListCreateAPIView):
            serializer_class = CommentSerializer

        urlparser = UrlParser()
        url_patterns = patterns('', url(r'my-api/', SerializedAPI.as_view()))
        apis = urlparser.get_apis(url_patterns)

        docgen = DocumentationGenerator()
        serializers = docgen.__get_serializer_set__(apis)

        self.assertIn(CommentSerializer, serializers)

    def test_get_serializer_fields(self):
        docgen = DocumentationGenerator()
        fields = docgen.__get_serializer_fields__(CommentSerializer)

        self.assertEqual(3, len(fields))

    def test_get_serializer_fields_api_with_no_serializer(self):
        docgen = DocumentationGenerator()
        fields = docgen.__get_serializer_fields__(None)

        self.assertIsNone(fields)

    def test_build_body_parameters(self):
        class SerializedAPI(ListCreateAPIView):
            serializer_class = CommentSerializer

        docgen = DocumentationGenerator()
        params = docgen.__build_body_parameters__(SerializedAPI)

        self.assertEqual('CommentSerializer', params['name'])


    def test_build_form_parameters(self):
        class SerializedAPI(ListCreateAPIView):
            serializer_class = CommentSerializer

        docgen = DocumentationGenerator()
        params = docgen.__build_form_parameters__(SerializedAPI, 'POST')

        self.assertEqual(len(CommentSerializer().get_fields()), len(params))

    def test_build_form_parameters_allowable_values(self):

        class MySerializer(serializers.Serializer):
            content = serializers.CharField(max_length=200, min_length=10, default="Vandalay Industries")
            a_read_only_field = serializers.BooleanField(read_only=True)

        class MyAPIView(ListCreateAPIView):
            serializer_class = MySerializer

        docgen = DocumentationGenerator()
        params = docgen.__build_form_parameters__(MyAPIView, 'POST')

        self.assertEqual(1, len(params))  # Read only field is ignored
        param = params[0]

        self.assertEqual('content', param['name'])
        self.assertEqual('form', param['paramType'])
        self.assertEqual(True, param['required'])
        self.assertEqual(200, param['allowableValues']['max'])
        self.assertEqual(10, param['allowableValues']['min'])
        self.assertEqual('Vandalay Industries', param['defaultValue'])

    def test_get_allowed_methods(self):
        """
        Tests a ModelViewSet's allowed methods. If the path includes something like {pk},
        consider it an object view, otherwise, a list view
        """
        from django.contrib.auth.models import User

        class MyViewSet(ModelViewSet):
            serializer_class = CommentSerializer
            model = User

        docgen = DocumentationGenerator()

        # Test a list endpoint
        allowed_methods = docgen.__get_allowed_methods__(MyViewSet, '/api/endpoint')
        self.assertEqual(2, len(allowed_methods))
        self.assertIn('POST', allowed_methods)
        self.assertIn('GET', allowed_methods)

        # Test an object endpoint
        allowed_methods = docgen.__get_allowed_methods__(MyViewSet, '/api/endpoint/{pk}')
        self.assertEqual(4, len(allowed_methods))
        self.assertIn('POST', allowed_methods)
        self.assertIn('PATCH', allowed_methods)
        self.assertIn('DELETE', allowed_methods)
        self.assertIn('GET', allowed_methods)
