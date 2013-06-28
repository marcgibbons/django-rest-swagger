from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

VERSION = '0.1.1'

DEFAULT_SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': '',
    'api_key': '',
    'enabled_methods': ['get', 'post', 'put', 'patch', 'delete']
}

try:
    SWAGGER_SETTINGS = getattr(settings, 'SWAGGER_SETTINGS', DEFAULT_SWAGGER_SETTINGS)

    for key, value in DEFAULT_SWAGGER_SETTINGS.items():
        if key not in SWAGGER_SETTINGS:
            SWAGGER_SETTINGS[key] = value

except ImproperlyConfigured:
    SWAGGER_SETTINGS = DEFAULT_SWAGGER_SETTINGS

