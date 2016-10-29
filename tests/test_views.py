from django.test import TestCase
from rest_framework import schemas
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.test import APIRequestFactory

from rest_framework_swagger import renderers
from rest_framework_swagger.views import get_swagger_view

from .compat.mock import patch


class TestGetSwaggerView(TestCase):
    def setUp(self):
        self.sut = get_swagger_view
        self.factory = APIRequestFactory()
        self.view_class = self.sut().cls

    def test_returns_get_schema_view(self):
        title = 'Vandelay Industries API',
        url = 'http://vandelay.industries'
        renderer_classes = [
            CoreJSONRenderer,
            renderers.OpenAPIRenderer,
            renderers.SwaggerUIRenderer
        ]

        with patch.object(schemas, 'get_schema_view') as mock:
            result = self.sut(title=title, url=url)

        mock.assert_called_once_with(
            title=title,
            url=url,
            renderer_classes=renderer_classes
        )

        self.assertEqual(mock.return_value, result)
