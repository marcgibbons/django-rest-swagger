# Settings
The configuration of Django REST Swagger is identical to Django REST Framework. Settings are configurable in `settings.py` by defining `SWAGGER_SETTINGS`.

Example:

**settings.py**
```python
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
    ...
}
```

## Authentication
### USE_SESSION_AUTH
Toggles the use of Django Auth as an authentication mechanism. Setting it to `True` will display
a login/logout button on the Swagger UI and post csrf_tokens to the API.

**Default:** `True`


**Note:** The login/logout button relies on the `LOGIN_URL` and `LOGOUT_URL` settings which default to `/accounts/login`. These can either be configured under `SWAGGER_SETTINGS` or Django settings.

**urls.py**
```python
urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
```
**settings.py**
```python
LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'
```

### LOGIN_URL
The URL to use to log in session authentication. Accepts named URL patterns.

**Default:** `django.conf.settings.LOGIN_URL`


### LOGOUT_URL
The URL to use to log out of session authentication. Accepts named URL patterns.

**Default:** `django.conf.settings.LOGOUT_URL`


### SECURITY_DEFINITIONS
The security definitions configures which authentication methods can be used by Swagger. The schemes types currently supported by the OpenAPI 2.0 spec are `basic`, `apiKey` and `oauth2`.

For more information on available options, please consult the OpenAPI [Security Object Definition](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#security-definitions-object).

**Default:** 
```python
{
    'basic': {
        'type': 'basic'
    }
}
```
