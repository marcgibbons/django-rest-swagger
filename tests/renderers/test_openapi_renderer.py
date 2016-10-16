import coreapi
from coreapi.compat import force_bytes
from django.test import TestCase
from rest_framework_swagger import renderers
import simplejson as json

from ..compat.mock import MagicMock, patch


class TestOpenAPICodec(TestCase):
    def setUp(self):
        self.sut = renderers.OpenAPICodec().encode

    def test_encode_without_document_instance_raises_assertion_error(self):
        """
        Given that the data is not a CoreAPI Document instance,
        an assertion error should be raised.
        """
        with self.assertRaises(TypeError) as cx:
            data = MagicMock()
            self.sut(data)

        expected = 'Expected a `coreapi.Document` instance'
        self.assertEqual(expected, str(cx.exception))

    def test_encode_generates_swagger_object_when_given_valid_document(self):
        expected = {'fizz': 'buzz'}
        with patch(
            'rest_framework_swagger.renderers.generate_swagger_object',
            return_value={'fizz': 'buzz'}
        ):
            result = self.sut(coreapi.Document())

        self.assertEqual(force_bytes(json.dumps(expected)), result)

    def test_encode_adds_extra_data_provided_to_swagger_object(self):
        expected = {'foo': 'bar'}
        with patch(
            'rest_framework_swagger.renderers.generate_swagger_object',
            return_value={}
        ):
            result = self.sut(coreapi.Document(), extra=expected)

        self.assertEqual(force_bytes(json.dumps(expected)), result)


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

    @patch('rest_framework_swagger.renderers.OpenAPICodec.encode')
    def test_render_encodes_customizations(self, encode_mock):
        data = coreapi.Document()
        renderer_context = {
            'request': MagicMock(),
            'response': MagicMock(status_code=200)
        }
        with patch.object(self.sut, 'get_customizations') as mock:
            self.sut.render(data, renderer_context=renderer_context)

        encode_mock.assert_called_once_with(data, extra=mock.return_value)

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


class TestGetCustomizations(TestCase):
    def setUp(self):
        self.sut = renderers.OpenAPIRenderer().get_customizations

        settings_patcher = patch(
            'rest_framework_swagger.renderers.swagger_settings'
        )
        self.swagger_settings = settings_patcher.start()
        self.addCleanup(settings_patcher.stop)

    def test_security_definitions_included_when_defined(self):
        self.swagger_settings.SECURITY_DEFINITIONS = {'foo': 'bar'}
        expected = {
            'securityDefinitions': self.swagger_settings.SECURITY_DEFINITIONS
        }
        self.assertDictContainsSubset(expected, self.sut())

    def test_security_definitions_not_present_when_none(self):
        self.swagger_settings.SECURITY_DEFINITIONS = None
        self.assertNotIn('securityDefinitions', self.sut())
