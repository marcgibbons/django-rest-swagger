from django.test import TestCase
from rest_framework_swagger import renderers

from ..compat.mock import DEFAULT, MagicMock, patch


class TestOpenAPIRenderer(TestCase):
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

    def test_render(self):
        data = MagicMock()
        renderer_context = {'request': MagicMock()}

        with patch.multiple(
            self.sut,
            get_openapi_specification=DEFAULT,
            add_customizations=DEFAULT,
            dump=DEFAULT
        ) as values:
            self.sut.render(data, renderer_context=renderer_context)

        values['get_openapi_specification'].assert_called_once_with(data)
        data = values['get_openapi_specification'].return_value
        values['add_customizations'].assert_called_once_with(
            data,
            renderer_context
        )
        values['dump'].assert_called_once_with(data)

    @patch('rest_framework_swagger.renderers.force_bytes')
    @patch('simplejson.dumps')
    def test_dump(self, json_mock, bytes_mock):
        data = MagicMock()
        result = self.sut.dump(data)

        json_mock.assert_called_once_with(data)
        bytes_mock.assert_called_once_with(json_mock.return_value)

        self.assertEqual(bytes_mock.return_value, result)

    @patch('openapi_codec.OpenAPICodec.dump')
    @patch('simplejson.loads')
    def test_get_openapi_specification(self, json_mock, codec_mock):
        """
        Asserts that the returned value is a Python representation
        of the OpenAPICodec's `dump` method.
        """
        data = {'foo': 'bar'}
        self.sut.get_openapi_specification(data)

        codec_mock.assert_called_once_with(data)
        json_mock.assert_called_once_with(codec_mock.return_value)


class TestAddSecurityDefinitons(TestCase):
    def setUp(self):
        self.sut = renderers.OpenAPIRenderer()

        settings_patcher = patch(
            'rest_framework_swagger.renderers.swagger_settings'
        )
        self.swagger_settings = settings_patcher.start()
        self.addCleanup(settings_patcher.stop)

    def test_add_customizations_adds_security_definitions(self):
        data = MagicMock()
        renderer_context = {'request': MagicMock()}
        with patch.object(self.sut, 'add_security_definitions') as mock:
            self.sut.add_customizations(data, renderer_context)

        mock.assert_called_once_with(data)

    def test_add_security_definitions_when_none(self):
        """
        Given that SECURITY_DEFINITIONS is set to None, security definitions
        should not be added.
        """
        data = {}
        self.swagger_settings.SECURITY_DEFINITIONS = None
        self.sut.add_security_definitions(data)
        self.assertNotIn('securityDefinitions', data)

    def test_add_security_definitions_when_defined(self):
        """
        Given that SECURITY_DEFINITIONS is defined, the value should be
        added to the data dictionary.
        """
        data = {}
        expected = {'foo': 'bar'}
        self.swagger_settings.SECURITY_DEFINITIONS = expected
        self.sut.add_security_definitions(data)

        self.assertDictContainsSubset(
            {'securityDefinitions': expected},
            data
        )


class TestAddRequestHost(TestCase):
    def setUp(self):
        self.sut = renderers.OpenAPIRenderer()

    def test_add_customizations_sets_hosts_when_falsey(self):
        """
        Given that the `host` on the OpenAPI spec is falsey,
        the host from the renderer's view request should be used as
        the value for this property.
        """
        data = {'host': ''}
        with patch.object(self.sut, 'get_host') as mock:
            self.sut.add_customizations(data, renderer_context=MagicMock())

        self.assertEqual(mock.return_value, data['host'])

    def test_add_customizations_preserves_host_when_truthy(self):
        """
        Given that the `host` is already specified on the OpenAPI spec,
        this value should be preserved.
        """
        data = {'host': 'vandelayindustries.com'}
        with patch.object(self.sut, 'get_host') as mock:
            self.sut.add_customizations(data, renderer_context=MagicMock())
        mock.assert_not_called()

        self.assertEqual('vandelayindustries.com', data['host'])

    def test_get_host(self):
        expected = 'kramerica.org'
        request = MagicMock()
        request.get_host.return_value = expected

        renderer_context = {'request': request}
        result = self.sut.get_host(renderer_context)

        self.assertEqual(expected, result)
