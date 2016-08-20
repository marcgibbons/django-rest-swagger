# Customization

## Template
The template used for the SwaggerUIRenderer can be customized by writing overriding
`rest_framework_swagger/index.html`.

Here are a few basic areas which can be customized:

- `{% block extra_styles %}` Add additional stylsheets
- `{% block extra_scripts %}` Add additional scripts.
- `{% block user_context_message %}` Customize the "Hello, user" message (Django session only)
- `{% block extra_nav %}` Placeholder for additional content in the nav bar.
