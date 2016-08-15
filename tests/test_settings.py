from django.conf import settings
from django.test import override_settings, TestCase
from rest_framework_swagger import settings as swagger_settings


class TestSettings(TestCase):
    def setUp(self):
        self.sut = swagger_settings

    def test_import_string(self):
        self.assertEqual([], self.sut.IMPORT_STRINGS)

    @override_settings(SWAGGER_SETTINGS={'SECURITY_DEFINITIONS': None})
    def test_settings_when_none(self):
        self.assertIsNone(self.sut.swagger_settings.SECURITY_DEFINITIONS)


class TestDefaults(TestCase):
    def setUp(self):
        self.sut = swagger_settings.DEFAULTS

    def test_login_url(self):
        self.assertEqual(
            getattr(settings, 'LOGIN_URL', None),
            self.sut['LOGIN_URL']
        )

    def test_logout_url(self):
        self.assertEqual(
            getattr(settings, 'LOGOUT_URL', None),
            self.sut['LOGOUT_URL']
        )

    def test_use_session_auth(self):
        self.assertIs(True, self.sut['USE_SESSION_AUTH'])

    def test_security_definitions(self):
        self.assertDictEqual(
            {'basic': {'type': 'basic'}},
            self.sut['SECURITY_DEFINITIONS']
        )

    def test_operations_sorter(self):
        self.assertIsNone(self.sut['OPERATIONS_SORTER'])

    def test_show_request_headers(self):
        self.assertIs(False, self.sut['SHOW_REQUEST_HEADERS'])

    def test_validator_url(self):
        self.assertEqual('', self.sut['VALIDATOR_URL'])

    def test_json_editor(self):
        self.assertIs(False, self.sut['JSON_EDITOR'])

    def test_doc_expansion(self):
        self.assertIsNone(self.sut['DOC_EXPANSION'])
