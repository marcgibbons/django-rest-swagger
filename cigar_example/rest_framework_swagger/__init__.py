from django.conf import settings

DEFAULT_SWAGGER_SETTINGS = {
    'exclude_namespaces': None,
    'api_version': None,
}
SWAGGER_SETTINGS = getattr(settings, 'SWAGGER_SETTINGS', DEFAULT_SWAGGER_SETTINGS)
