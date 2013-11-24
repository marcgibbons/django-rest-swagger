""" Generates API documentation by introspection. """
from django.http import HttpRequest

from rest_framework import viewsets

from .introspectors import BaseIntrospector, APIViewIntrospector, \
    ViewSetIntrospector


class DocumentationGenerator(BaseIntrospector):

    def generate(self, apis):
        """
        Returns documentaion for a list of APIs
        """
        api_docs = []
        for api in apis:
            api_docs.append({
                'description': self.get_description(api['callback']),
                'path': api['path'],
                'operations': self.get_operations(api),
            })

        return api_docs

    def get_operations(self, api):
        """
        Returns docs for the allowed methods of an API endpoint
        """
        operations = []
        path = api['path']
        callback = api['callback']
        callback.request = HttpRequest()

        if issubclass(callback, viewsets.ViewSetMixin):
            introspector = ViewSetIntrospector()
        else:
            introspector = APIViewIntrospector()

        allowed_methods = introspector.get_allowed_methods(callback, path)

        for method in allowed_methods:
            if method == "OPTIONS":
                continue  # No one cares. I impose JSON.

            serializer = introspector.get_serializer_class(callback, path)
            serializer_name = introspector.get_serializer_name(serializer)

            operation = {
                'httpMethod': method,
                'summary': introspector.get_method_summary(callback, method, path),
                'nickname': introspector.get_nickname(callback),
                'notes': introspector.get_notes(callback, method, path),
                'responseClass': serializer_name,
            }

            parameters = introspector.get_parameters(callback, method, path)
            if len(parameters) > 0:
                operation['parameters'] = parameters

            operations.append(operation)

        return operations
