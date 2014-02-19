"""Handles the instrospection of REST Framework Views and ViewSets."""

import re
import yaml
import importlib

from collections import OrderedDict
from _yaml import YAMLError
from abc import ABCMeta, abstractmethod

from django.contrib.admindocs.utils import trim_docstring

from rest_framework.views import get_view_name, get_view_description
from rest_framework.compat import apply_markdown, smart_text
from rest_framework.utils import formatting


def get_resolved_value(obj, attr, default=None):
    value = getattr(obj, attr, default)
    if callable(value):
        value = value()
    return value


class IntrospectorHelper(object):
    __metaclass__ = ABCMeta

    @staticmethod
    def strip_yaml_from_docstring(docstring):
        """
        Strips YAML from the docstring.
        """
        split_lines = trim_docstring(docstring).split('\n')

        cut_off = None
        for index, line in enumerate(split_lines):
            line = line.strip()
            if line.startswith('---'):
                cut_off = index
                break
        if cut_off is not None:
            split_lines = split_lines[0:cut_off]

        return "\n".join(split_lines)


    @staticmethod
    def get_serializer_name(serializer):
        if serializer is None:
            return None

        return serializer.__name__


    @staticmethod
    def get_view_description(callback):
        """
        Returns the first sentence of the first line of the class docstring
        """
        return get_view_description(callback).split("\n")[0].split(".")[0]


class BaseViewIntrospector(object):
    __metaclass__ = ABCMeta

    def __init__(self, callback, path, pattern):
        self.callback = callback
        self.path = path
        self.pattern = pattern

    @abstractmethod
    def __iter__(self):
        pass

    def get_iterator(self):
        return self.__iter__()

    def get_serializer_class(self):
        if hasattr(self.callback, 'get_serializer_class'):
            return self.callback().get_serializer_class()

    def get_description(self):
        """
        Returns the first sentence of the first line of the class docstring
        """
        return IntrospectorHelper.get_view_description(self.callback)


class BaseMethodIntrospector(object):
    __metaclass__ = ABCMeta

    def __init__(self, view_introspector, method):
        self.method = method
        self.parent = view_introspector
        self.callback = view_introspector.callback
        self.path = view_introspector.path

    def get_serializer_class(self):
        return self.parent.get_serializer_class()

    def get_summary(self):
        docs = self.get_docs()

        # If there is no docstring on the method, get class docs
        if docs is None:
            docs = self.parent.get_description()
        docs = trim_docstring(docs).split('\n')[0]

        return docs

    def get_nickname(self):
        """ Returns the APIView's nickname """
        return get_view_name(self.callback).replace(' ', '_')

    def get_notes(self):
        """
        Returns the body of the docstring trimmed before any parameters are
        listed. First, get the class docstring and then get the method's. The
        methods will always inherit the class comments.
        """
        docstring = ""

        class_docs = self.callback.__doc__ or ''
        class_docs = smart_text(class_docs)
        class_docs = IntrospectorHelper.strip_yaml_from_docstring(class_docs)
        method_docs = self.get_docs()

        if class_docs is not None:
            docstring += class_docs + "  \n"
        if method_docs is not None:
            method_docs = formatting.dedent(smart_text(method_docs))
            method_docs = IntrospectorHelper.strip_yaml_from_docstring(
                method_docs
            )
            docstring += '\n' + method_docs

        # Markdown is optional
        if apply_markdown:
            docstring = apply_markdown(docstring)
        else:
            docstring = docstring.replace("\n\n", "<br/>")

        return docstring

    def get_parameters(self):
        """
        Returns parameters for an API. Parameters are a combination of HTTP
        query parameters as well as HTTP body parameters that are defined by
        the DRF serializer fields
        """
        params = []
        path_params = self.build_path_parameters()
        body_params = self.build_body_parameters()
        form_params = self.build_form_parameters()

        if path_params:
            params += path_params

        if self.get_http_method() not in ["GET", "DELETE"]:
            params += form_params

            if not form_params and body_params is not None:
                params.append(body_params)

        return params

    def get_http_method(self):
        return self.method

    @abstractmethod
    def get_docs(self):
        return ''

    def retrieve_docstring(self):
        """
        Attempts to fetch the docs for a class method. Returns None
        if the method does not exist
        """
        method = str(self.method).lower()
        if not hasattr(self.callback, method):
            return None
        return getattr(self.callback, method).__doc__

    def build_body_parameters(self):
        serializer = self.get_serializer_class()
        serializer_name = IntrospectorHelper.get_serializer_name(serializer)

        if serializer_name is None:
            return

        return {
            'name': serializer_name,
            'dataType': serializer_name,
            'paramType': 'body',
        }

    def build_path_parameters(self):
        """
        Gets the parameters from the URL
        """
        url_params = re.findall('/{([^}]*)}', self.path)
        params = []

        for param in url_params:
            params.append({
                'name': param,
                'dataType': 'string',
                'paramType': 'path',
                'required': True
            })

        return params

    def build_form_parameters(self):
        """
        Builds form parameters from the serializer class
        """
        data = []
        serializer = self.get_serializer_class()

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
                'defaultValue': get_resolved_value(field, 'default'),
                'required': getattr(field, 'required', None)
            })

        return data


class APIViewIntrospector(BaseViewIntrospector):
    def __iter__(self):
        methods = self.callback().allowed_methods
        for method in methods:
            yield APIViewMethodIntrospector(self, method)


class APIViewMethodIntrospector(BaseMethodIntrospector):
    def get_docs(self):
        """
        Attempts to retrieve method specific docs for an
        endpoint. If none are available, the class docstring
        will be used
        """
        return self.retrieve_docstring()


class ViewSetIntrospector(BaseViewIntrospector):
    """Handle ViewSet introspection."""

    def __iter__(self):
        methods = self._resolve_methods()
        for method in methods:
            yield ViewSetMethodIntrospector(self, methods[method], method)

    def _resolve_methods(self):
        if not hasattr(self.pattern.callback, 'func_code') or \
                not hasattr(self.pattern.callback, 'func_closure') or \
                not hasattr(self.pattern.callback.func_code, 'co_freevars') or \
                'actions' not in self.pattern.callback.func_code.co_freevars:
            raise RuntimeError('Unable to use callback invalid closure/function specified.')

        idx = self.pattern.callback.func_code.co_freevars.index('actions')
        return self.pattern.callback.func_closure[idx].cell_contents


class ViewSetMethodIntrospector(BaseMethodIntrospector):
    def __init__(self, view_introspector, method, http_method):
        super(ViewSetMethodIntrospector, self).__init__(view_introspector, method)
        self.http_method = http_method.upper()

    def get_http_method(self):
        return self.http_method

    def get_docs(self):
        """
        Attempts to retrieve method specific docs for an
        endpoint. If none are available, the class docstring
        will be used
        """
        return self.retrieve_docstring()


class YAMLDocstringParser(object):
    """
    Docstring parser powered by YAML syntax

    This parser allows you override some parts of automatic method inspection
    behaviours which are not always correct.

    See the following documents for more information about YAML and Swagger:
    - https://github.com/wordnik/swagger-core/wiki
    - http://www.yaml.org/spec/1.2/spec.html
    - https://github.com/wordnik/swagger-codegen/wiki/Creating-Swagger-JSON-from-YAML-files

    1. Control over parameters
    ============================================================================
    Define parameters and its properties in docstrings:

        parameters:
            - name: some_param
              description: Foobar long description goes here
              required: true
              allowMultiple: false
              type: integer
              paramType: form
              minimum: 10
              maximum: 100
            - name: other_foo
              paramType: query
            - name: avatar
              type: file

    It is possible to override parameters discovered by method inspector by
    defining:
        `parameters_strategy` option to either `merge` or `replace`

    To define different strategies for different `paramType`'s use the
    following syntax:
        parameters_strategy:
            form: replace
            query: merge

    By default strategy is set to `merge`


    Sometimes method inspector produces wrong list of parameters that
    you might not won't to see in SWAGGER form. To handle this situation
    define `paramTypes` that should be omitted
        omit_parameters:
            - form

    2. Control over serializers
    ============================================================================
    Once in a while you are using different serializers inside methods
    but automatic method inspector cannot detect this. For that purpose there
    is two explicit parameters that allows you to discard serializer detected
    by method inspector OR replace it with another one

        serializer: some.package.FooSerializer
        omit_serializer: true

    3. Custom Response Class
    ============================================================================
    If your view is not using serializer at all but instead outputs simple
    data type such as JSON you may define custom response object in method
    signature like follows:

        responseClass:
          name:
            required: true
            type: string
          url:
            required: false
            type: url

    4. Response Messages (Error Codes)
    ============================================================================
    If you'd like to share common response errors that your APIView might throw
    you can define them in docstring using following format:

    responseMessages:
        - code: 401
          message: Not authenticated
        - code: 403
          message: Insufficient rights to call this procedure


    SAMPLE DOCSTRING:
    ============================================================================

    ---
    # API Docs
    # Note: YAML always starts with `---`

    responseClass:
      name:
        required: true
        type: string
      url:
        required: false
        type: url

    serializer: .serializers.FooSerializer
    omit_serializer: false

    parameters_strategy: merge
    omit_parameters:
        - path
    parameters:
        - name: name
          description: Foobar long description goes here
          required: true
          allowMultiple: false
          type: string
          paramType: form
          minimum: 10
          maximum: 100
        - name: other_foo
          paramType: query
        - name: other_bar
          paramType: query
        - name: avatar
          type: file

    responseMessages:
        - code: 401
          message: Not authenticated
    """
    PARAM_TYPES = ['header', 'path', 'form', 'body', 'query']

    def __init__(self, docstring):
        self.object = self.load_obj_from_docstring(docstring=docstring)
        if self.object is None:
            self.object = {}

    @staticmethod
    def load_obj_from_docstring(docstring):
        """Loads YAML from docstring"""
        split_lines = trim_docstring(docstring).split('\n')

        # Cut YAML from rest of docstring
        for index, line in enumerate(split_lines):
            line = line.strip()
            if line.startswith('---'):
                cut_from = index
                break
        else:
            return None

        yaml_string = "\n".join(split_lines[cut_from:])
        try:
            return yaml.load(yaml_string)
        except YAMLError:
            return None

    @staticmethod
    def _load_class(cls_name, callback):
        """
        Dynamically load a class from a string
        """
        if not cls_name or not callback or not hasattr(callback, '__module__'):
            return None

        if cls_name.find('.') == -1:
            # within current module/file
            class_name = cls_name
            module_path = callback.__module__
        else:
            # relative lookup?
            if cls_name[0] == '.':
                module_path = callback.__module__
                while cls_name[0] == '.':
                    idx = module_path.rfind('.')
                    if idx == -1:
                        if module_path == '':
                            return None
                        module_path = ''
                    else:
                        module_path = module_path[:idx]

                    cls_name = cls_name[1:]
                    if len(cls_name) <= 1:
                        return None

                if module_path:
                    cls_name = module_path + '.' + cls_name

            # extract class and module
            parts = cls_name.split('.')
            module_path, class_name = '.'.join(parts[:-1]), parts[-1]

        try:
            module = importlib.import_module(module_path)
            if hasattr(module, class_name):
                return getattr(module, class_name)
        except ImportError:
            pass
        return None

    def get_serializer_class(self, callback):
        """
        Retrieves serializer class from YAML object
        """
        serializer = self.object.get('serializer', None)
        try:
            return self._load_class(serializer, callback)
        except (ImportError, ValueError):
            pass
        return None

    def get_response_class(self):
        """
        Docstring may define custom response class
        """
        return self.object.get('responseClass', None)

    def get_response_messages(self):
        """
        Retrieves response error codes from YAML object
        """
        messages = []
        response_messages = self.object.get('responseMessages', [])
        for message in response_messages:
            messages.append({
                'code': message.get('code', 'Unknown'),
                'message': message.get('message')
            })
        return messages

    def get_parameters(self):
        """
        Retrieves parameters from YAML object
        """
        params = []
        fields = self.object.get('parameters', [])
        for field in fields:
            f = {
                'name': field.get('name', None),
                'description': field.get('description', None),
                'required': field.get('required', False),
                'allowMultiple': field.get('allowMultiple', False),
                'type': field.get('type', 'string'),
                'paramType': field.get('paramType', 'form'),
                'defaultValue': field.get('defaultValue', None),
            }

            # Min/Max are optional
            if 'minimum' in field:
                f['minimum'] = field.get('minimum', 0)

            if 'maximum' in field:
                f['maximum'] = field.get('maximum', 0)

            # File support
            if f['type'] == 'file':
                f['paramType'] = 'body'

            params.append(f)

        return params

    def discover_parameters(self, inspector):
        """
        Applies parameters strategy for parameters discovered
        from method and docstring
        """
        parameters = []
        docstring_params = self.get_parameters()
        method_params = inspector.get_parameters()

        for param_type in self.PARAM_TYPES:
            if self.should_omit_parameters(param_type):
                continue
            parameters += self._apply_strategy(
                param_type, method_params, docstring_params
            )

        return parameters

    def should_omit_parameters(self, param_type):
        """
        Checks if particular parameter types should be omitted explicitly
        """
        return param_type in self.object.get('omit_parameters', [])

    def should_omit_serializer(self):
        """
        Checks if serializer should be intentionally omitted
        """
        return self.object.get('omit_serializer', False)

    def _apply_strategy(self, param_type, method_params, docstring_params):
        """
        Applies strategy for subset of parameters filtered by `paramType`
        """
        strategy = self.get_parameters_strategy(param_type=param_type)
        method_params = self._filter_params(
            params=method_params,
            key='paramType',
            val=param_type
        )
        docstring_params = self._filter_params(
            params=docstring_params,
            key='paramType',
            val=param_type
        )

        if strategy == 'replace':
            return docstring_params or method_params
        elif strategy == 'merge':
            return self._merge_params(
                method_params,
                docstring_params,
                key='name',
            )

        return []

    @staticmethod
    def _filter_params(params, key, val):
        """
        Returns filter function for parameters structure
        """
        fn = lambda o: o.get(key, None) == val
        return filter(fn, params)

    @staticmethod
    def _merge_params(params1, params2, key):
        """
        Helper method.
        Merges parameters lists by key
        """
        merged = OrderedDict()
        for item in params1 + params2:
            merged[item[key]] = item

        return [val for (_, val) in merged.items()]

    def get_parameters_strategy(self, param_type=None):
        """
        Get behaviour strategy for parameter types.

        It can be either `merge` or `replace`:
            - `merge` overwrites duplicate parameters signatures
                discovered by inspector with the ones defined explicitly in
                docstring
            - `replace` strategy completely overwrites parameters discovered
                by inspector with the ones defined explicitly in docstring.

        Note: Strategy can be defined per `paramType` so `path` parameters can
        use `merge` strategy while `form` parameters will use `replace`
        strategy.

        Default strategy: `merge`
        """
        default = 'merge'
        strategy = self.object.get('parameters_strategy', default)
        if hasattr(strategy, 'get') and param_type is not None:
            strategy = strategy.get(param_type, default)

        if strategy not in ['merge', 'replace']:
            strategy = default

        return strategy
