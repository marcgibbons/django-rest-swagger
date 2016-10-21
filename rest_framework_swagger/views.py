from rest_framework import schemas
from rest_framework.renderers import CoreJSONRenderer

from . import renderers


def get_swagger_view(title=None, url=None):
    """
    Returns schema view which renders Swagger/OpenAPI.
    """
    return schemas.get_schema_view(
        title=title,
        url=url,
        renderer_classes=[
            CoreJSONRenderer,
            renderers.OpenAPIRenderer,
            renderers.SwaggerUIRenderer
        ]
    )
