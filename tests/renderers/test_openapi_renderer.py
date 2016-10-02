import coreapi
from django.test import TestCase
from rest_framework_swagger import renderers

from ..compat.mock import MagicMock, patch


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

    @patch('openapi_codec.OpenAPICodec.encode')
    def test_render(self, encode_mock):
        data = coreapi.Document()
        renderer_context = {
            'request': MagicMock(),
            'response': MagicMock(status_code=200)
        }
        with patch.object(self.sut, 'get_document') as mock:
            result = self.sut.render(data, renderer_context=renderer_context)

        mock.assert_called_once_with(data, renderer_context)
        encode_mock.assert_called_once_with(mock.return_value)
        self.assertEqual(result, encode_mock.return_value)

    def test_render_if_response_is_not_200(self):
        """
        Given the response returned in the renderer_context has a status
        code other than 200, the data should be dumped.
        """
        data = {'error': 'fizz buzz'}
        renderer_context = {'response': MagicMock(status_code=403)}
        result = self.sut.render(data, renderer_context=renderer_context)
        expected = renderers.JSONRenderer().render(data)

        self.assertEqual(expected, result)

    def test_render_raises_assertion_error(self):
        """
        Given that the data is not a CoreAPI Document instance,
        an assertion error should be raised.
        """
        renderer_context = {
            'request': MagicMock(),
            'response': MagicMock(status_code=200)
        }
        with self.assertRaises(AssertionError) as cx:
            data = MagicMock()
            self.sut.render(data, renderer_context=renderer_context)

        expected = (
            'Expected a coreapi.Document, but received %s instead.' %
            type(data)
        )
        self.assertEqual(expected, str(cx.exception))


class TestGetDocument(TestCase):
    def setUp(self):
        self.data = coreapi.Document(
            title='Vandelay Inustries',
            url='http://seinfeld.wikia.com/wiki/Vandelay_Industries',
            content={'fizz': 'buzz'}
        )
        self.renderer_context = MagicMock()

        self.customizations = {'foo': 'bar'}

        def add_customizations(data, renderer_context):
            data.update(self.customizations)

        with patch.object(
            renderers.OpenAPIRenderer,
            'add_customizations',
            side_effect=add_customizations
        ) as self.add_customizations_mock:
            self.sut = renderers.OpenAPIRenderer().get_document(
                data=self.data,
                renderer_context=self.renderer_context
            )

    def test_document_title(self):
        self.assertEqual(self.data.title, self.sut.title)

    def test_document_url(self):
        self.assertEqual(self.data.url, self.sut.url)

    def test_add_customizations_called(self):
        expected = dict(self.data, **self.customizations)
        self.add_customizations_mock.assert_called_once_with(
            expected,
            self.renderer_context
        )

        self.assertDictEqual(expected, dict(self.sut.data))


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
