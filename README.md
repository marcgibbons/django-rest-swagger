# Django REST Swagger
####An API documentation generator for Swagger UI and Django REST Framework version > 2.3.5

For older versions of Django REST Framework, see [Django REST Framework Docs](https://github.com/marcgibbons/django-rest-framework-docs)

## Installation
From PyPI: `pip install django-rest-swagger`

From source:
- Download the source
- Extract files
- Run `python setup.py install`

## Requirements
This application was developed and tested on:

* Django 1.5.1
* Django REST Framework 2.3.4, 2.3.5

Backwards compatibility for earlier Django & Django REST Framework versions will be added in a future release. Meanwhile, please use [Django REST Framework Docs](https://github.com/marcgibbons/django-rest-framework-docs) to document your projects.

## Quick start
**Note: This application will not work with Django REST Framework < 2.3**

1. Add `rest_framework_swagger` to your `INSTALLED_APPS` setting like this:

    ```python
        INSTALLED_APPS = (
            ...
            'rest_framework_swagger',
        )
    ```

2. Include the rest_framework_swagger URLs to a path of your choice

    ```python
    patterns = ('',
        ...
        url(r'^api-docs/', include('rest_framework_swagger.urls')),
    )
    ```

## Configuration
Further configuration can optionally be made from your project's `settings.py`.

* **Exclude namespaces:** you may wish to exclude a set of URLs from documentation. By default, all views that are subclassed from Django REST Framework APIView will be included for documentation
* **API Version:** your API's version. Default is blank.
* **Enabled methods:** You may specify the methods that can be interacted with in the UI
* **API key:** you can specify a key for your API. Default is blank

```python
SWAGGER_SETTINGS = {
    "exclude_namespaces": [], # List URL namespaces to ignore
    "api_version": '0.1',  # Specify your API's version
    "api_path": "/",  # Specify the path to your API not a root level
    "enabled_methods": [  # Specify which methods to enable in Swagger UI
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    "api_key": '', # An API key
    "is_authenticated": False,  # Set to True to enforce user authentication,
    "is_superuser": False,  # Set to True to enforce admin only access
}
```

## How It Works
This project is built on the [Django REST Framework Docs](https://github.com/marcgibbons/django-rest-framework-docs) and uses the lovely [Swagger from Wordnik](https://developers.helloreverb.com/swagger/) as an interface. This application introspectively generates documentation based on your Django REST Framework API code. Comments are generated in combination from code analysis and comment extraction. Here are some of the features that are documented:

* API title - taken from the class name
* Methods allowed
* Serializers & fields in use by a certain method
* Field default values, minimum, maximum, read-only and required attributes
* URL parameters (ie. /product/{id})
* Query parameters (user-defined) - Custom parameters. It is possible to customize a parameter list for your
    API. To do so, include a key-value pair in the docstring of your API class
    delimited by two hyphens ('--'). Example: 'start_time -- The first reading':

```python
    class Countries(APIView):
        """
        This text is the description for this API
        param1 -- A first parameter
        param2 -- A second parameter
        """
```

## Example
Included in this repository is a functioning example. Please clone the repo, copy or reference the `rest_framework_swagger` directory into the cigar_example folder. Install the required packages using `pip install -r requirements.txt`

## Screenshots
![](screenshots/api-list.png)
![](screenshots/fields.png)

## Bugs & Contributions
Please report bugs by opening an issue

Contributions are welcome and are encouraged !

## Special Thanks
![http://bnotions.com](http://bnotions.com/assets/img/bnotions_color.png)

Thanks to [BNOTIONS](http://www.bnotions.com) for sponsoring development time and for being an awesome place to work, play & innovate

Many thanks to Tom Christie & all the contributors who have developed [Django REST Framework](http://django-rest-framework.org/)

## Contributors
* Marc Gibbons (@marcgibbons)
* Geraldo Andrade (@quein)
* Vítek Pliska (@whit)
* Falk Schuetzenmeister (@postfalk)

### Django REST Framework Docs contributors:

* Scott Mountenay (@scottmx81)
* @swistakm
* Peter Baumgartner (@ipmb)
* Marlon Bailey (@avinash240)

## Release Notes:
### v0.1.7 (Sept 4, 2013)
* URL flattening fixes
* API root prefix fix

### v0.1.6 (August 3, 2013)
* Improvments and bug fixes with relative imports in Python 3
* throbber.gif image is being pointed to local copy

### v0.1.5 (July 30, 2013)
* Added permission settings for Swagger docs. Default is now allow any, which will override REST Framework settings
* Fixed throbber.gif URL in the swagger-ui.min.js to point to Wordnik's resource
