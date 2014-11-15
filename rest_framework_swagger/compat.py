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
            return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
