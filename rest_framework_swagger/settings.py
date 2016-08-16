from django.conf import settings
from django.test.signals import setting_changed
from rest_framework.settings import APISettings


DEFAULTS = {
    'USE_SESSION_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
    'LOGIN_URL': getattr(settings, 'LOGIN_URL', None),
    'LOGOUT_URL': getattr(settings, 'LOGOUT_URL', None),
    'DOC_EXPANSION': None,
    'APIS_SORTER': None,
    'OPERATIONS_SORTER': None,
    'JSON_EDITOR': False,
    'SHOW_REQUEST_HEADERS': False,
    'SUPPORTED_SUBMIT_METHODS': [
        'get',
        'post',
        'put',
        'delete',
        'patch'
    ],
    'VALIDATOR_URL': '',
}

IMPORT_STRINGS = []

swagger_settings = APISettings(
    user_settings=getattr(settings, 'SWAGGER_SETTINGS', {}),
    defaults=DEFAULTS,
    import_strings=IMPORT_STRINGS
)


def reload_settings(*args, **kwargs):  # pragma: no cover
    """
    Reloads settings during unit tests if override_settings decorator
    is used. (Taken from DRF)
    """
    # pylint: disable=W0603
    global swagger_settings

    if kwargs['setting'] == 'LOGIN_URL':
        swagger_settings.LOGIN_URL = kwargs['value']
    if kwargs['setting'] == 'LOGOUT_URL':
        swagger_settings.LOGOUT_URL = kwargs['value']
    if kwargs['setting'] != 'SWAGGER_SETTINGS':
        return

    swagger_settings = APISettings(
        kwargs['value'],
        DEFAULTS,
        IMPORT_STRINGS
    )


setting_changed.connect(reload_settings)
