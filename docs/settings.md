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
    }
}
```

## Authentication
#### USE_SESSION_AUTH
Toggles the use of Django Auth as an authentication mechanism. Setting it to `True` will display
a login/logout button on the Swagger UI and post csrf_tokens to the API.

Default: `True`


**Note:** The login/logout button relies on Django's `LOGIN_URL` and `LOGOUT_URL` settings which defaults to `/accounts/login`. Here's an example of how to configure using DRF's authentication endpoints.

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

#### SECURITY_DEFINITIONS
The security definitions configures which authentication methods can be used by Swagger. The schemes types currently supported by the OpenAPI 2.0 spec are `basic`, `apiKey` and `oauth2`.

For more information on available options, please consult the OpenAPI [Security Object Definition](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#security-definitions-object)

Default: 
```python
{
    'basic': {
        'type': 'basic'
    }
}
```
