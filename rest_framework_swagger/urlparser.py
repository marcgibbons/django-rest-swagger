import os
from django.conf import settings
from django.utils.importlib import import_module
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern
from django.contrib.admindocs.views import simplify_regex
from rest_framework.views import APIView

from apidocview import APIDocView


class UrlParser(object):

    def get_apis(self, patterns=None, filter_path=None, exclude_namespaces=[]):
        """
        Returns all the DRF APIViews found in the project URLs

        patterns -- supply list of patterns (optional)
        exclude_namespaces -- list of namespaces to ignore (optional)
        """
        if patterns is None:
            urls = import_module(settings.ROOT_URLCONF)
            patterns = urls.urlpatterns

        if filter_path is not None:
            all_apis = self.get_apis(patterns, exclude_namespaces=[])
            top_level_apis = list(self.get_top_level_apis(all_apis))

            if filter_path in top_level_apis:
                top_level_apis.remove(filter_path)

            for top in top_level_apis:
                if top in filter_path:
                    top_level_apis.remove(top)

            for pattern in patterns:
                for top in top_level_apis:
                    if top in pattern.regex.pattern:
                        patterns.remove(pattern)

        patterns = self.__flatten_patterns_tree__(
            patterns,
            filter_path=filter_path,
            exclude_namespaces=exclude_namespaces,
        )

        return patterns

    def get_top_level_apis(self, apis):
        """
        Returns the 'top level' APIs (ie. swagger 'resources')

        apis -- list of APIs as returned by self.get_apis
        """
        root_paths = set()

        api_paths = [endpoint['path'].strip("/") for endpoint in apis]
        base_path = os.path.commonprefix(api_paths) #.split("/")[0]

        for path in api_paths:
            if '{' in path:
                continue
            root_paths.add(path)

        return root_paths

    def __assemble_endpoint_data__(self, pattern, prefix='', filter_path=None):
        """
        Creates a dictionary for matched API urls

        pattern -- the pattern to parse
        prefix -- the API path prefix (used by recursion)
        """
        callback = self.__get_pattern_api_callback__(pattern)

        if callback is None:
            return

        path = simplify_regex(prefix + pattern.regex.pattern)

        if filter_path is not None:
            if filter_path not in path:
                return None

        path = path.replace('<', '{').replace('>', '}')

        return {
            'path': path,
            'pattern': pattern,
            'callback': callback,
        }

    def __flatten_patterns_tree__(self, patterns, prefix='', filter_path=None, exclude_namespaces=[]):
        """
        Uses recursion to flatten url tree.

        patterns -- urlpatterns list
        prefix -- (optional) Prefix for URL pattern
        """
        pattern_list = []

        for pattern in patterns:
            if isinstance(pattern, RegexURLPattern):
                endpoint_data = self.__assemble_endpoint_data__(pattern, prefix, filter_path=filter_path)

                if endpoint_data is None:
                    continue

                pattern_list.append(endpoint_data)

            elif isinstance(pattern, RegexURLResolver):

                if pattern.namespace in exclude_namespaces:
                    continue

                prefix = pattern.regex.pattern
                pattern_list.extend(self.__flatten_patterns_tree__(pattern.url_patterns, prefix, filter_path=filter_path))

        return pattern_list

    def __get_pattern_api_callback__(self, pattern):
        """
        Verifies that pattern callback is a subclass of APIView, and returns the class
        Handles older django & django rest 'cls_instance'
        """
        if not hasattr(pattern, 'callback'):
            return

        if (hasattr(pattern.callback, 'cls') and
                issubclass(pattern.callback.cls, APIView) and
                not issubclass(pattern.callback.cls, APIDocView)):

            return pattern.callback.cls

        elif (hasattr(pattern.callback, 'cls_instance') and
                isinstance(pattern.callback.cls_instance, APIView) and
                not issubclass(pattern.callback.cls_instance, APIDocView)):

            return pattern.callback.cls_instance

