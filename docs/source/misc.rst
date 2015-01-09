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
