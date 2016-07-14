#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.dirname('../%s' % __file__)))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tutorial.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
