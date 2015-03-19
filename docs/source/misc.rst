Miscellaneous
=============
Markdown
--------

django-rest-swagger will parse docstrings as markdown if `Markdown <https://pypi.python.org/pypi/Markdown>`_ is installed.

reStructuredText
-----------------
django-rest-swagger can be configured to parse docstrings as reStructuredText.

Add to your settings:

.. code-block:: python

    REST_FRAMEWORK = {
        'VIEW_DESCRIPTION_FUNCTION': 'rest_framework_swagger.views.get_restructuredtext'
    }

Swagger 'nickname' attribute
-----------------
By default, django-rest-swagger uses django-rest-framework's get_view_name to resolve the `nickname` attribute
of a Swagger operation. You can specify an alternative function for `nickname` resolution using the following setting:

.. code-block:: python

    REST_FRAMEWORK = {
        'VIEW_NAME_FUNCTION': 'module.path.to.custom.view.name.function'
    }

This function should use the following signature:

.. code-block:: python

    view_name(cls, suffix=None)

-:code:`cls` The view class providing the operation.

-:code:`suffix` The string name of the class method which is providing the operation.