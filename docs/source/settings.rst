SWAGGER_SETTINGS
========================

A dictionary containing all configuration of django-rest-swagger.

Example:

.. code-block:: python

    SWAGGER_SETTINGS = {
        'exclude_namespaces': [],
        'api_version': '0.1',
        'api_path': '/',
        'enabled_methods': [
            'get',
            'post',
            'put',
            'patch',
            'delete'
        ],
        'api_key': '',
        'is_authenticated': False,
        'is_superuser': False,
        'unauthenticated_user': 'django.contrib.auth.models.AnonymousUser',
        'permission_denied_handler': None,
        'resource_access_handler': None,
        'base_path':'helloreverb.com/docs',
        'info': {
            'contact': 'apiteam@wordnik.com',
            'description': 'This is a sample server Petstore server. '
                           'You can find out more about Swagger at '
                           '<a href="http://swagger.wordnik.com">'
                           'http://swagger.wordnik.com</a> '
                           'or on irc.freenode.net, #swagger. '
                           'For this sample, you can use the api key '
                           '"special-key" to test '
                           'the authorization filters',
            'license': 'Apache 2.0',
            'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
            'termsOfServiceUrl': 'http://helloreverb.com/terms/',
            'title': 'Swagger Sample App',
        },
        'doc_expansion': 'none',
    }

api_version
------------------------

version of your api.

Defaults to :code:`''`

api_path
------------------------
path to your api. url protocol and domain is taken from django settings, so do not include those in here.

Defaults to :code:`'/'`

api_key
------------------------

an api key

Defaults to :code:`''`

base_path
-----------------------

the url to where your main Swagger documentation page will live without the protocol. Optional.

If not provided, it will generate the base_path from the :code:`request.get_host()` method.

doc_expansion
-----------------------

The docExpansion parameter as defined in the Swagger UI spec. Potential values include "none", "list", or "full".

Defaults to :code:`'none'`


enabled_methods
-----------------------

The methods that can be interacted with in the UI

Default: :code:`['get', 'post', 'put', 'patch', 'delete']`

exclude_namespaces
------------------------

list URL namespaces to ignore

Default: :code:`[]`

info
-----------------------

specify the info object per
 https://github.com/swagger-api/swagger-spec/blob/master/versions/1.2.md#513-info-object

is_authenticated
------------------------

set to True to enforce user authentication

Default: :code:`False`

is_superuser
------------------------

set to True to enforce admin only access

Default: :code:`False`

unauthenticated_user
-------------------------

Sets the class that is used for the user in unauthenticated requests.

set to None to specify no user class

Default: :code:`django.contrib.auth.models.AnonymousUser`

permission_denied_handler
-------------------------

custom handler for permission denied on attempting to access swagger.

Takes a callable or a string that names a callable.

Default: :code:`None`

Example:

.. code-block:: python

    SWAGGER_SETTINGS = {
        'permission_denied_handler': 'app.views.permission_denied_handler'
    }

Then in app/views.py:

.. code-block:: python

    def permission_denied_handler(request):
        from django.http import HttpResponse
        return HttpResponse('you have no permissions!')

resource_access_handler
-------------------------

custom handler for delegating access rules to the project.

Takes a callable or a string that names a callable with the following signature:

.. code-block:: python

    def resource_access_handler(request, resource)

The handler must accept the following arguments:
    `request` (django.http.HttpRequest): The request for documentation, providing the user and any
        other relevant details about the user who is making the HTTP request.
    `resource` (str): The path to the API endpoint for which to approve or reject authorization. Does not have
        leading/trailing slashes.

The handler should return a truthy value when the resource is accessible in the context of the current request.

Default: :code:`None`

Example:

.. code-block:: python

    SWAGGER_SETTINGS = {
        'resource_access_handler': 'app.views.resource_access_handler'
    }

Then in app/views.py:

.. code-block:: python

    from django.core.urlresolvers import resolve

    from .flags import flag_is_active


    def resource_access_handler(request, resource):
        """ Callback for resource access. Determines who can see the documentation for which API. """
        # Superusers and staff can see whatever they want
        if request.user.is_superuser or request.user.is_staff:
            return True
        else:
            if isinstance(resource, basestring):
                try:
                    resolver_match = resolve('/{}/'.format(resource))
                    view = resolver_match.func
                except Exception:
                    return False
            else:
                view = resource.callback

            view_attributes = view.func_dict
            feature_flag = view_attributes.get('feature_flag')

            # Hide documentation for disabled features
            if feature_flag and not flag_is_active(request, feature_flag):
                return False
            else:
                return True

token_type
----------

Overrides authorization token type.

Default: :code:`'Token'`
