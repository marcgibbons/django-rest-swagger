"""
Generates Documentation
"""
import re
from django.contrib.admindocs.utils import trim_docstring

class DocumentationGenerator(object):

    def generate(self, apis):
        """
        Returns documentaion for a list of APIs
        """
        api_docs = []
        for api in apis:
            api_docs.append({
                'description': self.__get_description__(api['callback']),
                'path': api['path'],
                'operations': self.__get_operations__(api),
            })

        return api_docs

    def __get_operations__(self, api):
        """
        Returns docs for the allowed methods of an API endpoint
        """
        operations = []
        callback = api['callback']

        for method in callback.allowed_methods:
            if method == "OPTIONS":
                continue  # No one cares

            operation = {
                'httpMethod': method,
                'summary': self.__get_method_docs__(callback, method),
                'nickname': self.__get_nickname__(callback),
                'notes': self.__get_notes__(callback),
                'responseClass': self.__get_serializer_class_name__(callback),
            }

            parameters = self.get_parameters(api, method)
            if len(parameters) > 0:
                operation['parameters'] = parameters

            operations.append(operation)

        return operations

    def __get_name__(self, callback):
        """
        Returns the APIView class name
        """
        return callback.get_name()

    def __get_description__(self, callback):
        """
        Returns the first sentence of the first line of the class docstring
        """
        return callback.get_description().split("\n")[0].split(".")[0]

    def __get_method_docs__(self, callback, method):
        """
        Attempts to retrieve method specific docs for an
        endpoint. If none are available, the class docstring
        will be used
        """
        docs = eval("callback.%s.__doc__" % (str(method).lower()))

        if docs is None:
            docs = self.__get_description__(callback)

        return trim_docstring(docs)

    def __get_nickname__(self, callback):
        return self.__get_name__(callback)

    def __get_notes__(self, callback):
        return trim_docstring(callback.get_description())

    def get_models(self, apis):
        """
        Builds a list of Swagger 'models'. These represent
        DRF serializers and their fields
        """
        serializers = self.__get_serializer_set__(apis)

        models = {}

        for serializer in serializers:
            properties = self.__get_serializer_fields__(serializer)

            models[serializer.__name__] = {
                'id': serializer.__name__,
                'properties': properties,
            }

        return models

    def get_parameters(self, api, method):
        """
        Returns parameters for an API. Parameters are a combination of HTTP
        query parameters as well as HTTP body parameters that are defined by
        the DRF serializer fields
        """
        params = []
        path_params = self.__build_path_parameters__(api['path'])
        body_params = self.__build_body_parameters__(api['callback'])
        form_params = self.__build_form_parameters__(api['callback'], method)

        if path_params:
            params += path_params

        if method not in ["GET", "DELETE"]:
            params += form_params

            if not form_params and body_params is not None:
                params.append(body_params)

        return params

    def __build_body_parameters__(self, callback):
        serializer_name = self.__get_serializer_class_name__(callback)

        if serializer_name is None:
            return

        return {
            'name': serializer_name,
            'dataType': serializer_name,
            'paramType': 'body',
        }

    def __build_path_parameters__(self, path):
        """
        Gets the parameters from the URL
        """
        url_params = re.findall('/{([^}]*)}', path)
        params = []

        for param in url_params:
            params.append({
                'name': param,
                'dataType': 'string',
                'paramType': 'path',
                'required': True
            })

        return params

    def __build_form_parameters__(self, callback, method):
        """
        Builds form parameters from the serializer class
        """
        data = []
        serializer = self.__get_serializer_class__(callback)

        if serializer is None:
            return data

        fields = serializer().get_fields()

        for name, field in fields.items():

            if getattr(field, 'read_only', False):
                continue

            data_type = self.__convert_types_to_swagger__(field.__class__.__name__)
            max_length = getattr(field, 'max_length', None)
            min_length = getattr(field, 'min_length', None)
            allowable_values = None

            if max_length is not None or min_length is not None:
                allowable_values = {
                    'max': max_length,
                    'min': min_length,
                    'valueType': 'RANGE'
                }

            data.append({
                'paramType': 'form',
                'name': name,
                'dataType': data_type,
                'allowableValues': allowable_values,
                'description': '',
                'defaultValue': getattr(field, 'default', None),
                'required': getattr(field, 'required', None)
            })

        return data

    def __get_serializer_fields__(self, serializer):
        """
        Returns serializer fields in the Swagger MODEL format
        """
        if serializer is None:
            return

        fields = serializer().get_fields()

        data = {}
        for name, field in fields.items():
            data[name] = {
                'type': self.__convert_types_to_swagger__(field.__class__.__name__),
                'required': getattr(field, 'required', None),
                'allowableValues': {
                    'min': getattr(field, 'min_length', None),
                    'max': getattr(field, 'max_length', None),
                    'defaultValue': getattr(field, 'default', None),
                    'readOnly': getattr(field, 'read_only', None),
                    'valueType': 'RANGE',
                }
            }

        return data

    def __get_serializer_class__(self, callback):
        if hasattr(callback, 'get_serializer_class'):
            return callback.get_serializer_class()

    def __get_serializer_class_name__(self, callback):
        serializer = self.__get_serializer_class__(callback)

        if serializer is None:
            return None

        return serializer.__name__

    def __get_serializer_set__(self, apis):
        """
        Returns a set of serializer classes for a provided list
        of APIs
        """
        serializers = set()

        for api in apis:
            serializer = self.__get_serializer_class__(api['callback'])
            if serializer is not None:
                serializers.add(serializer)

        return serializers

    def __convert_types_to_swagger__(self, field_type):
        """
        Converts Django REST Framework data types into Swagger data types
        """
        type_matching = (
            ('BooleanField', 'boolean'),
            ('CharField', 'string'),
            ('URLField', 'string'),
            ('SlugField', 'string'),
            ('ChoiceField', 'LIST'),
            ('EmailField', 'string'),
            ('RegexField', 'string'),
            ('DateTimeField', 'Date'),
            ('DateField', 'Date'),
            ('TimeField', 'string'),
            ('IntegerField', 'int'),
            ('FloatField', 'float'),
            ('DecimalField', 'double'),
            ('FileField', 'byte'),
            ('ImageField', 'byte'),
        )
        type_matching = dict(type_matching)
        return type_matching.get(field_type, 'string')
