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
        'permission_denied_handler': None, 
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

token_type
----------

Overrides authorization token type.

Default: :code:`'Token'`
