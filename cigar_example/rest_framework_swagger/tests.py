from django.conf.urls import patterns, url, include
from django.test import TestCase
from urlparser import UrlParser
from docgenerator import DocumentationGenerator

from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView


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


class UrlParserTest(TestCase):
    def setUp(self):
        self.url_patterns = patterns('',
            url(r'a-view/?$', MockApiView.as_view(), name='a test view'),
            url(r'a-view/child/?$', MockApiView.as_view()),
            url(r'another-view/?$', MockApiView.as_view(), name='another test view'),
        )

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

        self.assertEqual(2, len(apis))

    def test_flatten_url_tree_excluded_namesapce(self):
        urls = patterns('',
            url(r'api/base/path/', include(self.url_patterns, namespace='exclude'))
        )
        urlparser = UrlParser()
        apis = urlparser.get_apis(urls, 'exclude')

        self.assertEqual([], apis)

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

        self.assertEqual(2, len(apis))


class DocumentationGeneratorTest(TestCase):
    def setUp(self):
        self.url_patterns = patterns('',
            url(r'a-view/?$', MockApiView.as_view(), name='a test view'),
            url(r'a-view/child/?$', MockApiView.as_view()),
            url(r'a-view/<pk>/?$', MockApiView.as_view(), name="detailed view for mock"),
            url(r'another-view/?$', MockApiView.as_view(), name='another test view'),
        )

    def test_generate(self):
        urlparser = UrlParser()
        apis = urlparser.get_apis(self.url_patterns, filter_path='a-view')

        generator = DocumentationGenerator()
        docs = generator.generate(apis)

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
