# -*- coding: utf-8 -*-

"""Handles the instrospection of REST Framework Views and ViewSets."""

import inspect
import re
import yaml
import importlib

from .compat import OrderedDict
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
    def strip_params_from_docstring(docstring):
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

    @staticmethod
    def get_serializer_name(serializer):
        if serializer is None:
            return None

        if inspect.isclass(serializer):
            return serializer.__name__

        return serializer.__class__.__name__

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

    def get_yaml_parser(self):
        parser = YAMLDocstringParser(self)
        return parser

    @abstractmethod
    def __iter__(self):
        pass

    def get_iterator(self):
        return self.__iter__()

    def get_serializer_class(self):
        # import pdb;pdb.set_trace()
        if hasattr(self.callback, 'get_serializer_class'):
            view = self.callback()
            if not hasattr(view, 'kwargs'):
                view.kwargs = dict()
            if hasattr(self.pattern, 'default_args'):
                view.kwargs.update(self.pattern.default_args)
            return view.get_serializer_class()

    def get_description(self):
        """
        Returns the first sentence of the first line of the class docstring
        """
        return IntrospectorHelper.get_view_description(self.callback)

    def get_docs(self):
        return self.callback.__doc__


class BaseMethodIntrospector(object):
    __metaclass__ = ABCMeta

    PRIMITIVES = {
        'integer': ['int32', 'int64'],
        'number': ['float', 'double'],
        'string': ['string', 'byte', 'date', 'date-time'],
        'boolean': ['boolean'],
    }

    def __init__(self, view_introspector, method):
        self.method = method
        self.parent = view_introspector
        self.callback = view_introspector.callback
        self.path = view_introspector.path

    def get_module(self):
        return self.callback.__module__

    def check_yaml_methods(self, yaml_methods):
        missing_set = set()
        for key in yaml_methods:
            if key not in self.parent.methods():
                missing_set.add(key)
        if missing_set:
            raise Exception(
                "methods %s in class docstring are not in view methods %s"
                % (list(missing_set), list(self.parent.methods())))

    def get_yaml_parser(self):
        parser = YAMLDocstringParser(self)
        parent_parser = YAMLDocstringParser(self.parent)
        self.check_yaml_methods(parent_parser.object.keys())
        new_object = {}
        new_object.update(parent_parser.object.get(self.method, {}))
        new_object.update(parser.object)
        parser.object = new_object
        return parser

    def get_serializer_class(self):
        parser = self.get_yaml_parser()
        serializer = parser.get_serializer_class(self.callback)
        if serializer is None:
            serializer = self.parent.get_serializer_class()
        return serializer

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
        class_docs = IntrospectorHelper.strip_params_from_docstring(class_docs)
        method_docs = self.get_docs()

        if class_docs is not None:
            docstring += class_docs + "  \n"
        if method_docs is not None:
            method_docs = formatting.dedent(smart_text(method_docs))
            method_docs = IntrospectorHelper.strip_yaml_from_docstring(
                method_docs
            )
            method_docs = IntrospectorHelper.strip_params_from_docstring(
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
        query_params = self.build_query_params_from_docstring()

        if path_params:
            params += path_params

        if self.get_http_method() not in ["GET", "DELETE"]:
            params += form_params

            if not form_params and body_params is not None:
                params.append(body_params)

        if query_params:
            params += query_params

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
            'type': serializer_name,
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
                'type': 'string',
                'paramType': 'path',
                'required': True
            })

        return params

    def build_query_params_from_docstring(self):
        params = []

        docstring = self.retrieve_docstring() or ''
        docstring += "\n" + get_view_description(self.callback)

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

            # guess format
            data_format = 'string'
            if data_type in self.PRIMITIVES:
                data_format = self.PRIMITIVES.get(data_type)[0]

            f = {
                'paramType': 'form',
                'name': name,
                'description': getattr(field, 'help_text', ''),
                'type': data_type,
                'format': data_format,
                'required': getattr(field, 'required', False),
                'defaultValue': get_resolved_value(field, 'default'),
            }

            # Min/Max values
            max_val = getattr(field, 'max_val', None)
            min_val = getattr(field, 'min_val', None)
            if max_val is not None and data_type == 'integer':
                f['minimum'] = min_val

            if max_val is not None and data_type == 'integer':
                f['maximum'] = max_val

            # ENUM options
            if field.type_label in ['multiple choice', 'choice'] \
                    and isinstance(field.choices, list):
                f['enum'] = [k for k, v in field.choices]

            data.append(f)

        return data


class APIViewIntrospector(BaseViewIntrospector):
    def __iter__(self):
        for method in self.methods():
            yield APIViewMethodIntrospector(self, method)

    def methods(self):
        return self.callback().allowed_methods


class WrappedAPIViewIntrospector(BaseViewIntrospector):
    def __iter__(self):
        for method in self.methods():
            yield WrappedAPIViewMethodIntrospector(self, method)

    def methods(self):
        return self.callback().allowed_methods

    def get_notes(self):
        class_docs = self.callback.__doc__ or ''
        class_docs = smart_text(class_docs)
        class_docs = IntrospectorHelper.strip_yaml_from_docstring(class_docs)
        class_docs = IntrospectorHelper.strip_params_from_docstring(class_docs)
        return class_docs


class APIViewMethodIntrospector(BaseMethodIntrospector):
    def get_docs(self):
        """
        Attempts to retrieve method specific docs for an
        endpoint. If none are available, the class docstring
        will be used
        """
        return self.retrieve_docstring()


class WrappedAPIViewMethodIntrospector(BaseMethodIntrospector):
    def get_docs(self):
        """
        Attempts to retrieve method specific docs for an
        endpoint. If none are available, the class docstring
        will be used
        """
        return self.callback.__doc__

    def get_module(self):
        from rest_framework_swagger.decorators import wrapper_to_func
        func = wrapper_to_func(self.callback)
        return func.__module__

    def get_notes(self):
        return self.parent.get_notes()

    def get_yaml_parser(self):
        parser = YAMLDocstringParser(self)
        return parser


class ViewSetIntrospector(BaseViewIntrospector):
    """Handle ViewSet introspection."""

    def __init__(self, callback, path, pattern, patterns=None):
        super(ViewSetIntrospector, self).__init__(callback, path, pattern)
        self.patterns = patterns or [pattern]

    def __iter__(self):
        methods = self._resolve_methods()
        for method in methods:
            yield ViewSetMethodIntrospector(self, methods[method], method)

    def methods(self):
        stuff = []
        for pattern in self.patterns:
            if pattern.callback:
                stuff.extend(self._resolve_methods(pattern).values())
        return stuff

    def _resolve_methods(self, pattern=None):
        from .decorators import closure_n_code, get_closure_var
        if pattern is None:
            pattern = self.pattern
        callback = pattern.callback

        try:
            x = closure_n_code(callback)

            while getattr(x.code, 'co_name') != 'view':
                # lets unwrap!
                callback = get_closure_var(callback)
                x = closure_n_code(callback)

            freevars = x.code.co_freevars
        except (AttributeError, IndexError):
            raise RuntimeError('Unable to use callback invalid closure/function specified.')
        else:
            return x.closure[freevars.index('actions')].cell_contents


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


def multi_getattr(obj, attr, default=None):
    """
    Get a named attribute from an object; multi_getattr(x, 'a.b.c.d') is
    equivalent to x.a.b.c.d. When a default argument is given, it is
    returned when any attribute in the chain doesn't exist; without
    it, an exception is raised when a missing attribute is encountered.

    """
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = getattr(obj, i)
        except AttributeError:
            if default:
                return default
            else:
                raise
    return obj


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

        type:
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


    5. Different models for reading and writing operations
    ============================================================================
    Since REST Framework won't output write_only fields in responses as well as
    does not require read_only fields to be provided it is worth to
    automatically register 2 separate models for reading and writing operations.

    Discovered serializer will be registered with `Write` or `Read` prefix.
    Response Class will be automatically adjusted if serializer class was
    detected by method inspector.

    You can also refer to this models in your parameters:

    parameters:
        - name: CigarSerializer
          type: WriteCigarSerializer
          paramType: body


    SAMPLE DOCSTRING:
    ============================================================================

    ---
    # API Docs
    # Note: YAML always starts with `---`

    type:
      name:
        required: true
        type: string
      url:
        required: false
        type: url
      created_at:
        required: true
        type: string
        format: date-time

    serializer: .serializers.FooSerializer
    omit_serializer: false

    parameters_strategy: merge
    omit_parameters:
        - path
    parameters:
        - name: name
          description: Foobar long description goes here
          required: true
          type: string
          paramType: form
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
    yaml_error = None

    def __init__(self, method_introspector):
        self.method_introspector = method_introspector
        self.object = self.load_obj_from_docstring(
            docstring=self.method_introspector.get_docs())
        if self.object is None:
            self.object = {}

    def load_obj_from_docstring(self, docstring):
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
        yaml_string = formatting.dedent(yaml_string)
        try:
            return yaml.load(yaml_string)
        except yaml.YAMLError as e:
            self.yaml_error = e
            return None

    def _load_class(self, cls_path, callback):
        """
        Dynamically load a class from a string
        """
        if not cls_path or not callback or not hasattr(callback, '__module__'):
            return None

        package = None

        if '.' not in cls_path:
            # within current module/file
            class_name = cls_path
            module_path = self.method_introspector.get_module()
        else:
            # relative or fully qualified path import
            class_name = cls_path.split('.')[-1]
            module_path = ".".join(cls_path.split('.')[:-1])

            if cls_path.startswith('.'):
                # relative lookup against current package
                # ..serializers.FooSerializer
                package = self.method_introspector.get_module()

        class_obj = None
        # Try to perform local or relative/fq import
        try:
            module = importlib.import_module(module_path, package=package)
            class_obj = getattr(module, class_name, None)
        except ImportError:
            pass

        # Class was not found, maybe it was imported to callback module?
        # from app.serializers import submodule
        # serializer: submodule.FooSerializer
        if class_obj is None:
            try:
                module = importlib.import_module(
                    self.method_introspector.get_module())
                class_obj = multi_getattr(module, cls_path, None)
            except (ImportError, AttributeError):
                raise Exception("Could not find %s, looked in %s" % (cls_path, module))

        return class_obj

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

    def get_response_type(self):
        """
        Docstring may define custom response class
        """
        return self.object.get('type', None)

    def get_response_messages(self):
        """
        Retrieves response error codes from YAML object
        """
        messages = []
        response_messages = self.object.get('responseMessages', [])
        for message in response_messages:
            messages.append({
                'code': message.get('code', None),
                'message': message.get('message', None),
                'responseModel': message.get('responseModel', None),
            })
        return messages

    def get_parameters(self):
        """
        Retrieves parameters from YAML object
        """
        params = []
        fields = self.object.get('parameters', [])
        for field in fields:
            param_type = field.get('paramType', None)
            if param_type not in self.PARAM_TYPES:
                param_type = 'form'

            # Data Type & Format
            # See:
            # https://github.com/wordnik/swagger-core/wiki/1.2-transition#wiki-additions-2
            # https://github.com/wordnik/swagger-core/wiki/Parameters
            data_type = field.get('type', 'string')
            if param_type in ['path', 'query', 'header']:
                if data_type not in BaseMethodIntrospector.PRIMITIVES:
                    data_type = 'string'

            # Data Format
            data_format = field.get('format', None)
            flatten_primitives = [
                val for sublist in BaseMethodIntrospector.PRIMITIVES.values()
                for val in sublist
            ]

            if data_format not in flatten_primitives:
                formats = BaseMethodIntrospector.PRIMITIVES.get(data_type, None)
                if formats:
                    data_format = formats[0]
                else:
                    data_format = 'string'

            f = {
                'paramType': param_type,
                'name': field.get('name', None),
                'description': field.get('description', None),
                'type': data_type,
                'format': data_format,
                'required': field.get('required', False),
                'defaultValue': field.get('defaultValue', None),

            }

            # Allow Multiple Values &f=1,2,3,4
            if field.get('allowMultiple'):
                f['allowMultiple'] = True

            # Min/Max are optional
            if 'minimum' in field and data_type == 'integer':
                f['minimum'] = field.get('minimum', 0)

            if 'maximum' in field and data_type == 'integer':
                f['maximum'] = field.get('maximum', 0)

            # enum options
            enum = field.get('enum', [])
            if enum:
                f['enum'] = enum

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

        # paramType may differ, overwrite first
        # so strategy can be applied
        for meth_param in method_params:
            for doc_param in docstring_params:
                if doc_param['name'] == meth_param['name']:
                    if 'paramType' in doc_param:
                        meth_param['paramType'] = doc_param['paramType']

        for param_type in self.PARAM_TYPES:
            if self.should_omit_parameters(param_type):
                continue
            parameters += self._apply_strategy(
                param_type, method_params, docstring_params
            )

        # PATCH requests expects all fields except path fields to be optional
        if inspector.get_http_method() == "PATCH":
            for param in parameters:
                if param['paramType'] != 'path':
                    param['required'] = False

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
        import itertools
        merged = OrderedDict()
        for item in itertools.chain(params1, params2):
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
