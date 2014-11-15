.. django-rest-swagger documentation master file, created by
   sphinx-quickstart on Sun Nov  9 17:02:55 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django REST Swagger
===============================================

Contents:

.. toctree::
   :maxdepth: 2

   settings
   yaml
   misc
   examples

Overview
------------------

Django REST Swagger is a library that generates 
`Swagger <https://developers.helloreverb.com/swagger/>`_
documentation from you `Django Rest Framework <http://www.django-rest-framework.org/>`_ API code.

Supports `Swagger 1.2 <https://github.com/swagger-api/swagger-spec/blob/master/versions/1.2.md>`_.

Quickstart
------------------

1. Add :code:`rest_framework_swagger` to :code:`INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'rest_framework_swagger',
    )

2. Include the rest_framework_swagger URLs to a path of your choice

.. code-block:: python

    patterns = ('',
        ...
        url(r'^docs/', include('rest_framework_swagger.urls')),
    )

Further configuration can be made via :doc:`SWAGGER_SETTINGS <settings>` in your project's `settings.py`.

