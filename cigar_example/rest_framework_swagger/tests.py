from django.conf.urls import patterns, url, include
from django.test import TestCase
from urlparser import UrlParser

from django.views.generic import View
from rest_framework.views import APIView


class MockApiView(APIView):
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

        self.assertTrue(isinstance(callback, MockApiView))

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
