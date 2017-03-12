# Customization

## Template
The template used for the SwaggerUIRenderer can be customized by overriding
`rest_framework_swagger/index.html`.

Here are a few basic areas which can be customized:

- `{% block extra_styles %}` Add additional stylsheets
- `{% block extra_scripts %}` Add additional scripts.
- `{% block user_context_message %}` Customize the "Hello, user" message (Django session only)
- `{% block extra_nav %}` Placeholder for additional content in the nav bar.
- `{% block logo %}` Logo area of the nav bar.


## Version Headers
The following would append a version number to every request, which is required
with `rest_framework.versioning.AcceptHeaderVersioning`.
This should go into `rest_framework_swagger/index.html` in your template path.

```html
{% extends "rest_framework_swagger/base.html" %}

{% block extra_scripts %}
<script type="text/javascript">
  $(function () {
    var ApiVersionAuthorization = function () {};
    ApiVersionAuthorization.prototype.apply = function (obj) {
      obj.headers['Accept'] += '; version=1.0';
      return true;
    };
    swaggerUi.api.clientAuthorizations.add(
        'api_version',
        new ApiVersionAuthorization()
    );
  });
</script>
{% endblock extra_scripts %}
```
