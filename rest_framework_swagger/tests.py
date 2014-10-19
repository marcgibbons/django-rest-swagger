import datetime

from django.core.urlresolvers import RegexURLResolver
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib.auth.models import User
from django.contrib.admindocs.utils import trim_docstring
from django.http import HttpRequest
from django.test import TestCase
from django.utils.importlib import import_module
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework import serializers
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view

from .decorators import wrapper_to_func, func_to_wrapper
from .urlparser import UrlParser
from .docgenerator import DocumentationGenerator
from .introspectors import ViewSetIntrospector, APIViewIntrospector, \
    WrappedAPIViewIntrospector, WrappedAPIViewMethodIntrospector, \
    IntrospectorHelper, APIViewMethodIntrospector


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
    created = serializers.DateTimeField(default=datetime.datetime.now)


class UrlParserTest(TestCase):
    def setUp(self):
        self.url_patterns = patterns(
            '',
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

    def test_resources_starting_with_letters_from_base_path(self):
        base_path = r'api/'
        url_patterns = patterns('',
                                url(r'test', MockApiView.as_view(), name='a test view'),
                                url(r'pai_test', MockApiView.as_view(), name='start with letters a, p, i'),
                                )
        urls = patterns('', url(base_path, include(url_patterns)))
        urlparser = UrlParser()
        apis = urlparser.get_apis(urls)
        resources = urlparser.get_top_level_apis(apis)
        self.assertEqual(set(resources), set([base_path + url_pattern.regex.pattern for url_pattern in url_patterns]))

    def test_flatten_url_tree_with_filter(self):
        urlparser = UrlParser()
        apis = urlparser.get_apis(self.url_patterns, filter_path="a-view")

        self.assertEqual(3, len(apis))

    def test_filter_custom(self):
        urlparser = UrlParser()
        apis = [{'path': '/api/custom'}]
        apis2 = urlparser.get_filtered_apis(apis, 'api/custom')
        self.assertEqual(apis, apis2)

    def test_flatten_url_tree_excluded_namesapce(self):
        urls = patterns(
            '',
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
        urls = patterns(
            '',
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
        non_api = patterns(
            '',
            url(r'something', NonApiView.as_view())
        )
        callback = urlparser.__get_pattern_api_callback__(non_api)

        self.assertIsNone(callback)

    def test_get_top_level_api(self):
        urlparser = UrlParser()
        apis = urlparser.get_top_level_apis(urlparser.get_apis(self.url_patterns))

        self.assertEqual(2, len(apis))

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

    def test_get_base_path_for_common_endpoints(self):
        parser = UrlParser()
        paths = ['api/endpoint1', 'api/endpoint2']
        base_path = parser.__get_base_path__(paths)

        self.assertEqual('api/', base_path)

    def test_get_base_path_for_root_level_endpoints(self):
        parser = UrlParser()
        paths = ['endpoint1', 'endpoint2', 'endpoint3']
        base_path = parser.__get_base_path__(paths)

        self.assertEqual('', base_path)


class NestedUrlParserTest(TestCase):
    def setUp(self):
        class FuzzyApiView(APIView):
            def get(self, request):
                pass

        class ShinyApiView(APIView):
            def get(self, request):
                pass

        api_fuzzy_url_patterns = patterns(
            '', url(r'^item/$', FuzzyApiView.as_view(), name='find_me'))
        api_shiny_url_patterns = patterns(
            '', url(r'^item/$', ShinyApiView.as_view(), name='hide_me'))

        fuzzy_app_urls = patterns(
            '', url(r'^api/', include(api_fuzzy_url_patterns,
                                      namespace='api_fuzzy_app')))
        shiny_app_urls = patterns(
            '', url(r'^api/', include(api_shiny_url_patterns,
                                      namespace='api_shiny_app')))

        self.project_urls = patterns(
            '',
            url('my_fuzzy_app/', include(fuzzy_app_urls)),
            url('my_shiny_app/', include(shiny_app_urls)),
        )

    def test_exclude_nested_urls(self):

        url_parser = UrlParser()
        # Overwrite settings with test patterns
        urlpatterns = self.project_urls
        apis = url_parser.get_apis(urlpatterns,
                                   exclude_namespaces=['api_shiny_app'])
        self.assertEqual(len(apis), 1)
        self.assertEqual(apis[0]['pattern'].name, 'find_me')


class DocumentationGeneratorTest(TestCase):
    def setUp(self):
        self.url_patterns = patterns(
            '',
            url(r'a-view/?$', MockApiView.as_view(), name='a test view'),
            url(r'a-view/child/?$', MockApiView.as_view()),
            url(r'a-view/<pk>/?$', MockApiView.as_view(), name="detailed view for mock"),
            url(r'another-view/?$', MockApiView.as_view(), name='another test view'),
        )

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

        self.assertEqual('POST', operations[0]['method'])

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

    def test_get_models(self):
        class SerializedAPI(ListCreateAPIView):
            serializer_class = CommentSerializer

        urlparser = UrlParser()
        url_patterns = patterns('', url(r'my-api/', SerializedAPI.as_view()))
        apis = urlparser.get_apis(url_patterns)

        docgen = DocumentationGenerator()
        models = docgen.get_models(apis)

        self.assertIn('CommentSerializer', models)

    def test_get_models_resolves_callable_values(self):
        class SerializedAPI(ListCreateAPIView):
            serializer_class = CommentSerializer

        urlparser = UrlParser()
        url_patterns = patterns('', url(r'my-api/', SerializedAPI.as_view()))
        apis = urlparser.get_apis(url_patterns)

        docgen = DocumentationGenerator()
        models = docgen.get_models(apis)

        created_prop = models['CommentSerializer']['properties']['created']
        value = created_prop['defaultValue']
        delta = datetime.timedelta(seconds=1)
        self.assertAlmostEqual(value, datetime.datetime.now(), delta=delta)

    def test_get_serializer_set(self):
        class SerializedAPI(ListCreateAPIView):
            serializer_class = CommentSerializer

        urlparser = UrlParser()
        url_patterns = patterns('', url(r'my-api/', SerializedAPI.as_view()))
        apis = urlparser.get_apis(url_patterns)

        docgen = DocumentationGenerator()
        serializers = docgen._get_serializer_set(apis)

        self.assertIn(CommentSerializer, serializers)

    def test_get_serializer_fields(self):
        docgen = DocumentationGenerator()
        fields = docgen._get_serializer_fields(CommentSerializer)

        self.assertEqual(3, len(fields['fields']))

    def test_get_serializer_fields_api_with_no_serializer(self):
        docgen = DocumentationGenerator()
        fields = docgen._get_serializer_fields(None)

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
        serializer_class = docgen._get_serializer_class(MyListView)

        self.assertIs(serializer_class, CommentSerializer)


class IntrospectorHelperTest(TestCase):
    def test_strip_yaml_from_docstring(self):
        class AnAPIView(APIView):
            """
            My comments are here
            ---
            # This is YAML
            param: my param
            """
            pass

        docstring = IntrospectorHelper.strip_yaml_from_docstring(trim_docstring(AnAPIView.__doc__))

        self.assertEqual("My comments are here", docstring)

    def test_strip_params_from_docstring_multiline(self):
        class TestView(APIView):
            """
            Creates a new user.
            Returns: token - auth token
            ---
            # This is YAML
            param: my param
            foo: 123
            """
            pass

        docstring = IntrospectorHelper.strip_yaml_from_docstring(TestView.__doc__)
        expected = 'Creates a new user.\nReturns: token - auth token'

        self.assertEqual(expected, docstring)


class ViewSetTestIntrospectorTest(TestCase):
    def test_get_allowed_methods_list(self):
        class MyViewSet(ModelViewSet):
            serializer_class = CommentSerializer
            model = User

        # Test a list endpoint
        introspector = ViewSetIntrospector(
            MyViewSet,
            '/api/endpoint',
            url(r'^/api/endpoint$', MyViewSet.as_view({
                'get': 'list',
                'post': 'create'
            }))
        )
        allowed_methods = list(introspector)
        self.assertEqual(2, len(allowed_methods))
        allowed_methods = [method.get_http_method() for method in allowed_methods]
        self.assertIn('POST', allowed_methods)
        self.assertIn('GET', allowed_methods)

    def test_get_allowed_methods_object(self):
        class MyViewSet(ModelViewSet):
            serializer_class = CommentSerializer
            model = User

        # Test an object endpoint
        introspector = ViewSetIntrospector(
            MyViewSet,
            '/api/endpoint/{pk}',
            url(
                r'^/api/endpoint/(?P<{pk}>[^/]+)$',
                MyViewSet.as_view({
                    'get': 'retrieve',
                    'put': 'update',
                    'patch': 'partial_update',
                    'delete': 'destroy'
                })
            )
        )
        allowed_methods = list(introspector)
        self.assertEqual(4, len(allowed_methods))
        allowed_methods = [method.get_http_method() for method in allowed_methods]
        self.assertIn('PUT', allowed_methods)
        self.assertIn('PATCH', allowed_methods)
        self.assertIn('DELETE', allowed_methods)
        self.assertIn('GET', allowed_methods)


class BaseViewIntrospectorTest(TestCase):
    def test_get_description(self):
        introspector = APIViewIntrospector(MockApiView, '/', RegexURLResolver(r'^/', ''))
        self.assertEqual('A Test View', introspector.get_description())

    def test_get_serializer_class(self):
        introspector = APIViewIntrospector(MockApiView, '/', RegexURLResolver(r'^/', ''))
        self.assertEqual(None, introspector.get_serializer_class())


class BaseMethodIntrospectorTest(TestCase):
    def test_get_method_docs(self):

        class TestApiView(APIView):
            def get(self, *args):
                """
                Here are my comments
                """
            pass

        class_introspector = ViewSetIntrospector(TestApiView, '/{pk}', RegexURLResolver(r'^/(?P<{pk}>[^/]+)$', ''))
        introspector = APIViewMethodIntrospector(class_introspector, 'GET')
        docs_get = introspector.get_docs()

        self.assertEqual("Here are my comments", docs_get.strip())

    def test_get_method_summary_without_docstring(self):

        class MyListView(ListCreateAPIView):
            """
            My comment
            """
            pass

        class_introspector = ViewSetIntrospector(MyListView, '/{pk}', RegexURLResolver(r'^/(?P<{pk}>[^/]+)$', ''))
        introspector = APIViewMethodIntrospector(class_introspector, 'POST')
        method_docs = introspector.get_summary()

        self.assertEqual("My comment", method_docs)

    def test_build_body_parameters(self):
        class SerializedAPI(ListCreateAPIView):
            serializer_class = CommentSerializer

        class_introspector = ViewSetIntrospector(SerializedAPI, '/', RegexURLResolver(r'^/$', ''))
        introspector = APIViewMethodIntrospector(class_introspector, 'POST')
        params = introspector.build_body_parameters()

        self.assertEqual('CommentSerializer', params['name'])

    def test_build_form_parameters(self):
        class SerializedAPI(ListCreateAPIView):
            serializer_class = CommentSerializer

        class_introspector = ViewSetIntrospector(SerializedAPI, '/', RegexURLResolver(r'^/$', ''))
        introspector = APIViewMethodIntrospector(class_introspector, 'POST')
        params = introspector.build_form_parameters()

        self.assertEqual(len(CommentSerializer().get_fields()), len(params))

    def test_build_form_parameters_allowable_values(self):

        class MySerializer(serializers.Serializer):
            content = serializers.CharField(max_length=200, min_length=10, default="Vandalay Industries")
            a_read_only_field = serializers.BooleanField(read_only=True)

        class MyAPIView(ListCreateAPIView):
            serializer_class = MySerializer

        class_introspector = ViewSetIntrospector(MyAPIView, '/', RegexURLResolver(r'^/$', ''))
        introspector = APIViewMethodIntrospector(class_introspector, 'POST')
        params = introspector.build_form_parameters()

        self.assertEqual(1, len(params))  # Read only field is ignored
        param = params[0]

        self.assertEqual('content', param['name'])
        self.assertEqual('form', param['paramType'])
        self.assertEqual(True, param['required'])
        self.assertEqual('Vandalay Industries', param['defaultValue'])

    def test_build_form_parameters_callable_default_value_is_resolved(self):

        class MySerializer(serializers.Serializer):
            content = serializers.IntegerField(default=lambda: 203)

        class MyAPIView(ListCreateAPIView):
            serializer_class = MySerializer

        class_introspector = ViewSetIntrospector(MyAPIView, '/', RegexURLResolver(r'^/$', ''))
        introspector = APIViewMethodIntrospector(class_introspector, 'POST')
        params = introspector.build_form_parameters()

        self.assertEqual(1, len(params))
        param = params[0]

        self.assertEqual('content', param['name'])
        self.assertEqual('form', param['paramType'])
        self.assertEqual(True, param['required'])
        self.assertEqual(203, param['defaultValue'])


class YAMLDocstringParserTests(TestCase):

    def test_yaml_loader(self):
        class AnAPIView(APIView):
            def get(self):
                """
                My comments are here
                ---
                # This is YAML
                param: my param
                """
                pass

        class_introspector = ViewSetIntrospector(
            AnAPIView, '/', RegexURLResolver(r'^/$', '')
        )
        introspector = APIViewMethodIntrospector(class_introspector, 'GET')
        doc_parser = introspector.get_yaml_parser()
        self.assertEqual(doc_parser.object['param'], 'my param')

    def test_yaml_loader_class_yaml(self):
        class AnAPIView(APIView):
            """
            ---
            GET:
                param: my param
            """
            def get(self):
                """
                My comments are here
                ---
                # This is YAML
                param: your param
                """
                pass

        class_introspector = ViewSetIntrospector(
            AnAPIView, '/', RegexURLResolver(r'^/$', '')
        )
        class_introspector.methods = lambda: ['GET']
        introspector = APIViewMethodIntrospector(class_introspector, 'GET')
        doc_parser = introspector.get_yaml_parser()
        self.assertEqual(doc_parser.object['param'], 'your param')

    def test_yaml_loader_class_yaml2(self):
        class AnAPIView(APIView):
            """
            ---
            GET:
                param: my param
            """
            def get(self):
                """
                My comments are here
                ---
                # This is YAML
                """
                pass

        class_introspector = ViewSetIntrospector(
            AnAPIView, '/', RegexURLResolver(r'^/$', '')
        )
        class_introspector.methods = lambda: ['GET']
        introspector = APIViewMethodIntrospector(class_introspector, 'GET')
        doc_parser = introspector.get_yaml_parser()
        self.assertEqual(doc_parser.object['param'], 'my param')

    def test_yaml_loader_class_yaml3(self):
        class MyViewSet(ModelViewSet):
            """
            ---
            GET:
                param: my param
            """
            serializer_class = CommentSerializer
            model = User

        # Test a list endpoint
        introspector = ViewSetIntrospector(
            MyViewSet,
            '/api/endpoint',
            url(r'^/api/endpoint$', MyViewSet.as_view({
                'get': 'list',
                'post': 'create'
            }))
        )
        allowed_methods = list(introspector)
        self.assertEqual(2, len(allowed_methods))
        allowed_methods = [method.get_http_method() for method in allowed_methods]
        self.assertIn('POST', allowed_methods)
        self.assertIn('GET', allowed_methods)
        self.assertIn('list', introspector.methods())
        self.assertIn('create', introspector.methods())
        try:
            introspector = APIViewMethodIntrospector(introspector, 'get')
            introspector.get_yaml_parser()
        except Exception as e:
            self.assertIn('in class docstring are not in view methods', str(e))
        else:
            self.assertTrue(False)

    def test_yaml_loader_class_yaml4(self):
        class MyViewSet(ModelViewSet):
            """
            ---
            list:
                param: my param
            """
            serializer_class = CommentSerializer
            model = User

        # Test a list endpoint
        introspector = ViewSetIntrospector(
            MyViewSet,
            '/api/endpoint',
            url(r'^/api/endpoint$', MyViewSet.as_view({
                'get': 'list',
                'post': 'create'
            }))
        )
        allowed_methods = list(introspector)
        self.assertEqual(2, len(allowed_methods))
        allowed_methods = [method.get_http_method() for method in allowed_methods]
        self.assertIn('POST', allowed_methods)
        self.assertIn('GET', allowed_methods)
        self.assertIn('list', introspector.methods())
        self.assertIn('create', introspector.methods())
        introspector = APIViewMethodIntrospector(introspector, 'list')
        doc_parser = introspector.get_yaml_parser()
        self.assertEqual(doc_parser.object['param'], 'my param')

    def test_merge_parameters(self):
        class SerializedAPI(ListCreateAPIView):
            serializer_class = CommentSerializer

            def post(self, request, *args, **kwargs):
                """
                My post view with custom post parameters

                ---
                parameters:
                    - name: name
                      type: string
                      required: true
                """
                return super(SerializedAPI, self).post(request, *args, **kwargs)

        class_introspector = ViewSetIntrospector(
            SerializedAPI, '/', RegexURLResolver(r'^/$', '')
        )
        introspector = APIViewMethodIntrospector(class_introspector, 'POST')
        parser = introspector.get_yaml_parser()
        params = parser.discover_parameters(introspector)

        self.assertEqual(len(CommentSerializer().get_fields()) + 1, len(params))

    def test_replace_parameters(self):
        class SerializedAPI(ListCreateAPIView):
            serializer_class = CommentSerializer

            def post(self, request, *args, **kwargs):
                """
                My post view with custom post parameters

                ---
                parameters_strategy: replace
                parameters:
                    - name: name
                      type: string
                      required: true
                """
                return super(SerializedAPI, self).post(request, *args, **kwargs)

        class_introspector = ViewSetIntrospector(
            SerializedAPI, '/', RegexURLResolver(r'^/$', '')
        )
        introspector = APIViewMethodIntrospector(class_introspector, 'POST')
        parser = introspector.get_yaml_parser()
        params = parser.discover_parameters(introspector)

        self.assertEqual(1, len(params))

    def test_omit_parameters(self):
        class SerializedAPI(ListCreateAPIView):
            serializer_class = CommentSerializer

            def post(self, request, *args, **kwargs):
                """
                My post view with custom post parameters

                ---
                omit_parameters:
                    - form
                parameters:
                    - name: name
                      type: string
                      required: true
                """
                return super(SerializedAPI, self).post(request, *args, **kwargs)

        class_introspector = ViewSetIntrospector(
            SerializedAPI, '/', RegexURLResolver(r'^/$', '')
        )
        introspector = APIViewMethodIntrospector(class_introspector, 'POST')
        parser = introspector.get_yaml_parser()
        params = parser.discover_parameters(introspector)

        self.assertEqual(0, len(params))

    def test_complex_parameters_strategy(self):
        class SerializedAPI(ListCreateAPIView):
            serializer_class = CommentSerializer

            def get(self, request, *args, **kwargs):
                """
                My list view with custom query parameters

                ---
                parameters_strategy:
                    form: replace
                    query: merge
                parameters:
                    - name: search
                      type: string
                      required: true
                      paramType: query
                    - name: foo
                      paramType: form
                """
                return super(SerializedAPI, self).post(request, *args, **kwargs)

        class_introspector = ViewSetIntrospector(
            SerializedAPI, '/', RegexURLResolver(r'^/$', '')
        )
        introspector = APIViewMethodIntrospector(class_introspector, 'GET')
        parser = introspector.get_yaml_parser()
        params = introspector.build_form_parameters()
        self.assertEqual(len(CommentSerializer().get_fields()), len(params))

        params = parser.discover_parameters(introspector)
        self.assertEqual(2, len(params))
        query_params = parser._filter_params(params, 'paramType', 'query')
        form_params = parser._filter_params(params, 'paramType', 'form')
        self.assertEqual(1, len(list(query_params)))
        self.assertEqual(1, len(list(form_params)))

    def test_response_messages(self):
        class SerializedAPI(ListCreateAPIView):
            serializer_class = CommentSerializer

            def post(self, request, *args, **kwargs):
                """
                ---
                responseMessages:
                    - code: 403
                      message: Not authorized.
                    - code: 404
                      message: Not found.
                """
                return super(SerializedAPI, self).post(request, *args, **kwargs)

        class_introspector = ViewSetIntrospector(
            SerializedAPI, '/', RegexURLResolver(r'^/$', '')
        )
        introspector = APIViewMethodIntrospector(class_introspector, 'POST')
        parser = introspector.get_yaml_parser()
        messages = parser.get_response_messages()

        self.assertEqual(2, len(messages))
        self.assertEqual(messages[0]['message'], 'Not authorized.')
        self.assertEqual(messages[1]['message'], 'Not found.')

    def test_custom_serializer(self):
        class SerializedAPI(ListCreateAPIView):
            serializer_class = CommentSerializer

            def post(self, request, *args, **kwargs):
                """
                ---
                serializer: serializers.Serializer
                """
                return super(SerializedAPI, self).post(request, *args, **kwargs)

        class_introspector = ViewSetIntrospector(
            SerializedAPI, '/', RegexURLResolver(r'^/$', '')
        )
        introspector = APIViewMethodIntrospector(class_introspector, 'POST')
        generator = DocumentationGenerator()
        serializer = generator._get_method_serializer(introspector)
        self.assertTrue(serializer, serializers.Serializer)

        DocumentationGenerator.explicit_serializers.clear()

    def test_fbv_custom_serializer_explicit(self):

        @api_view(['POST'])
        def SerializedAPI2(request):
            """
            ---
            serializer: rest_framework_swagger.tests.CommentSerializer
            """
            return "blarg"

        class_introspector = WrappedAPIViewIntrospector(
            func_to_wrapper(SerializedAPI2), '/', RegexURLResolver(r'^/$', '')
        )
        introspector = WrappedAPIViewMethodIntrospector(class_introspector, 'POST')
        generator = DocumentationGenerator()
        serializer = generator._get_method_serializer(introspector)
        self.assertEqual(serializer, CommentSerializer)

    def test_fbv_custom_serializer_relative1(self):

        @api_view(['POST'])
        def SerializedAPI2(request):
            """
            ---
            serializer: ..tests.CommentSerializer
            """
            return "blarg"

        class_introspector = WrappedAPIViewIntrospector(
            SerializedAPI2.cls, '/', RegexURLResolver(r'^/$', '')
        )
        wrapper_to_func(SerializedAPI2.cls)
        introspector = WrappedAPIViewMethodIntrospector(class_introspector, 'POST')
        generator = DocumentationGenerator()
        serializer = generator._get_method_serializer(introspector)
        self.assertEqual(serializer, CommentSerializer)

    def test_fbv_custom_serializer(self):

        @api_view(['POST'])
        def SerializedAPI2(request):
            """
            ---
            serializer: CommentSerializer
            """
            return "blarg"

        class_introspector = WrappedAPIViewIntrospector(
            SerializedAPI2.cls, '/', RegexURLResolver(r'^/$', '')
        )
        wrapper_to_func(SerializedAPI2.cls)
        introspector = WrappedAPIViewMethodIntrospector(class_introspector, 'POST')
        generator = DocumentationGenerator()
        serializer = generator._get_method_serializer(introspector)
        self.assertEqual(serializer, CommentSerializer)

    def test_fbv_custom_serializer_noisy_fail(self):

        @api_view(['POST'])
        def SerializedAPI2(request):
            """
            ---
            serializer: HonkSerializer
            """
            return "blarg"

        class_introspector = WrappedAPIViewIntrospector(
            SerializedAPI2.cls, '/', RegexURLResolver(r'^/$', '')
        )
        wrapper_to_func(SerializedAPI2.cls)
        introspector = WrappedAPIViewMethodIntrospector(class_introspector, 'POST')
        generator = DocumentationGenerator()
        try:
            generator._get_method_serializer(introspector)
        except Exception as e:
            self.assertTrue("Could not find HonkSerializer" in str(e))
        else:
            self.assertTrue(False)

    def test_omit_serializer(self):
        class SerializedAPI(ListCreateAPIView):
            serializer_class = CommentSerializer

            def post(self, request, *args, **kwargs):
                """
                ---
                omit_serializer: true
                """
                return super(SerializedAPI, self).post(request, *args, **kwargs)

        class_introspector = ViewSetIntrospector(
            SerializedAPI, '/', RegexURLResolver(r'^/$', '')
        )
        introspector = APIViewMethodIntrospector(class_introspector, 'POST')
        generator = DocumentationGenerator()
        serializer = generator._get_method_serializer(introspector)
        self.assertEqual(serializer, None)

    def test_custom_response_class(self):
        class SerializedAPI(ListCreateAPIView):
            serializer_class = CommentSerializer

            def post(self, request, *args, **kwargs):
                """
                ---
                type:
                  name:
                    required: true
                    type: string
                  url:
                    required: false
                    type: url
                """
                return super(SerializedAPI, self).post(request, *args, **kwargs)

        class_introspector = ViewSetIntrospector(
            SerializedAPI, '/', RegexURLResolver(r'^/$', '')
        )
        introspector = APIViewMethodIntrospector(class_introspector, 'POST')
        parser = introspector.get_yaml_parser()
        generator = DocumentationGenerator()
        serializer = generator._get_method_serializer(introspector)
        response_class = generator._get_method_response_type(
            parser, serializer, class_introspector, introspector)

        self.assertEqual(response_class, 'SerializedAPIPostResponse')
        self.assertEqual(serializer, None)
        self.assertIn('SerializedAPIPostResponse',
                      generator.explicit_response_types)

    def test_fbv_notes(self):

        @api_view(["POST"])
        def a_view(request):
            """
            Slimy toads
            """
            return "blarg"

        class_introspector = WrappedAPIViewIntrospector(
            func_to_wrapper(a_view), '/', RegexURLResolver(r'^/$', '')
        )

        notes = class_introspector.get_notes()
        self.assertEqual(notes, "Slimy toads")
        introspector = WrappedAPIViewMethodIntrospector(class_introspector, 'POST')

        notes = introspector.get_notes()

        self.assertEqual(notes, "Slimy toads")
