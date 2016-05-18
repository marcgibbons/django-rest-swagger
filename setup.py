import os
import sys
import shutil
from setuptools import setup
from rest_framework_swagger import VERSION

if sys.argv[-1] == 'publish':
    if os.system("wheel version"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload -r pypi dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (VERSION, VERSION))
    print("  git push --tags")
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('django_rest_swagger.egg-info')
    sys.exit()

README = """
Django REST Swagger

An API documentation generator for Swagger UI and Django REST Framework version 2.3.8+

Installation
From pip:

pip install django-rest-swagger

Project @ https://github.com/marcgibbons/django-rest-swagger
Docs @ http://django-rest-swagger.readthedocs.org/
"""

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
install_requires = [
    'Django>=1.5',
    'djangorestframework>=2.3.8',
    'PyYAML>=3.10',
]

import platform

version = platform.python_version_tuple()
if version < ('2','7'):
    install_requires.append('importlib>=1.0.1')
    install_requires.append('ordereddict>=1.1')

setup(
    name='django-rest-swagger',
    version=VERSION,
    packages=['rest_framework_swagger'],
    package_data={'rest_framework_swagger': ['rest_framework_swagger/templates/rest_framework_swagger/*', 'rest_framework_swagger/static/rest_framework_swagger/*']},
    include_package_data=True,
    license='FreeBSD License',
    description='Swagger UI for Django REST Framework 2.3.8+',
    long_description=README,
    install_requires=install_requires,
    extras_require = {
        'reST': ['docutils>=0.8'],
    },

    author='Marc Gibbons',
    author_email='marc_gibbons@rogers.com',
    maintainer='Ellery Newcomer',
    maintainer_email='ellery-newcomer@utulsa.edu',
    url='http://github.com/marcgibbons/django-rest-swagger',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
