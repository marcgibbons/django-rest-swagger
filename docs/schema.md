# Rendering the Schema

Django REST Swagger includes two renderers; the `OpenAPIRenderer` and the 
`SwaggerUIRenderer`.

The `OpenAPIRenderer` is responsible for generating the JSON spec, while the `SwaggerUIRenderer` renders the UI (HTML/JS/CSS).

**Note:** to render the UI, both renderers must be included. The `OpenAPIRenderer` may be used on its own if you wish to host the UI independently.


### The `get_swagger_view` shortcut

As a convenience, a shortcut method with sensible default configurations is provided  to generate SwaggerUI documentation for your API. This view features the following:

- Enforces the DRF permission classes and user context. This means that anonymous users may not see the full endpoint list should views require authentication.
- Anyone can view the docs, however, documentation will only be generated for endpoints which are publicly available.
- Renders CoreJSON

Parameters:

`title`: The title of the documentation (Default: `None`)

`url`: The URL to the documentation (if not on the same host or path). Can be a relative path or  can be an absolute URL. (Default: `None`)


#### Example:
```python
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='My great API', url='/a-different-path')
```

### Advanced Usage

For finer control of the documentation, create your own schema view by using a function based or class-based view. This can be useful if you want to produce documentation for specific URL patterns, or URL confs.

For more detailed documentation on the schema generator, see:

[http://www.django-rest-framework.org/api-guide/schemas/](http://www.django-rest-framework.org/api-guide/schemas/#schemagenerator)


Example: Class-based view
```python
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers


class SwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)

        return Response(schema)
```


Example: function based view
```python
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas

@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Pastebin API')
    return response.Response(generator.get_schema(request=request))
```
