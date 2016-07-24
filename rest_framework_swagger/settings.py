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
    'LOGOUT_URL': getattr(settings, 'LOGOUT_URL', None)
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
    if kwargs['setting'] != 'SWAGGER_SETTINGS':
        return

    # pylint: disable=W0603
    global swagger_settings
    swagger_settings = APISettings(
        kwargs['value'],
        DEFAULTS,
        IMPORT_STRINGS
    )


setting_changed.connect(reload_settings)
