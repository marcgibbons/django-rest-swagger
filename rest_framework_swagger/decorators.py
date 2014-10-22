import types
from django.utils import six
from collections import namedtuple


def serializer_class(clazz):
    def _get_serializer_class(self):
        return clazz

    def decorator(func):
        if not hasattr(func, 'cls'):
            raise Exception("""@serializer_class should be above @api_view, like so:

    @serializer_class(MySerializer)
    @api_view
    def my_view(request):
        ...
""")
        apiview = func.cls
        apiview.get_serializer_class = types.MethodType(
            _get_serializer_class,
            apiview)
        return func
    return decorator


unwrappage = namedtuple('unwrappage', ['closure', 'code'])


def closure_n_code(func):
    return unwrappage(
        six.get_function_closure(func),
        six.get_function_code(func))


def get_closure_var(func, name=None):
    unwrap = closure_n_code(func)
    i = 0
    if name:
        i = unwrap.code.co_freevars.index(name)
    return unwrap.closure[i].cell_contents


def wrapper_to_func(wrapper):
    noms = wrapper.http_method_names
    handlers = [getattr(wrapper, m) for m in noms if m != 'options']
    return get_closure_var(handlers[0], name="func")


def func_to_wrapper(func):
    return func.cls
