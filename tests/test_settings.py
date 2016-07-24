from unittest import TestCase

from django.test import override_settings
from rest_framework_swagger import settings


class TestSettings(TestCase):
    def test_defaults(self):
        self.assertDictEqual(
            {
                'USE_SESSION_AUTH': True,
                'SECURITY_DEFINITIONS': {
                    'basic': {
                        'type': 'basic'
                    }
                }
            },
            settings.DEFAULTS
        )

    def test_import_string(self):
        self.assertEqual([], settings.IMPORT_STRINGS)

    @override_settings(SWAGGER_SETTINGS={'SECURITY_DEFINITIONS': None})
    def test_settings_when_none(self):
        self.assertIsNone(settings.swagger_settings.SECURITY_DEFINITIONS)
