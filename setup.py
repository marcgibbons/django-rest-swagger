import os
from setuptools import setup
from rest_framework_swagger import VERSION

#README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
README = """
Django REST Swagger

An API documentation generator for Swagger UI and Django REST Framework version 2.3+

Installation
From pip:

pip install django-rest-swagger

Docs & details @
https://github.com/marcgibbons/django-rest-swagger
"""

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-rest-swagger',
    version=VERSION,
    packages=['rest_framework_swagger'],
    package_data={'rest_framework_swagger': ['rest_framework_swagger/templates/rest_framework_swagger/*', 'rest_framework_swagger/static/rest_framework_swagger/*']},
    include_package_data=True,
    license='FreeBSD License',
    description='Swagger UI for Django REST Framework 2.3+',
    long_description=README,
    install_requires=[
        'django>=1.5',
        'djangorestframework>=2.3.5',
        'Unipath>=1.0'
    ],

    url='http://github.com/marcgibbons',
    author='Marc Gibbons',
    author_email='marc_gibbons@rogers.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

