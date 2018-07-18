# Django REST Swagger
Swagger/OpenAPI Documentation Generator for Django REST Framework

<iframe src="https://ghbtns.com/github-btn.html?user=marcgibbons&repo=django-rest-swagger&type=star&count=true" frameborder="0" scrolling="0" width="170px" height="20px"></iframe>

---

**Note:** you are viewing documentation for version 2, using Django REST Framework 3.5+ and CoreAPI. Documentation for previous versions is available [here](http://django-rest-swagger.readthedocs.io/en/stable-0.3.x/).

---

## Installation

`$ pip install django-rest-swagger`


Add `'rest_framework_swagger'` to `INSTALLED_APPS` in Django settings.

**settings.py**
```python
INSTALLED_APPS = [
    ...
    'rest_framework_swagger',
    ...
]
```

## Quick start

To quickly get started, use the `get_swagger_view` shortcut. This will produce
a schema view which uses common settings. For more advanced usage, please see
the schemas section.

#### Example

**urls.py**
```python
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^$', schema_view)
]
```

#### View in the browser
![Screenshot](/img/ui-screenshot.png)


## Example app
An example based on the [Django REST Tutorial](http://www.django-rest-framework.org/tutorial/1-serialization/) ships with the project. It can be deployed locally using Docker, or on heroku (for free).

### Deploy with Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/marcgibbons/django-rest-swagger)

Log in credentials are:
```
username: amy
password: amy
```

### Docker Instructions

Ensure [Docker](https://www.docker.com/) is installed on your system.

First, clone the repository:

`$ git clone https://github.com/marcgibbons/django-rest-swagger`

To quickly get up and running using the Docker image, simply run:

`$ ./run_example.sh`

The initial run may take several minutes to build. Once complete, the
application will be available at `http://localhost:8000`

Log in credentials are:
```
username: amy
password: amy
```

## Changes in 2.0
Version 2.0 is fundamentally different from previous versions and leverages the new schema generation features introduced in Django REST Framework 3.4. Introspection is performed by the framework and uses CoreAPI to store definitions. This is a breaking change from previous versions which were responsible for introspection as well as overrides.

New:

- SwaggerUI and the OpenAPI spec are renderer classes (simpler configuration)
- SwaggerUI 2.1.6
- Improved performance
- Allow multiple instances of Swagger UI in a single Django project
- Allow rendering the OpenAPI JSON spec independently
- Improved control of authentication mechanisms

Deprecated:

- YAML docstrings


## License
```text
Copyright (c) 2013-2018, Marc Gibbons
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
