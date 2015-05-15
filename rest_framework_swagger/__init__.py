VERSION = '0.3.0'

DEFAULT_SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': '',
    'api_path': '/',
    'api_key': '',
    'token_type': 'Token',
    'enabled_methods': ['get', 'post', 'put', 'patch', 'delete'],
    'is_authenticated': False,
    'is_superuser': False,
    'permission_denied_handler': None,
    'template_path': 'rest_framework_swagger/index.html',
    'doc_expansion': 'none',
}

try:
    from django.conf import settings
    SWAGGER_SETTINGS = getattr(settings, 'SWAGGER_SETTINGS', DEFAULT_SWAGGER_SETTINGS)

    for key, value in DEFAULT_SWAGGER_SETTINGS.items():
        if key not in SWAGGER_SETTINGS:
            SWAGGER_SETTINGS[key] = value

except:
    SWAGGER_SETTINGS = DEFAULT_SWAGGER_SETTINGS
