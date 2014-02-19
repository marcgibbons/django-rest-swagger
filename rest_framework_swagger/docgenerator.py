""" Generates API documentation by introspection. """
from django.http import HttpRequest

from rest_framework import viewsets

from .introspectors import APIViewIntrospector, \
    ViewSetIntrospector, BaseMethodIntrospector, IntrospectorHelper, \
    get_resolved_value, YAMLDocstringParser


class DocumentationGenerator(object):
    explicit_serializers = set()

    def generate(self, apis):
        """
        Returns documentaion for a list of APIs
        """
        api_docs = []
        for api in apis:
            api_docs.append({
                'description': IntrospectorHelper.get_view_description(api['callback']),
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
        pattern = api['pattern']
        callback = api['callback']
        callback.request = HttpRequest()

        if issubclass(callback, viewsets.ViewSetMixin):
            introspector = ViewSetIntrospector(callback, path, pattern)
        else:
            introspector = APIViewIntrospector(callback, path, pattern)

        for method_introspector in introspector:
            if not isinstance(method_introspector, BaseMethodIntrospector) or \
                    method_introspector.get_http_method() == "OPTIONS":
                continue  # No one cares. I impose JSON.

            docstring_parser = YAMLDocstringParser(method_introspector)
            serializer = method_introspector.get_serializer_class()

            # Docstring may override serializer discovery
            docstring_serializer = docstring_parser.get_serializer_class()
            if docstring_serializer is not None:
                self.explicit_serializers.add(docstring_serializer)
                serializer = docstring_serializer

            # Serializer might be intentionally omitted
            if docstring_parser.should_omit_serializer():
                serializer = None

            serializer_name = IntrospectorHelper.get_serializer_name(serializer)

            operation = {
                'httpMethod': method_introspector.get_http_method(),
                'summary': method_introspector.get_summary(),
                'nickname': method_introspector.get_nickname(),
                'notes': method_introspector.get_notes(),
                'responseClass': serializer_name,
            }

            response_messages = docstring_parser.get_response_messages()
            parameters = docstring_parser.discover_parameters()

            if parameters:
                operation['parameters'] = parameters

            if response_messages:
                operation['responseMessages'] = response_messages

            operations.append(operation)

        return operations

    def get_models(self, apis):
        """
        Builds a list of Swagger 'models'. These represent
        DRF serializers and their fields
        """
        serializers = self._get_serializer_set(apis)
        serializers.update(self.explicit_serializers)

        models = {}

        for serializer in serializers:
            properties = self._get_serializer_fields(serializer)

            models[serializer.__name__] = {
                'id': serializer.__name__,
                'properties': properties,
            }

        return models

    def _get_serializer_set(self, apis):
        """
        Returns a set of serializer classes for a provided list
        of APIs
        """
        serializers = set()

        for api in apis:
            serializer = self._get_serializer_class(api['callback'])
            if serializer is not None:
                serializers.add(serializer)

        return serializers

    def _get_serializer_fields(self, serializer):
        """
        Returns serializer fields in the Swagger MODEL format
        """
        if serializer is None:
            return

        fields = serializer().get_fields()

        data = {}
        for name, field in fields.items():

            data[name] = {
                'type': field.type_label,
                'required': getattr(field, 'required', None),
                'allowableValues': {
                    'min': getattr(field, 'min_length', None),
                    'max': getattr(field, 'max_length', None),
                    'defaultValue': get_resolved_value(field, 'default', None),
                    'readOnly': getattr(field, 'read_only', None),
                    'valueType': 'RANGE',
                }
            }

        return data

    def _get_serializer_class(self, callback):
        if hasattr(callback, 'get_serializer_class'):
            return callback().get_serializer_class()
