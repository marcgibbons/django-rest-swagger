"""
Generates Documentation
"""
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
                'operations': self.__get_operations__(api['callback']),
            })

        return api_docs

    def __get_operations__(self, callback):
        """
        Returns docs for the allowed methods of an API endpoint
        """
        operations = []

        for method in callback.allowed_methods:
            if method == "OPTIONS":
                continue  # No one cares

            operations.append({
                'httpMethod': method,
                'summary': self.__get_method_docs__(callback, method),
                'nickname': self.__get_nickname__(callback),
                'notes': self.__get_notes__(callback),
            })

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
