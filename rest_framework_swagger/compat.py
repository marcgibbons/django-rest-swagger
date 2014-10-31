import platform
if platform.python_version_tuple() < ('2', '7'):
    import ordereddict
    OrderedDict = ordereddict.OrderedDict
else:
    import collections
    OrderedDict = collections.OrderedDict
