from unittest import TestCase
from rest_framework_swagger.renderers import SwaggerUIRenderer

from ..compat.mock import patch, MagicMock


class TestSwaggerUIRenderer(TestCase):
    def setUp(self):
        self.sut = SwaggerUIRenderer()
        self.renderer_context = {'request': MagicMock()}

        django_settings_patcher = patch(
            'rest_framework_swagger.renderers.settings',
        )
        self.django_settings = django_settings_patcher.start()
        self.addCleanup(django_settings_patcher.stop)

        swagger_settings_patcher = patch(
            'rest_framework_swagger.renderers.swagger_settings',
        )
        self.swagger_settings = swagger_settings_patcher.start()
        self.addCleanup(swagger_settings_patcher.stop)

    def test_media_type(self):
        self.assertEqual('text/html', self.sut.media_type)

    def test_format(self):
        self.assertEqual('swagger', self.sut.format)

    def test_template(self):
        self.assertEqual(
            'rest_framework_swagger/index.html',
            self.sut.template
        )

    def test_charset(self):
        self.assertEqual('utf-8', self.sut.charset)

    @patch('rest_framework_swagger.renderers.render')
    def test_render(self, render_mock):
        with patch.object(self.sut, 'set_context') as context_mock:
            self.sut.render(
                data=None,
                accepted_media_type=None,
                renderer_context=self.renderer_context
            )

        context_mock.assert_called_once_with(self.renderer_context)
        render_mock.assert_called_once_with(
            self.renderer_context['request'],
            self.sut.template,
            self.renderer_context
        )

    def test_set_context_use_session_auth(self):
        self.sut.set_context(self.renderer_context)

        self.assertEqual(
            self.renderer_context['USE_SESSION_AUTH'],
            self.swagger_settings.USE_SESSION_AUTH
        )

    def test_set_context_sets_auth_urls(self):
        urls = {'fizz': 'buzz'}
        with patch.object(self.sut, 'get_auth_urls', return_value=urls):
            self.sut.set_context(self.renderer_context)

        self.assertDictContainsSubset(urls, self.renderer_context)

    def test_get_auth_urls(self):
        key = 'LOGIN_URL'
        value = '/foo?next=bar'
        with patch.multiple(
            self.sut,
            get_auth_url_settings=lambda *args: {key: ''},
            add_next_to_url=lambda *args: value
        ):
            self.sut.set_context(self.renderer_context)

        self.assertDictContainsSubset({key: value}, self.renderer_context)

    def test_get_auth_url_settings(self):
        self.assertDictEqual(
            {
                'LOGIN_URL': self.django_settings.LOGIN_URL,
                'LOGOUT_URL': self.django_settings.LOGOUT_URL
            },
            self.sut.get_auth_url_settings()
        )

    @patch('rest_framework_swagger.renderers.resolve_url')
    def test_add_next_to_url(self, mock):
        request = MagicMock(path='industries')
        url = '/vandelay'
        expected = '%s?next=%s' % (mock.return_value, request.path)

        self.assertEqual(expected, self.sut.add_next_to_url(url, request))
        mock.assert_called_once_with(url)
