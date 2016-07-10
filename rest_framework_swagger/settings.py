from django.conf import settings
from rest_framework.settings import APISettings


DEFAULTS = {
    'USE_SESSION_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    }
}

IMPORT_STRINGS = []

swagger_settings = APISettings(
    user_settings=getattr(settings, 'SWAGGER_SETTINGS', {}),
    defaults=DEFAULTS,
    import_strings=IMPORT_STRINGS
)
