from unittest import TestCase

from rest_framework_swagger import renderers


class OpenAPIRendererTestCase(TestCase):
    def setUp(self):
        self.sut = renderers.OpenAPIRenderer

    def test_media_type(self):
        self.assertEqual(
            'application/openapi+json',
            self.sut.media_type
        )

    def test_charset(self):
        self.assertIsNone(self.sut.charset)

    def test_format(self):
        self.assertEqual('openapi', self.sut.format)
