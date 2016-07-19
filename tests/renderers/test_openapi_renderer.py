from unittest import TestCase
from rest_framework_swagger import renderers

from ..compat import mock


class OpenAPIRendererTestCase(TestCase):
    def setUp(self):
        self.sut = renderers.OpenAPIRenderer()

    def test_media_type(self):
        self.assertEqual(
            'application/openapi+json',
            self.sut.media_type
        )

    def test_charset(self):
        self.assertIsNone(self.sut.charset)

    def test_format(self):
        self.assertEqual('openapi', self.sut.format)

    @mock.patch('openapi_codec.OpenAPICodec.dump')
    @mock.patch('simplejson.loads')
    def test_get_openapi_specification(self, json_mock, codec_mock):
        """
        Asserts that the returned value is a Python representation
        of the OpenAPICodec's `dump` method.
        """
        data = {'foo': 'bar'}
        self.sut.get_openapi_specification(data)

        codec_mock.assert_called_once_with(data)
        json_mock.assert_called_once_with(codec_mock.return_value)
