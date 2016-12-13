from django.test import TestCase
from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from rest_framework_swagger import renderers
from rest_framework_swagger.views import get_swagger_view

from .compat.mock import patch


class TestGetSwaggerView(TestCase):
    def setUp(self):
        self.sut = get_swagger_view
        self.factory = APIRequestFactory()
        self.view_class = self.sut().cls

    def test_title_and_urlpassed_to_schema_generator(self):
        title = 'Vandelay'
        url = 'https://github.com/marcgibbons/django-rest-swagger'
        urlconf = 'fizz'
        patterns = []
        view = self.sut(
            title=title,
            url=url,
            patterns=patterns,
            urlconf=urlconf
        )

        with patch('rest_framework_swagger.views.SchemaGenerator') as mock:
            request = self.factory.get('/')
            view(request=request)

        mock.assert_called_once_with(
            title=title,
            url=url,
            patterns=patterns,
            urlconf=urlconf
        )

    def test_ignore_model_permissions_true(self):
        self.assertTrue(self.view_class._ignore_model_permissions)

    def test_exclude_from_schema(self):
        self.assertTrue(self.view_class.exclude_from_schema)

    def test_renderer_classes(self):
        self.assertListEqual(
            [
                CoreJSONRenderer,
                renderers.OpenAPIRenderer,
                renderers.SwaggerUIRenderer
            ],
            self.view_class.renderer_classes
        )

    def test_permission_class(self):
        self.assertListEqual(
            [AllowAny],
            self.view_class.permission_classes
        )

    def test_return_400_if_schema_is_none(self):
        with patch('rest_framework_swagger.views.SchemaGenerator') as mock:
            mock.return_value.get_schema.return_value = None
            request = self.factory.get('/')
            response = self.sut()(request=request)

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            ['The schema generator did not return a schema Document'],
            response.data
        )

    def test_response_is_result_of_schema_generator(self):
        expected = 'My amazing schema'
        with patch('rest_framework_swagger.views.SchemaGenerator') as mock:
            mock.return_value.get_schema.return_value = expected
            request = self.factory.get('/')
            response = self.sut()(request=request)

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.data)

    def test_schema_generator_instantiated_with_request(self):
        with patch('rest_framework_swagger.views.SchemaGenerator') as mock:
            request = self.factory.get('/')
            self.sut()(request=request)

        call_args = mock.return_value.get_schema.call_args[1]
        self.assertIn('request', call_args)
        self.assertIsInstance(call_args['request'], Request)
