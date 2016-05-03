# -*- coding: utf-8 -*-

"""Handles the instrospection of REST Framework Views and ViewSets."""

import inspect
import itertools
import re
import yaml
import importlib

from .compat import OrderedDict, strip_tags, get_pagination_attribures
from abc import ABCMeta, abstractmethod

from django.http import HttpRequest
from django.contrib.admindocs.utils import trim_docstring
from django.utils.encoding import smart_text

import rest_framework
from rest_framework import viewsets
from rest_framework.compat import apply_markdown
try:
    from rest_framework.fields import CurrentUserDefault
except ImportError:
    # FIXME once we drop support of DRF 2.x .
    CurrentUserDefault = None
from rest_framework.utils import formatting
from django.utils import six
try:
    import django_filters
except ImportError:
    django_filters = None


def get_view_description(view_cls, html=False, docstring=None):
    if docstring is not None:
        view_cls = type(
            view_cls.__name__ + '_fake',
            (view_cls,),
            {'__doc__': docstring})
    return rest_framework.settings.api_settings \
        .VIEW_DESCRIPTION_FUNCTION(view_cls, html)


def get_default_value(field):
    default_value = getattr(field, 'default', None)
    if rest_framework.VERSION >= '3.0.0':
        from rest_framework.fields import empty
        if default_value == empty:
            default_value = None
    if callable(default_value):
        if CurrentUserDefault is not None and isinstance(default_value,
                                                         CurrentUserDefault):
            default_value.user = None
        default_value = default_value()
    return default_value


class IntrospectorHelper(object):
    __metaclass__ = ABCMeta

    @staticmethod
    def strip_yaml_from_docstring(docstring):
        """
        Strips YAML from the docstring.
        """
        split_lines = trim_docstring(docstring).split('\n')

        cut_off = None
        for index in range(len(split_lines) - 1, -1, -1):
            line = split_lines[index]
            line = line.strip()
            if line == '---':
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
        params_pattern = re.compile(r' -- ')
        split_lines = trim_docstring(docstring).split('\n')

        cut_off = None
        for index, line in enumerate(split_lines):
            line = line.strip()
            if params_pattern.search(line):
                cut_off = index
                break
        if cut_off is not None:
            split_lines = split_lines[0:cut_off]

        return "\n".join(split_lines)

    @staticmethod
    def get_serializer_name(serializer):
        if serializer is None:
            return None
        if rest_framework.VERSION >= '3.0.0':
            from rest_framework.serializers import ListSerializer
            assert serializer != ListSerializer, "uh oh, what now?"
            if isinstance(serializer, ListSerializer):
                serializer = serializer.child

        if inspect.isclass(serializer):
            return serializer.__name__

        return serializer.__class__.__name__

    @staticmethod
    def get_summary(callback, docstring=None):
        """
        Returns the first sentence of the first line of the class docstring
        """
        description = get_view_description(
            callback, html=False, docstring=docstring) \
            .split("\n")[0].split(".")[0]
        description = IntrospectorHelper.strip_yaml_from_docstring(
            description)
        description = IntrospectorHelper.strip_params_from_docstring(
            description)
        description = strip_tags(get_view_description(
            callback, html=True, docstring=description))
        return description


class BaseViewIntrospector(object):
    __metaclass__ = ABCMeta

    def __init__(self, callback, path, pattern, user):
        self.callback = callback
        self.path = path
        self.pattern = pattern
        self.user = user

    def get_yaml_parser(self):
        parser = YAMLDocstringParser(self)
        return parser

    @abstractmethod
    def __iter__(self):
        pass

    def get_iterator(self):
        return self.__iter__()

    def get_description(self):
        """
        Returns the first sentence of the first line of the class docstring
        """
        return IntrospectorHelper.get_summary(self.callback)

    def get_docs(self):
        return get_view_description(self.callback)


class BaseMethodIntrospector(object):
    __metaclass__ = ABCMeta

    ENUMS = [
        'choice',
        'multiple choice',
    ]

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
        self.user = view_introspector.user

    @property
    def is_array_response(self):
        """ Support definition of array responses with the 'many' attr """
        return self.get_yaml_parser().object.get('many')

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

    def get_extra_serializer_classes(self):
        return self.get_yaml_parser().get_extra_serializer_classes(
            self.callback)

    def ask_for_serializer_class(self):
        if hasattr(self.callback, 'get_serializer_class'):
            view = self.create_view()
            parser = self.get_yaml_parser()
            mock_view = parser.get_view_mocker(self.callback)
            view = mock_view(view)
            if view is not None:
                if parser.should_omit_serializer():
                    return None
                try:
                    serializer_class = view.get_serializer_class()
                except AssertionError as e:
                    if "should either include a `serializer_class` attribute, or override the `get_serializer_class()` method." in str(e):  # noqa
                        serializer_class = None
                    else:
                        raise
                return serializer_class

    def create_view(self):
        view = self.callback()
        if not hasattr(view, 'kwargs'):
            view.kwargs = dict()
        if hasattr(self.parent.pattern, 'default_args'):
            view.kwargs.update(self.parent.pattern.default_args)
        view.request = HttpRequest()
        view.request.user = self.user
        view.request.method = self.method
        return view

    def get_serializer_class(self):
        parser = self.get_yaml_parser()
        serializer = parser.get_serializer_class(self.callback)
        if serializer is None:
            serializer = self.ask_for_serializer_class()
        return serializer

    def get_response_serializer_class(self):
        parser = self.get_yaml_parser()
        serializer = parser.get_response_serializer_class(self.callback)
        if serializer is None:
            serializer = self.get_serializer_class()
        return serializer

    def get_request_serializer_class(self):
        parser = self.get_yaml_parser()
        serializer = parser.get_request_serializer_class(self.callback)
        if serializer is None:
            serializer = self.get_serializer_class()
        return serializer

    def get_summary(self):
        # If there is no docstring on the method, get class docs
        return IntrospectorHelper.get_summary(
            self.callback,
            self.get_docs() or self.parent.get_description())

    def get_nickname(self):
        """ Returns the APIView's nickname """
        return rest_framework.settings.api_settings \
            .VIEW_NAME_FUNCTION(self.callback, self.method).replace(' ', '_')

    def get_notes(self):
        """
        Returns the body of the docstring trimmed before any parameters are
        listed. First, get the class docstring and then get the method's. The
        methods will always inherit the class comments.
        """
        docstring = ""

        class_docs = get_view_description(self.callback)
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
        docstring = docstring.strip()

        return do_markdown(docstring)

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
        query_params = self.build_query_parameters()
        if django_filters is not None:
            query_params.extend(
                self.build_query_parameters_from_django_filters())

        if path_params:
            params += path_params

        if self.get_http_method() not in ["GET", "DELETE", "HEAD"]:
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

        return get_view_description(getattr(self.callback, method))

    def build_body_parameters(self):
        serializer = self.get_request_serializer_class()
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

    def build_query_parameters(self):
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
                               'type': 'string'})

        return params

    def build_query_parameters_from_django_filters(self):
        """
        introspect ``django_filters.FilterSet`` instances.
        """
        params = []
        filter_class = getattr(self.callback, 'filter_class', None)
        if (filter_class is not None and
                issubclass(filter_class, django_filters.FilterSet)):
            for name, filter_ in filter_class.base_filters.items():
                data_type = 'string'
                parameter = {
                    'paramType': 'query',
                    'name': name,
                    'description': filter_.label,
                }
                normalize_data_format(data_type, None, parameter)
                multiple_choices = filter_.extra.get('choices', {})
                if multiple_choices:
                    parameter['enum'] = [choice[0] for choice
                                         in itertools.chain(multiple_choices)]
                    parameter['type'] = 'enum'
                params.append(parameter)

        return params

    def build_form_parameters(self):
        """
        Builds form parameters from the serializer class
        """
        data = []
        serializer = self.get_request_serializer_class()

        if serializer is None:
            return data

        fields = serializer().get_fields()

        for name, field in fields.items():

            if getattr(field, 'read_only', False):
                continue

            data_type, data_format = get_data_type(field) or ('string', 'string')
            if data_type == 'hidden':
                continue

            # guess format
            # data_format = 'string'
            # if data_type in self.PRIMITIVES:
                # data_format = self.PRIMITIVES.get(data_type)[0]

            choices = []
            if data_type in BaseMethodIntrospector.ENUMS:
                if isinstance(field.choices, list):
                    choices = [k for k, v in field.choices]
                elif isinstance(field.choices, dict):
                    choices = [k for k, v in field.choices.items()]

            if choices:
                # guest data type and format
                data_type, data_format = get_primitive_type(choices[0]) or ('string', 'string')

            f = {
                'paramType': 'form',
                'name': name,
                'description': getattr(field, 'help_text', '') or '',
                'type': data_type,
                'format': data_format,
                'required': getattr(field, 'required', False),
                'defaultValue': get_default_value(field),
            }

            # Swagger type is a primitive, format is more specific
            if f['type'] == f['format']:
                del f['format']

            # defaultValue of null is not allowed, it is specific to type
            if f['defaultValue'] is None:
                del f['defaultValue']

            # Min/Max values
            max_value = getattr(field, 'max_value', None)
            min_value = getattr(field, 'min_value', None)
            if max_value is not None and data_type == 'integer':
                f['minimum'] = min_value

            if max_value is not None and data_type == 'integer':
                f['maximum'] = max_value

            # ENUM options
            if choices:
                f['enum'] = choices

            data.append(f)

        return data


def get_primitive_type(var):
    if isinstance(var, bool):
        return 'boolean', 'boolean'
    elif isinstance(var, int):
        return 'integer', 'int32'
    elif isinstance(var, float):
        return 'number', 'float'
    elif isinstance(var, six.string_types):
        return 'string', 'string'
    else:
        return 'string', 'string'  # 'default'


def get_data_type(field):
    # (in swagger 2.0 we might get to use the descriptive types..
    from rest_framework import fields
    if isinstance(field, fields.BooleanField):
        return 'boolean', 'boolean'
    elif hasattr(fields, 'NullBooleanField') and isinstance(field, fields.NullBooleanField):
        return 'boolean', 'boolean'
    # elif isinstance(field, fields.URLField):
        # return 'string', 'string' #  'url'
    # elif isinstance(field, fields.SlugField):
        # return 'string', 'string', # 'slug'
    elif isinstance(field, fields.ChoiceField):
        return 'choice', 'choice'
    # elif isinstance(field, fields.EmailField):
        # return 'string', 'string' #  'email'
    # elif isinstance(field, fields.RegexField):
        # return 'string', 'string' # 'regex'
    elif isinstance(field, fields.DateField):
        return 'string', 'date'
    elif isinstance(field, fields.DateTimeField):
        return 'string', 'date-time'  # 'datetime'
    # elif isinstance(field, fields.TimeField):
        # return 'string', 'string' # 'time'
    elif isinstance(field, fields.IntegerField):
        return 'integer', 'int64'  # 'integer'
    elif isinstance(field, fields.FloatField):
        return 'number', 'float'  # 'float'
    # elif isinstance(field, fields.DecimalField):
        # return 'string', 'string' #'decimal'
    # elif isinstance(field, fields.ImageField):
        # return 'string', 'string' # 'image upload'
    # elif isinstance(field, fields.FileField):
        # return 'string', 'string' # 'file upload'
    # elif isinstance(field, fields.CharField):
        # return 'string', 'string'
    elif rest_framework.VERSION >= '3.0.0':
        if isinstance(field, fields.HiddenField):
            return 'hidden', 'hidden'
        elif isinstance(field, fields.ListField):
            return 'array', 'array'
        else:
            return 'string', 'string'
    else:
        return 'string', 'string'


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
        class_docs = get_view_description(self.callback)
        class_docs = IntrospectorHelper.strip_yaml_from_docstring(
            class_docs)
        class_docs = IntrospectorHelper.strip_params_from_docstring(
            class_docs)
        return get_view_description(
            self.callback, html=True, docstring=class_docs)


def do_markdown(docstring):
    # Markdown is optional
    if apply_markdown:
        return apply_markdown(docstring)
    else:
        return docstring.replace("\n\n", "<br/>")


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
        return get_view_description(self.callback)

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

    def __init__(self, callback, path, pattern, user, patterns=None):
        super(ViewSetIntrospector, self).__init__(callback, path, pattern, user)
        if not issubclass(callback, viewsets.ViewSetMixin):
            raise Exception("wrong callback passed to ViewSetIntrospector")
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
            raise RuntimeError(
                'Unable to use callback invalid closure/function ' +
                'specified.')
        else:
            return x.closure[freevars.index('actions')].cell_contents


class ViewSetMethodIntrospector(BaseMethodIntrospector):
    def __init__(self, view_introspector, method, http_method):
        super(ViewSetMethodIntrospector, self) \
            .__init__(view_introspector, method)
        self.http_method = http_method.upper()

    @property
    def is_array_response(self):
        """ ViewSet.list methods always return array responses """
        return (self.method == 'list' or
                super(ViewSetMethodIntrospector, self).is_array_response)

    def get_http_method(self):
        return self.http_method

    def get_docs(self):
        """
        Attempts to retrieve method specific docs for an
        endpoint. If none are available, the class docstring
        will be used
        """
        return self.retrieve_docstring()

    def create_view(self):
        view = super(ViewSetMethodIntrospector, self).create_view()
        if not hasattr(view, 'action'):
            setattr(view, 'action', self.method)
        view.request.method = self.http_method
        return view

    def build_query_parameters(self):
        parameters = super(ViewSetMethodIntrospector, self) \
            .build_query_parameters()
        view = self.create_view()
        page_size, page_query_param, page_size_query_param = get_pagination_attribures(view)
        if self.method == 'list' and page_size:
            data_type = 'integer'
            if page_query_param:
                parameters.append({
                    'paramType': 'query',
                    'name': page_query_param,
                    'description': None,
                })
                normalize_data_format(data_type, None, parameters[-1])
            if page_size_query_param:
                parameters.append({
                    'paramType': 'query',
                    'name': page_size_query_param,
                    'description': None,
                })
                normalize_data_format(data_type, None, parameters[-1])
        return parameters


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


def normalize_data_format(data_type, data_format, obj):
    """
    sets 'type' on obj
    sets a valid 'format' on obj if appropriate
    uses data_format only if valid
    """
    if data_type == 'array':
        data_format = None

    flatten_primitives = [
        val for sublist in BaseMethodIntrospector.PRIMITIVES.values()
        for val in sublist
    ]

    if data_format not in flatten_primitives:
        formats = BaseMethodIntrospector.PRIMITIVES.get(data_type, None)
        if formats:
            data_format = formats[0]
        else:
            data_format = None
    if data_format == data_type:
        data_format = None

    obj['type'] = data_type
    if data_format is None and 'format' in obj:
        del obj['format']
    elif data_format is not None:
        obj['format'] = data_format


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

    def get_extra_serializer_classes(self, callback):
        """
        Retrieves serializer classes from pytype YAML objects
        """
        parameters = self.object.get('parameters', [])
        serializers = []
        for parameter in parameters:
            serializer = parameter.get('pytype', None)
            if serializer is not None:
                try:
                    serializer = self._load_class(serializer, callback)
                    serializers.append(serializer)
                except (ImportError, ValueError):
                    pass
        return serializers

    def get_request_serializer_class(self, callback):
        """
        Retrieves request serializer class from YAML object
        """
        serializer = self.object.get('request_serializer', None)
        try:
            return self._load_class(serializer, callback)
        except (ImportError, ValueError):
            pass
        return None

    def get_response_serializer_class(self, callback):
        """
        Retrieves response serializer class from YAML object
        """
        serializer = self.object.get('response_serializer', None)
        if isinstance(serializer, list):
            serializer = serializer[0]
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

    def get_consumes(self):
        """
        Retrieves media type supported as input
        """
        return self.object.get('consumes', [])

    def get_produces(self):
        """
        Retrieves media type supported as output
        """
        return self.object.get('produces', [])

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

    def get_view_mocker(self, callback):
        view_mocker = self.object.get('view_mocker', lambda a: a)
        if isinstance(view_mocker, six.string_types):
            view_mocker = self._load_class(view_mocker, callback)
        return view_mocker

    def get_parameters(self, callback):
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
            pytype = field.get('pytype', None)
            if pytype is not None:
                try:
                    serializer = self._load_class(pytype, callback)
                    data_type = IntrospectorHelper.get_serializer_name(
                        serializer)
                except (ImportError, ValueError):
                    pass
            if param_type in ['path', 'query', 'header']:
                if data_type not in BaseMethodIntrospector.PRIMITIVES:
                    data_type = 'string'

            # Data Format
            data_format = field.get('format', None)

            f = {
                'paramType': param_type,
                'name': field.get('name', None),
                'description': field.get('description', ''),
                'required': field.get('required', False),
            }

            normalize_data_format(data_type, data_format, f)

            if field.get('defaultValue', None) is not None:
                f['defaultValue'] = field.get('defaultValue', None)

            # Allow Multiple Values &f=1,2,3,4
            if field.get('allowMultiple'):
                f['allowMultiple'] = True

            if f['type'] == 'array':
                items = field.get('items', {})
                elt_data_type = items.get('type', 'string')
                elt_data_format = items.get('type', 'format')
                f['items'] = {
                }
                normalize_data_format(elt_data_type, elt_data_format, f['items'])

                uniqueItems = field.get('uniqueItems', None)
                if uniqueItems is not None:
                    f['uniqueItems'] = uniqueItems

            # Min/Max are optional
            if 'minimum' in field and data_type == 'integer':
                f['minimum'] = str(field.get('minimum', 0))

            if 'maximum' in field and data_type == 'integer':
                f['maximum'] = str(field.get('maximum', 0))

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
        docstring_params = self.get_parameters(inspector.callback)
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
        def filter_by(o):
            return o.get(key, None) == val
        return filter(filter_by, params)

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
