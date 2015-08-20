VERSION = '0.3.4'

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
    'resource_access_handler': None,
    'template_path': 'rest_framework_swagger/index.html',
    'doc_expansion': 'none',
}

try:
    from django.conf import settings
    from django.test.signals import setting_changed

    def load_settings(provided_settings):
        global SWAGGER_SETTINGS
        SWAGGER_SETTINGS = provided_settings

        for key, value in DEFAULT_SWAGGER_SETTINGS.items():
            if key not in SWAGGER_SETTINGS:
                SWAGGER_SETTINGS[key] = value

    def reload_settings(*args, **kwargs):
        setting, value = kwargs['setting'], kwargs['value']
        if setting == 'SWAGGER_SETTINGS':
            load_settings(value)

    load_settings(getattr(settings,
                          'SWAGGER_SETTINGS',
                          DEFAULT_SWAGGER_SETTINGS))
    setting_changed.connect(reload_settings)

except:
    SWAGGER_SETTINGS = DEFAULT_SWAGGER_SETTINGS
