from django.conf.urls import patterns
from rest_framework_swagger.views import SwaggerResourcesView, SwaggerApiView, SwaggerUIView


urlpatterns = patterns('',
    (r'^$', SwaggerUIView.as_view()),
    (r'^api-docs/$', SwaggerResourcesView.as_view()),
    (r'^api-docs/(?P<path>.*)/$', SwaggerApiView.as_view()),
)
