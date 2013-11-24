import os
from django.conf import settings
from django.utils.importlib import import_module
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern
from django.contrib.admindocs.views import simplify_regex
from rest_framework.views import APIView

from rest_framework_swagger.apidocview import APIDocView


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
            return self.get_filtered_apis(patterns, filter_path)

        patterns = self.__flatten_patterns_tree__(
            patterns,
            filter_path=filter_path,
            exclude_namespaces=exclude_namespaces,
        )

        return patterns

    def get_filtered_apis(self, patterns, filter_path):
        filtered_list = []

        all_apis = self.get_apis(patterns, exclude_namespaces=[])
        top_level_apis = self.get_top_level_apis(all_apis)
        top_level_apis.discard(filter_path)

        for top in list(top_level_apis):
            if top in filter_path: #and len(filter_path) > len(top):
                top_level_apis.remove(top)

        for api in all_apis:
            remove = False
            for top in top_level_apis:
                if top + '/' in api['path'].lstrip("/"):
                    remove = True

            if filter_path in api['path'].strip("/") and not remove:
                filtered_list.append(api)

        return filtered_list

    def get_top_level_apis(self, apis):
        """
        Returns the 'top level' APIs (ie. swagger 'resources')

        apis -- list of APIs as returned by self.get_apis
        """
        root_paths = set()
        api_paths = [endpoint['path'].strip("/") for endpoint in apis]

        for path in api_paths:
            #  If a URLs /resource/ and /resource/{pk} exist, use the base
            #  as the resource. If there is no base resource URL, then include
            path_base = path.split('/{')[0]
            if '{' in path and path_base in api_paths:
                continue
            root_paths.add(path_base)

        return root_paths

    def __assemble_endpoint_data__(self, pattern, prefix='', filter_path=None):
        """
        Creates a dictionary for matched API urls

        pattern -- the pattern to parse
        prefix -- the API path prefix (used by recursion)
        """
        callback = self.__get_pattern_api_callback__(pattern)

        if callback is None or self.__exclude_router_api_root__(callback):
            return

        path = simplify_regex(prefix + pattern.regex.pattern)

        if filter_path is not None:
            if filter_path not in path:
                return None

        path = path.replace('<', '{').replace('>', '}')

        if self.__exclude_format_endpoints__(path):
            return

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

                pref = prefix + pattern.regex.pattern
                pattern_list.extend(self.__flatten_patterns_tree__(pattern.url_patterns, pref, filter_path=filter_path))

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

    def __exclude_router_api_root__(self, callback):
        """
        Returns True if the URL's callback is rest_framework.routers.APIRoot
        """
        if callback.__module__ == 'rest_framework.routers':
            return True

        return False

    def __exclude_format_endpoints__(self, path):
        """
        Excludes URL patterns that contain .{format}
        """
        if '.{format}' in path:
            return True

        return False
