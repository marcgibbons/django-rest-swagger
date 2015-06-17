from django.utils import six
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView

from .compat import import_string
from rest_framework_swagger import SWAGGER_SETTINGS


class APIDocView(APIView):
    def initial(self, request, *args, **kwargs):
        self.permission_classes = (self.get_permission_class(request),)
        self.host = request.build_absolute_uri()
        self.api_path = SWAGGER_SETTINGS['api_path']
        self.api_full_uri = request.build_absolute_uri(self.api_path)
        return super(APIDocView, self).initial(request, *args, **kwargs)

    def get_permission_class(self, request):
        if SWAGGER_SETTINGS['is_superuser'] and not request.user.is_superuser:
            return IsAdminUser
        if SWAGGER_SETTINGS['is_authenticated'] and not request.user.is_authenticated():
            return IsAuthenticated
        return AllowAny

    def handle_resource_access(self, request, resource):
        resource_access_handler = SWAGGER_SETTINGS.get('resource_access_handler')
        if isinstance(resource_access_handler, six.string_types):
            resource_access_handler = import_string(resource_access_handler)
            if resource_access_handler:
                return resource_access_handler(request, resource)
        return True
