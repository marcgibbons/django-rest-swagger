from distutils.version import StrictVersion
import rest_framework
import platform
if platform.python_version_tuple() < ('2', '7'):
    import ordereddict
    OrderedDict = ordereddict.OrderedDict
else:
    import collections
    OrderedDict = collections.OrderedDict

if platform.python_version_tuple() < ('3', '0'):
    from HTMLParser import HTMLParser

    class MLStripper(HTMLParser):
        def __init__(self):
            self.reset()
            self.fed = []

        def handle_data(self, d):
            self.fed.append(d)

        def get_data(self):
            return ''.join(self.fed)
else:
    from html.parser import HTMLParser

    class MLStripper(HTMLParser):
        def __init__(self):
            self.reset()
            self.strict = False
            self.convert_charrefs = True
            self.fed = []

        def handle_data(self, d):
            self.fed.append(d)

        def get_data(self):
            return ''.join(self.fed) + self.rawdata


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

try:
    from django.utils.module_loading import import_string
except ImportError:
    def import_string(dotted_path):
        from django.utils.importlib import import_module
        from django.core.exceptions import ImproperlyConfigured
        module, attr = dotted_path.rsplit('.', 1)
        try:
            mod = import_module(module)
        except ImportError as e:
            raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                       (module, e))
        try:
            view = getattr(mod, attr)
        except AttributeError:
            raise ImproperlyConfigured('Module "%s" does not define a "%s".'
                                       % (module, attr))
        return view


def get_pagination_attribures(view):
    if StrictVersion(rest_framework.VERSION) >= StrictVersion('3.1.0'):
        if not (hasattr(view, 'pagination_class') and view.pagination_class):
            return None, None, None

        page_size = hasattr(view.pagination_class, 'page_size') and \
            view.pagination_class.page_size
        page_query_param = hasattr(view.pagination_class, 'page_query_param') and \
            view.pagination_class.page_query_param
        page_size_query_param = hasattr(view.pagination_class, 'page_size_query_param') and \
            view.pagination_class.page_size_query_param
    else:
        if not hasattr(view, 'paginate_by'):
            return None, None, None

        page_size = view.paginate_by
        page_query_param = view.page_kwarg
        page_size_query_param = hasattr(view, 'paginate_by_param') and \
            view.paginate_by_param

    return page_size, page_query_param, page_size_query_param
