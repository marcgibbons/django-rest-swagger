from unipath import Path

from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib.auth.models import User
from django.contrib.admindocs.utils import trim_docstring
from django.http import HttpRequest
from django.test import TestCase
from django.utils.importlib import import_module
from django.views.generic import View

from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework import serializers
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet, ViewSet

from .urlparser import UrlParser
from .docgenerator import DocumentationGenerator
from .introspectors import ViewSetIntrospector, APIViewIntrospector


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
        urls = patterns('', url(r'api/base/path/', include(self.url_patterns)))
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

        class MockApiViewSet(ModelViewSet):
            serializer_class = CommentSerializer
            model = User

        class AnotherMockApiViewSet(ModelViewSet):
            serializer_class = CommentSerializer
            model = User

        router = DefaultRouter()
        router.register(r'other_views', MockApiViewSet)
        router.register(r'more_views', MockApiViewSet)

        urls_app = patterns('', url(r'^', include(router.urls)))
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
        description = generator.get_description(MockApiView())

        self.assertEqual('A Test View', description)

    def test_get_method_docs(self):

        class TestApiView(APIView):
            def get(self, *args):
                """
                Here are my comments
                """
            pass

        introspector = APIViewIntrospector()
        docs_get = introspector.get_method_docs(TestApiView, 'GET')

        self.assertEqual("Here are my comments", docs_get.strip())

    def test_get_method_summary_without_docstring(self):

        class MyListView(ListCreateAPIView):
            """
            My comment
            """
            pass

        introspector = APIViewIntrospector()
        method_docs = introspector.get_method_summary(MyListView, 'POST')

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
        operations = docgen.get_operations(api)

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
        operations = docgen.get_operations(api)

        self.assertEqual([], operations)

    def test_strip_params_from_docstring(self):
        class AnAPIView(APIView):
            """
            My comments are here

            param -- my param
            """
            pass

        docgen = DocumentationGenerator()
        docstring = docgen.strip_params_from_docstring(trim_docstring(AnAPIView.__doc__))

        self.assertEqual("My comments are here<br/>", docstring)

    def test_strip_params_from_docstring_multiline(self):
        class TestView(APIView):
            """
            Creates a new user.
            Returns: token - auth token

            email -- e-mail address
            password -- password, optional
            city -- city, optional
            street -- street, optional
            number -- house number, optional
            zip_code -- zip code 10 chars, optional
            phone -- phone number in US format (XXX-XXX-XXXX), optional
            """
            pass

        docgen = DocumentationGenerator()
        docstring = docgen.strip_params_from_docstring(TestView.__doc__)
        expected = 'Creates a new user.<br/>Returns: token - auth token<br/>'

        self.assertEqual(expected, docstring)

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
        serializers = docgen.get_serializer_set(apis)

        self.assertIn(CommentSerializer, serializers)

    def test_get_serializer_fields(self):
        docgen = DocumentationGenerator()
        fields = docgen.get_serializer_fields(CommentSerializer)

        self.assertEqual(3, len(fields))

    def test_get_serializer_fields_api_with_no_serializer(self):
        docgen = DocumentationGenerator()
        fields = docgen.get_serializer_fields(None)

        self.assertIsNone(fields)

    def test_get_serializer_class_access_request_context(self):
        class MyListView(ListCreateAPIView):
            serializer_class = CommentSerializer
            def get_serializer_class(self):
                self.serializer_class.context = {'request': self.request}
                return self.serializer_class

        docgen = DocumentationGenerator()
        callback = MyListView
        callback.request = HttpRequest()
        serializer_class = docgen.get_serializer_class(MyListView)

        self.assertIs(serializer_class, CommentSerializer)

    def test_build_body_parameters(self):
        class SerializedAPI(ListCreateAPIView):
            serializer_class = CommentSerializer

        docgen = DocumentationGenerator()
        params = docgen.build_body_parameters(SerializedAPI)

        self.assertEqual('CommentSerializer', params['name'])

    def test_build_form_parameters(self):
        class SerializedAPI(ListCreateAPIView):
            serializer_class = CommentSerializer

        docgen = DocumentationGenerator()
        params = docgen.build_form_parameters(SerializedAPI, 'POST')

        self.assertEqual(len(CommentSerializer().get_fields()), len(params))

    def test_build_form_parameters_allowable_values(self):

        class MySerializer(serializers.Serializer):
            content = serializers.CharField(max_length=200, min_length=10, default="Vandalay Industries")
            a_read_only_field = serializers.BooleanField(read_only=True)

        class MyAPIView(ListCreateAPIView):
            serializer_class = MySerializer

        docgen = DocumentationGenerator()
        params = docgen.build_form_parameters(MyAPIView, 'POST')

        self.assertEqual(1, len(params))  # Read only field is ignored
        param = params[0]

        self.assertEqual('content', param['name'])
        self.assertEqual('form', param['paramType'])
        self.assertEqual(True, param['required'])
        self.assertEqual(200, param['allowableValues']['max'])
        self.assertEqual(10, param['allowableValues']['min'])
        self.assertEqual('Vandalay Industries', param['defaultValue'])


class ViewTestIntrospectorTest(TestCase):
    def test_get_allowed_methods(self):
        """
        Tests a ModelViewSet's allowed methods. If the path includes something like {pk},
        consider it an object view, otherwise, a list view
        """

        class MyViewSet(ModelViewSet):
            serializer_class = CommentSerializer
            model = User

        introspector = ViewSetIntrospector()

        # Test a list endpoint
        allowed_methods = introspector.get_allowed_methods(MyViewSet, '/api/endpoint')
        self.assertEqual(2, len(allowed_methods))
        self.assertIn('POST', allowed_methods)
        self.assertIn('GET', allowed_methods)

        # Test an object endpoint
        allowed_methods = introspector.get_allowed_methods(MyViewSet, '/api/endpoint/{pk}')
        self.assertEqual(4, len(allowed_methods))
        self.assertIn('POST', allowed_methods)
        self.assertIn('PATCH', allowed_methods)
        self.assertIn('DELETE', allowed_methods)
        self.assertIn('GET', allowed_methods)

    def test_is_custom_action_true(self):
        class MyViewSet(ViewSet):
            @action()
            def my_action(self, request):
                pass

        path = '/api/{pk}/my_action/'
        introspector = ViewSetIntrospector()

        self.assertTrue(introspector.is_custom_action(MyViewSet, path))

    def test_viewset_action_allowed_methods(self):
        class MyViewSet(ViewSet):
            @action()
            def do_something(self, request):
                """
                This is a REST action that does something. Django REST maps it
                to an HTTP POST method
                """

        callback = MyViewSet
        path = '/api-path/myviewset/{pk}/do_something/'

        path_components = Path(path).components()
        last_element = unicode(path_components[len(path_components) - 1])

        action_func = eval('callback.%s.im_func' % last_element)
        expected_result = action_func.bind_to_methods

        introspector = ViewSetIntrospector()
        allowed_methods = introspector.get_allowed_methods(callback, path)

        self.assertEqual(expected_result, allowed_methods)
