from django.conf import settings
from django.utils.importlib import import_module
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern
from django.contrib.admindocs.views import simplify_regex

from rest_framework.views import APIView


class UrlParser(object):

    def get_apis(self, patterns=None, exclude_namespaces=[]):
        """
        Returns all the DRF APIViews found in the project URLs

        patterns -- supply list of patterns (optional)
        exclude_namespaces -- list of namespaces to ignore (optional)
        """
        if patterns is None:
            urls = import_module(settings.ROOT_URLCONF)
            patterns = urls.urlpatterns

        patterns = self.__flatten_patterns_tree__(patterns, exclude_namespaces=exclude_namespaces)

        return patterns

    def get_top_level_apis(self, apis, pos=0):
        """
        Returns the 'top level' APIs (ie. swagger 'resources')

        apis -- list of APIs as returned by self.get_apis
        pos -- the position in the path (used by the recursion)
        """
        root_paths = set()

        for endpoint in apis:
            path = endpoint['path']

            if path[0] == '/':
                path = path[1:]

            split_path = path.split("/")

            if pos < len(split_path) and split_path[pos] != '':
                root_paths.add(path.split("/")[pos])

            base_path = "/".join(split_path[0:pos])

        if len(root_paths) == 1 and len(apis) > 1:
            next_level = self.get_top_level_apis(apis, pos + 1)
            root_paths = next_level['root_paths']
            base_path = next_level['base_path']

        return {
            'root_paths': root_paths,
            'base_path': base_path
        }

    def __assemble_endpoint_data__(self, pattern, prefix=''):
        """
        Creates a dictionary for matched API urls

        pattern -- the pattern to parse
        prefix -- the API path prefix (used by recursion)
        """
        callback = self.__get_pattern_api_callback__(pattern)

        if callback is None:
            return

        return {
            'path': simplify_regex(prefix + pattern.regex.pattern),
            'pattern': pattern,
            'callback': callback,
        }

    def __flatten_patterns_tree__(self, patterns, prefix='', exclude_namespaces=[]):
        """
        Uses recursion to flatten url tree.

        patterns -- urlpatterns list
        prefix -- (optional) Prefix for URL pattern
        """
        pattern_list = []

        for pattern in patterns:
            if isinstance(pattern, RegexURLPattern):
                endpoint_data = self.__assemble_endpoint_data__(pattern, prefix)

                if endpoint_data is None:
                    continue

                pattern_list.append(endpoint_data)

            elif isinstance(pattern, RegexURLResolver):

                if pattern.namespace in exclude_namespaces:
                    return

                prefix = pattern.regex.pattern
                pattern_list.extend(self.__flatten_patterns_tree__(pattern.url_patterns, prefix))

        return pattern_list

    def __get_pattern_api_callback__(self, pattern):
        """
        Verifies that pattern callback is a subclass of APIView, and returns the class
        Handles older django & django rest 'cls_instance'
        """
        if not hasattr(pattern, 'callback'):
            return

        if (hasattr(pattern.callback, 'cls') and
                issubclass(pattern.callback.cls, APIView)):

            return pattern.callback.cls

        elif (hasattr(pattern.callback, 'cls_instance') and
                isinstance(pattern.callback.cls_instance, APIView)):

            return pattern.callback.cls_instance
