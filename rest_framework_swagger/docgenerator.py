""" Generates API documentation by introspection. """
from django.http import HttpRequest

from rest_framework import viewsets

from .introspectors import APIViewIntrospector, \
    ViewSetIntrospector, BaseMethodIntrospector, IntrospectorHelper, \
    get_resolved_value, YAMLDocstringParser


class DocumentationGenerator(object):
    # Serializers defined in docstrings
    explicit_serializers = set()

    # Response classes defined in docstrings
    explicit_response_classes = dict()

    def generate(self, apis):
        """
        Returns documentation for a list of APIs
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

            doc_parser = YAMLDocstringParser(
                docstring=method_introspector.get_docs())

            serializer = self._get_method_serializer(
                doc_parser, method_introspector)

            response_class = self._get_method_response_class(
                doc_parser, serializer, introspector, method_introspector)

            operation = {
                'method': method_introspector.get_http_method(),
                'summary': method_introspector.get_summary(),
                'nickname': method_introspector.get_nickname(),
                'notes': method_introspector.get_notes(),
                'type': response_class,
            }

            response_messages = doc_parser.get_response_messages()
            parameters = doc_parser.discover_parameters(
                inspector=method_introspector)

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
            properties, required = self._get_serializer_fields(serializer)

            models[serializer.__name__] = {
                'id': serializer.__name__,
                'required': required,
                'properties': properties,
            }

        models.update(self.explicit_response_classes)
        return models

    def _get_method_serializer(self, doc_parser, method_inspector):
        """
        Returns serializer used in method.
        Registers custom serializer from docstring in scope.

        Serializer might be ignored if explicitly told in docstring
        """
        serializer = method_inspector.get_serializer_class()

        docstring_serializer = doc_parser.get_serializer_class(
            callback=method_inspector.callback
        )

        if doc_parser.get_response_class() is not None:
            # Custom response class detected
            return None

        if docstring_serializer is not None:
            self.explicit_serializers.add(docstring_serializer)
            serializer = docstring_serializer

        if doc_parser.should_omit_serializer():
            serializer = None

        return serializer

    def _get_method_response_class(self, doc_parser, serializer,
                                   view_inspector, method_inspector):
        """
        Returns responseClass for method.
        This might be custom responseClass from docstring or discovered
        serializer class name.

        Once custom responseClass found in docstring - it'd be
        registered in a scope
        """
        response_class = doc_parser.get_response_class()
        if response_class is not None:
            # Register class in scope
            view_name = view_inspector.callback.__name__
            view_name = view_name.replace('ViewSet', '')
            view_name = view_name.replace('APIView', '')
            view_name = view_name.replace('View', '')
            response_class_name = "{view}{method}Response".format(
                view=view_name,
                method=method_inspector.method.title().replace('_', '')
            )
            self.explicit_response_classes.update({
                response_class_name: {
                    "id": response_class_name,
                    "properties": response_class
                }
            })
            return response_class_name
        else:
            return IntrospectorHelper.get_serializer_name(serializer)

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
        required = []
        for name, field in fields.items():
            if getattr(field, 'required', None):
                required.append(name)

            data_type = field.type_label

            # guess format
            data_format = 'string'
            if data_type in BaseMethodIntrospector.PRIMITIVES:
                data_format = BaseMethodIntrospector.PRIMITIVES.get(data_type)[0]

            f = {
                'description': getattr(field, 'help_text', ''),
                'type': data_type,
                'format': data_format,
                'required': getattr(field, 'required', False),
                'defaultValue': get_resolved_value(field, 'default'),
                'readOnly': getattr(field, 'read_only', None),
            }

            # Min/Max values
            max_val = getattr(field, 'max_val', None)
            min_val = getattr(field, 'min_val', None)
            if max_val is not None and data_type == 'integer':
                f['minimum'] = min_val

            if max_val is not None and data_type == 'integer':
                f['maximum'] = max_val

            # ENUM options
            if field.type_label == 'multiple choice' \
                    and isinstance(field.choices, list):
                f['enum'] = [k for k, v in field.choices]

            data[name] = f

        return data, required

    def _get_serializer_class(self, callback):
        if hasattr(callback, 'get_serializer_class'):
            return callback().get_serializer_class()
