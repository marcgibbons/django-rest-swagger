"""Handles the instrospection of REST Framework Views and ViewSets."""
import re
from unipath import Path

from django.contrib.admindocs.utils import trim_docstring

from rest_framework.views import get_view_name, get_view_description


class BaseIntrospector(object):

    """Base class containing common methods."""

    def path_contains_lookup_field(self, callback, path):
        """
        Evaluates the path containing the default lookup field
        (ie. /items/{pk})
        """
        lookup_field = getattr(callback, 'lookup_field', 'pk')
        return '{%s}' % lookup_field in path

    def get_last_url_element(self, path):
        url_components = Path(path).components()
        last_index = len(url_components) - 1

        return unicode(url_components[last_index])

    def get_name(self, callback):
        """
        Returns the APIView class name
        """
        return get_view_name(callback)

    def get_description(self, callback):
        """
        Returns the first sentence of the first line of the class docstring
        """
        return get_view_description(callback).split("\n")[0].split(".")[0]

    def eval_method_docstring(self, callback, method):
        """
        Attempts to fetch the docs for a class method. Returns None
        if the method does not exist
        """
        try:
            return eval("callback.%s.__doc__" % (str(method).lower()))
        except AttributeError:
            return None

    def get_method_summary(self, callback, method, path=None):
        docs = self.get_method_docs(callback, method, path)
        # If there is no docstring on the method, get class docs
        if docs is None:
            docs = self.get_description(callback)
        docs = trim_docstring(docs).split('\n')[0]

        return docs

    def get_nickname(self, callback):
        """ Returns the APIView's nickname """
        return self.get_name(callback).replace(' ', '_')

    def get_notes(self, callback, method=None, path=None):
        """
        Returns the body of the docstring trimmed before any parameters are
        listed. First, get the class docstring and then get the method's. The
        methods will always inherit the class comments.
        """
        docstring = ""

        if method is not None:
            class_docs = self.get_notes(callback)
            method_docs = self.get_method_docs(callback, method, path)

            if class_docs is not None:
                docstring += class_docs
            if method_docs is not None:
                docstring += '\n' + method_docs
        else:
            docstring = trim_docstring(get_view_description(callback))

        docstring = self.strip_params_from_docstring(docstring)
        docstring = docstring.replace("\n\n", "<br/>")

        return docstring

    def strip_params_from_docstring(self, docstring):
        """
        Strips the params from the docstring (ie. myparam -- Some param) will
        not be removed from the text body
        """
        split_lines = trim_docstring(docstring).split('\n')

        cut_off = None
        for index, line in enumerate(split_lines):
            line = line.strip()
            if line.find('--') != -1:
                cut_off = index
                break
        if cut_off is not None:
            split_lines = split_lines[0:cut_off]

        return "<br/>".join(split_lines)

    def get_models(self, apis):
        """
        Builds a list of Swagger 'models'. These represent
        DRF serializers and their fields
        """
        serializers = self.get_serializer_set(apis)

        models = {}

        for serializer in serializers:
            properties = self.get_serializer_fields(serializer)

            models[serializer.__name__] = {
                'id': serializer.__name__,
                'properties': properties,
            }

        return models

    def get_parameters(self, callback, method, path):
        """
        Returns parameters for an API. Parameters are a combination of HTTP
        query parameters as well as HTTP body parameters that are defined by
        the DRF serializer fields
        """
        params = []
        path_params = self.build_path_parameters(path)
        body_params = self.build_body_parameters(callback, path)
        form_params = self.build_form_parameters(callback, method, path)
        query_params = self.build_query_params_from_docstring(callback, method)

        if path_params:
            params += path_params

        if method not in ["GET", "DELETE"]:
            params += form_params

            if not form_params and body_params is not None:
                params.append(body_params)

        if query_params:
            params += query_params

        return params

    def build_body_parameters(self, callback, path=None):
        serializer = self.get_serializer_class(callback, path)
        serializer_name = self.get_serializer_name(serializer)

        if serializer_name is None:
            return

        return {
            'name': serializer_name,
            'dataType': serializer_name,
            'paramType': 'body',
        }

    def build_path_parameters(self, path):
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

    def build_form_parameters(self, callback, method, path=None):
        """
        Builds form parameters from the serializer class
        """
        data = []
        serializer = self.get_serializer_class(callback, path)

        if serializer is None:
            return data

        fields = serializer().get_fields()

        for name, field in fields.items():

            if getattr(field, 'read_only', False):
                continue

            data_type = field.type_label
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
                'description': getattr(field, 'help_text', ''),
                'defaultValue': getattr(field, 'default', None),
                'required': getattr(field, 'required', None)
            })

        return data

    def build_query_params_from_docstring(self, callback, method=None):
        params = []
        # Combine class & method level comments. If parameters are specified
        if method is not None:
            docstring = self.eval_method_docstring(callback, method)
            params += self.build_query_params_from_docstring(callback)
        else:  # Get the class docstring
            docstring = get_view_description(callback)

        if docstring is None:
            return params

        split_lines = docstring.split('\n')

        for line in split_lines:
            param = line.split(' -- ')
            if len(param) == 2:
                params.append({'paramType': 'query',
                               'name': param[0].strip(),
                               'description': param[1].strip(),
                               'dataType': ''})

        return params

    def get_serializer_fields(self, serializer):
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
                    'defaultValue': getattr(field, 'default', None),
                    'readOnly': getattr(field, 'read_only', None),
                    'valueType': 'RANGE',
                }
            }

        return data

    def get_serializer_class(self, callback, path=None):
        if hasattr(callback, 'get_serializer_class'):
            return callback().get_serializer_class()

    def get_serializer_name(self, serializer):
        if serializer is None:
            return None

        return serializer.__name__

    def get_serializer_set(self, apis):
        """
        Returns a set of serializer classes for a provided list
        of APIs
        """
        serializers = set()

        for api in apis:
            serializer = self.get_serializer_class(api['callback'])
            if serializer is not None:
                serializers.add(serializer)

        return serializers


class APIViewIntrospector(BaseIntrospector):
    def get_allowed_methods(self, callback, path):
        allowed_methods = callback().allowed_methods
        return allowed_methods

    def get_method_docs(self, callback, method, path=None):
        """
        Attempts to retrieve method specific docs for an
        endpoint. If none are available, the class docstring
        will be used
        """
        return self.eval_method_docstring(callback, method)


class ViewSetIntrospector(BaseIntrospector):

    """Handle ViewSet introspection."""

    METHOD_MAPPINGS = {
        'create': 'POST',
        'retrieve': 'GET',
        'update': 'PUT',
        'partial_update': 'PATCH',
        'destroy': 'DELETE',
        'list': 'GET'
    }

    def get_allowed_methods(self, callback, path=None):
        if self.is_custom_action(callback, path):
            return self.get_action_allowed_methods(callback, path)

        allowed_methods = set()

        object_view_methods = ['create', 'retrieve', 'updated', 'partial_update', 'destroy']
        list_view_methods = ['create', 'list']

        if self.path_contains_lookup_field(callback, path):
            possible_methods = object_view_methods
        else:
            possible_methods = list_view_methods

        for method_name in possible_methods:
            if hasattr(callback, method_name):
                allowed_methods.add(self.METHOD_MAPPINGS[method_name])

        return list(allowed_methods)

    def get_method_docs(self, callback, method, path):
        """
        Attempts to retrieve method specific docs for an
        endpoint. If none are available, the class docstring
        will be used
        """
        if self.is_custom_action(callback, path):
            method = self.get_action_function_name(callback, path)
        else:
            method = self.convert_http_method_to_viewset_method(callback, method)
        docs = self.eval_method_docstring(callback, method)

        return docs

    def get_action_allowed_methods(self, callback, path):
        """
        Returns the bound methods to the action
        """
        action_name = self.get_action_function_name(callback, path)
        action_func = eval('callback.%s.im_func' % action_name)

        return action_func.bind_to_methods

    def get_action_function_name(self, callback, path):
        """
        Returns the action function object from the ViewSet
        """
        return self.get_last_url_element(path)

    def is_custom_action(self, callback, path):
        """
        Determines if the endpoint is a ViewSet custom action
        (ie. a method decorated by @link or @action) by checking the URI
        for a lookup field, and seeing if the last element in the URL
        matches a method name on the ViewSet class
        """
        if path is None or not self.path_contains_lookup_field(callback, path):
            return False
        action_name = self.get_last_url_element(path)

        return hasattr(callback, action_name)

    def convert_http_method_to_viewset_method(self, callback, method):
        #  Reverse viewset method to HTTP method mapping
        mapping = {v: k for k, v in self.METHOD_MAPPINGS.items()}
        return mapping[method.upper()]

    def get_serializer_class(self, callback, path=None):
        """Override to return None when the endpoint is a custom action"""
        if not self.is_custom_action(callback, path):
            return super(ViewSetIntrospector, self). \
                get_serializer_class(callback, path)
