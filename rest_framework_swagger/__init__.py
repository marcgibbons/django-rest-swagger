from django.conf import settings

VERSION = '0.1.0'

DEFAULT_SWAGGER_SETTINGS = {
    'exclude_namespaces': None,
    'api_version': '',
    'api_key': '',
    'enabled_methods': ['get', 'post', 'put', 'patch', 'delete']
}

SWAGGER_SETTINGS = getattr(settings, 'SWAGGER_SETTINGS', DEFAULT_SWAGGER_SETTINGS)

for key, value in DEFAULT_SWAGGER_SETTINGS.items():
    if key not in SWAGGER_SETTINGS:
        SWAGGER_SETTINGS[key] = value
