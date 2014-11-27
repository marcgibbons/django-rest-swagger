# Django REST Swagger

[![Build Status](https://travis-ci.org/marcgibbons/django-rest-swagger.svg?branch=master)](https://travis-ci.org/marcgibbons/django-rest-swagger)

####An API documentation generator for Swagger UI and Django REST Framework

Documentation: http://django-rest-swagger.readthedocs.org/

This project is built on the [Django REST Framework Docs](https://github.com/marcgibbons/django-rest-framework-docs) and uses the lovely [Swagger from Wordnik](https://developers.helloreverb.com/swagger/) as an interface. This application introspectively generates documentation based on your Django REST Framework API code. Comments are generated in combination from code analysis and comment extraction. Here are some of the features that are documented:

* API title - taken from the class name
* Methods allowed
* Serializers & fields in use by a certain method
* Field default values, minimum, maximum, read-only and required attributes
* URL parameters (ie. /product/{id})
* Field `help_text` property is used to create the description from the serializer or model.

## Requirements
* Python (2.6.5+, 2.7, 3.2, 3.3, 3.4)
* Django (1.5.5+, 1.6, 1.7)
* Django REST framework (2.3.5+)

## Bugs & Contributions
Please report bugs by opening an issue

Contributions are welcome and are encouraged!

## Special Thanks
Thanks to [BNOTIONS](http://www.bnotions.com) for sponsoring initial development time.

Many thanks to Tom Christie & all the contributors who have developed [Django REST Framework](http://django-rest-framework.org/)

## Contributors
* Marc Gibbons (@marcgibbons)
* Geraldo Andrade (@quein)
* Vítek Pliska (@whit)
* Falk Schuetzenmeister (@postfalk)
* Lukas Hetzenecker (@lukas-hetzenecker)
* David Wolever (@wolever)
* Brian Moe (@bmoe)
* Ian Martin (@aztechian)
* @pzrq
* @jfelectron
* Warnar Boekkooi (@boekkooi)
* Darren Thompson (@WhiteDawn)
* Lukasz Balcerzak (@lukaszb)
* David Newgas (@davidn)
* Bozidar Benko (@bbenko)
* @pySilver


### Django REST Framework Docs contributors:

* Scott Mountenay (@scottmx81)
* @swistakm
* Peter Baumgartner (@ipmb)
* Marlon Bailey (@avinash240)

## Release Notes:

### v0.2.1 (November 15, 2014)
* add readthedocs based documentation 
* add request and response serializer spec to yaml
* preserve order of fields in serializers
* support nested serializers

### v0.2.0 (October 31, 2014)
* Added YAML Parser to docstring handling
* Fixed Python 3 bugs

### v0.1.14 (March 7, 2014)
* Fixed resource name truncation bug

### v0.1.13 (Feb 25, 2014)
* Fixed grouping bug

### v0.1.12 (Feb 24, 2014)
* Improved resource grouping
* Alphabetical sorting of resources
* Fixed CSRF headers
* Misc bug fixes & improvements

### v0.1.11 (Dec 1, 2013)
* Added proper unicode support for Python 2
* Compatibility fixes for Python 3
* Changed settings template var to avoid naming conflicts
* Fixed mapping dict constructor in introspectors for Python 2.6 support

### v0.1.10 (Nov 23, 2013)
* Upgraded Swagger UI version
* Now supports Django ViewSet method-level documentation
* Now supports ViewSet @action & @link method implementation
* Added blank HttpRequest to the callback for those who like to hack the get_serializer classes
* HTML Markdown supported in docstrings (use responsibly)

### v0.1.9 (Oct 1, 2013)
* Revisited doc algorithm
* Added support for APPEND_SLASH = False

### v0.1.8 (Sept 16, 2013)
* Fixed broken imports - Now supports DRF 2.3.8
* Added description on the model field

### v0.1.7 (Sept 4, 2013)
* URL flattening fixes
* API root prefix fix

### v0.1.6 (August 3, 2013)
* Improvments and bug fixes with relative imports in Python 3
* throbber.gif image is being pointed to local copy

### v0.1.5 (July 30, 2013)
* Added permission settings for Swagger docs. Default is now allow any, which will override REST Framework settings
* Fixed throbber.gif URL in the swagger-ui.min.js to point to Wordnik's resource


