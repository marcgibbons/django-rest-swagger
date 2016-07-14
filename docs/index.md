# Django REST Swagger

<iframe src="https://ghbtns.com/github-btn.html?user=marcgibbons&repo=django-rest-swagger&type=star&count=true" frameborder="0" scrolling="0" width="170px" height="20px"></iframe>


---
Django REST Swagger provides auto-generated Swagger documentation for your Django REST Framework project.

**Note:** you are viewing documentation for version 2, using Django REST Framework 3.4+ and CoreAPI. Documentation for previous versions is available [here](http://django-rest-swagger.readthedocs.io/en/0.3.8/).

---

## Installation

`$ pip install django-rest-swagger`


Add `'rest_framework_swagger'` to `INSTALLED_APPS` in Django settings.

**settings.py**
```python
INSTALLED_APPS = [
    ...
    'rest_framework_swagger',
    ...
]
```

## Quick start

To render the Swagger UI, set the Django REST Framework schema view rendere classes to include
`OpenAPIRenderer` and the `SwaggerUIRenderer` classes from `rest_framework_swagger.renderers`.

The `OpenAPIRenderer` is responsible for generating the JSON spec, while the `SwaggerUIRenderer` renders
the UI.

**Note:** to render the UI, both renderers must be included. The `OpenAPIRenderer` may be used on its own if you wish to host the UI independently.

#### Example

**views.py**
```python
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import schemas
from rest_framework_swagger import OpenAPIRenderer, SwaggerUIRenderer

generator = schemas.SchemaGenerator(title='Bookings API')

@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    return generator.get_schema()


```
**urls.py**
```python
from django.conf.urls import url
from views import schema_view

urlpatterns = [
    url('/', schema_view),
    ...
]
```

#### View in the browser
![Screenshot](/img/ui-screenshot.png)
