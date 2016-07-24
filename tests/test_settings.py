from unittest import TestCase

from django.conf import settings
from django.test import override_settings
from rest_framework_swagger import settings as swagger_settings


class TestSettings(TestCase):
    def setUp(self):
        self.sut = swagger_settings

    def test_defaults(self):
        self.assertDictEqual(
            {
                'USE_SESSION_AUTH': True,
                'SECURITY_DEFINITIONS': {
                    'basic': {
                        'type': 'basic'
                    }
                },
                'LOGIN_URL': getattr(settings, 'LOGIN_URL', None),
                'LOGOUT_URL': getattr(settings, 'LOGOUT_URL', None)
            },
            self.sut.DEFAULTS
        )

    def test_import_string(self):
        self.assertEqual([], self.sut.IMPORT_STRINGS)

    @override_settings(SWAGGER_SETTINGS={'SECURITY_DEFINITIONS': None})
    def test_settings_when_none(self):
        self.assertIsNone(self.sut.swagger_settings.SECURITY_DEFINITIONS)
